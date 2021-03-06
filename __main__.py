from math import ceil


def get_shape_name(input_values, filling_symbol):
    min_x = min_y = float('inf')
    max_x = max_y = -1
    filled_cells = y = 0
    top_lft = {'x': float('inf'), 'y': float('inf')}
    top_rgt = {'x': -1, 'y': float('inf')}
    btm_lft = {'x': float('inf'), 'y': -1}
    btm_rgt = {'x': float('inf'), 'y': -1}

    for row in input_values:
        for x in range(len(row)):
            if filling_symbol == row[x]:
                min_x, min_y = min(min_x, x), min(min_y, y)
                max_x, max_y = max(max_x, x), max(max_y, y)
                filled_cells += 1

                # Check top left position
                if y < top_lft['y']:
                    top_lft = {'x': min(x, top_lft['x']), 'y': y}
                # Check top right position. Might be the same point as top left
                if x >= top_lft['x'] and y <= top_rgt['y']:
                    top_rgt = {'x': max(x, top_rgt['x']), 'y': min(y, top_rgt['y'])}
                # Check the bottom left position
                if x <= btm_lft['x'] and y >= btm_lft['y']:
                    btm_lft = {'x': min(x, btm_lft['x']), 'y': max(y, btm_lft['y'])}
                # Check the bottom right position
                if x >= btm_rgt['x'] or y >= btm_rgt['y']:
                    btm_rgt = {'x': x, 'y': y}
        y += 1

    # Nothing found
    if 0 == filled_cells:
        return 'NONE'

    # A single dot has been found
    if 1 == filled_cells:
        return 'DOT'

    top_width = top_rgt['x'] - top_lft['x'] + 1
    lft_height = btm_lft['y'] - top_lft['y'] + 1

    # The shape is perfectly filled so it can be either a square or a rectangle
    if filled_cells == top_width*lft_height:
        return 'SQUARE' if top_width == lft_height else 'RECTANGLE'

    # The shape might be a perfect circle
    diff_x = max_x - min_x + 1
    diff_y = max_y - min_y + 1
    is_centered = (max_x + btm_lft['x'])/2 == top_lft['x']

    if is_centered and (diff_x == diff_y or diff_y == diff_x + 1 or diff_x == diff_y + 1):
        expected_size = calculate_surface(diff_x - 2, 0, -2)*2 + diff_x
        if expected_size == filled_cells:
            return 'CIRCLE'

    # A triangle maybe ?
    expected_size = -1

    if top_lft == top_rgt or top_lft == btm_lft or btm_lft == btm_rgt:
        # equilateral triangle
        if diff_x == diff_y:
            expected_size = sum(range(0, diff_x + 1))
        # isosceles triangle
        elif top_lft['y'] < btm_lft['y'] or btm_rgt['y'] > top_lft['y']:
            expected_size = calculate_surface(diff_x, diff_y, -2)

        if expected_size == filled_cells:
            return 'TRIANGLE'

        # Random triangle shape : define a square then remove the area of 3 triangles (4 actually but 1 does not exist)
        covered_area_top_lft = {'x': min(top_lft['x'], top_rgt['x'], btm_lft['x'], btm_rgt['x']),
                                'y': min(top_lft['y'], top_rgt['y'], btm_lft['y'], btm_rgt['y'])}
        covered_area_btm_rgt = {'x': max(top_lft['x'], top_rgt['x'], btm_lft['x'], btm_rgt['x']),
                                'y': max(top_lft['y'], top_rgt['y'], btm_lft['y'], btm_rgt['y'])}

        to_del_area = 0

        # calculate the top left triangle size
        top_lft_width = top_lft['x'] - covered_area_top_lft['x']
        top_lft_height = max(top_lft['y'], btm_lft['y']) - covered_area_top_lft['y']
        to_del_area += calculate_for_shape(top_lft_width, top_lft_height)

        # calculate the top right triangle size
        top_rgt_width = covered_area_btm_rgt['x'] - top_rgt['x']
        top_rgt_height = min(covered_area_btm_rgt['y'], btm_rgt['y']) - covered_area_top_lft['y']
        to_del_area += calculate_for_shape(top_rgt_width, top_rgt_height)

        # calculate the bottom left triangle size
        btm_lft_width = covered_area_btm_rgt['x'] - min(btm_lft['x'], btm_rgt['x'])
        btm_lft_height = covered_area_btm_rgt['y'] - btm_lft['y']
        to_del_area += calculate_for_shape(btm_lft_width, btm_lft_height)

        # calculate the bottom right triangle size
        btm_rgt_width = covered_area_btm_rgt['x'] - btm_rgt['x']
        btm_rgt_height = covered_area_btm_rgt['y'] - btm_rgt['y']
        to_del_area += calculate_for_shape(btm_rgt_width, btm_rgt_height)

        covered_area = (covered_area_btm_rgt['x'] - covered_area_top_lft['x'] + 1) * (covered_area_btm_rgt['y'] -
            covered_area_top_lft['y'] + 1) - to_del_area

        if covered_area == filled_cells:
            return 'TRIANGLE'

    return 'UNKNOWN'


def calculate_step(width, height):
    if width == 0 or height == 0:
        return -1
    step = ceil(max(width, height)/min(width, height))
    return int(step*-1)


def calculate_surface(width, height, step):
    return sum(range(max(width, height), 0, step))


def calculate_for_shape(width, height):
    if width == 0 or height == 0:
        return 0
    step = calculate_step(width, height)
    return calculate_surface(width, height, step)


if __name__ == '__main__':
    files = {
        'circle_even.txt': 'CIRCLE',
        'circle_even_800x600.txt': 'CIRCLE',
        'circle_even_invalid_a.txt': 'UNKNOWN',
        'circle_even_invalid_b.txt': 'UNKNOWN',
        'circle_odd.txt': 'CIRCLE',
        'circle_odd_invalid_a.txt': 'UNKNOWN',
        'circle_odd_invalid_b.txt': 'UNKNOWN',
        'dot.txt': 'DOT',
        'none.txt': 'NONE',
        'random.txt': 'UNKNOWN',
        'rectangle.txt': 'RECTANGLE',
        'rectangle_3d_a.txt': 'RECTANGLE',
        'rectangle_3d_b.txt': 'RECTANGLE',
        'rectangle_3d_c.txt': 'RECTANGLE',
        'square.txt': 'SQUARE',
        'square_invalid.txt': 'UNKNOWN',
        'square_3d.txt': 'SQUARE',
        'triangle_isosceles_a.txt': 'TRIANGLE',
        'triangle_isosceles_b.txt': 'TRIANGLE',
        'triangle_isosceles_c.txt': 'TRIANGLE',
        'triangle_rectangle_a.txt': 'TRIANGLE',
        'triangle_rectangle_b.txt': 'TRIANGLE',
        'triangle_rectangle_c.txt': 'TRIANGLE',
        'triangle_rectangle_d.txt': 'TRIANGLE',
        'triangle_random_a.txt': 'TRIANGLE',
        'triangle_random_b.txt': 'TRIANGLE',
        'triangle_random_c.txt': 'TRIANGLE',
    }
    errors = 0
    for current_file, assertion in files.items():
        f = open('./tests/sample/' + current_file)
        result = get_shape_name(f.readlines(), 'X')
        if assertion != result:
            errors += 1
            print "KO for %s (expected %s - got %s)" % (current_file, assertion, result)
        f.close()
    print "%d/%d failing tests" % (errors, len(files))