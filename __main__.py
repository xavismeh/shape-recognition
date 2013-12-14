from math import sqrt, floor


def get_shape_name(input_values, filling_symbol):
    min_x = min_y = float('inf')
    max_x = max_y = -1
    filled_cells = 0
    top_lft = {'x': float('inf'), 'y': float('inf')}
    top_rgt = {'x': -1, 'y': float('inf')}
    btm_lft = {'x': float('inf'), 'y': -1}
    btm_rgt = {'x': -1, 'y': -1}
    y = 0

    for row in input_values:
        for x in range(len(row)):
            if filling_symbol == row[x]:
                min_x, min_y = min(min_x, x), min(min_y, y)
                max_x, max_y = max(max_x, x), max(max_y, y)
                filled_cells += 1

                if y == min(y, top_lft['y']) and x == min(x, top_lft['x']):
                    top_lft = {'x': min(x, top_lft['x']), 'y': min(y, top_lft['y'])}
                if y <= top_rgt['y']:
                    top_rgt = {'x': max(x, top_rgt['x']), 'y': min(y, top_rgt['y'])}
                if x <= btm_lft['x']:
                    btm_lft = {'x': min(x, btm_lft['x']), 'y': max(y, btm_lft['y'])}
                if y >= btm_rgt['y']:
                    btm_rgt = {'x': x, 'y': y}
        y += 1

    top_width = top_rgt['x'] - top_lft['x'] + 1
    btm_width = btm_rgt['x'] - btm_lft['x'] + 1
    lft_height = btm_lft['y'] - top_lft['y'] + 1
    rgt_height = btm_rgt['y'] - top_rgt['y'] + 1

    # Nothing found
    if 0 == filled_cells:
        return 'NONE'

    # A single dot has been found
    if 1 == filled_cells:
        return 'DOT'

    # The shape is perfectly filled so it can be either a square or a rectangle
    if filled_cells == top_width*lft_height:
        if top_width == btm_width == lft_height == rgt_height:
            return 'SQUARE'

        return 'RECTANGLE'

    # The shape might be a perfect circle
    diff_x = max_x - min_x + 1
    diff_y = max_y - min_y + 1
    is_centered = (max_x + btm_lft['x'])/2 == top_lft['x']

    if (diff_x == diff_y or (diff_y == diff_x + 1 or diff_x == diff_y + 1)) and is_centered:
        expected_size = sum(range(diff_x - 2, 0, -2))*2 + diff_x
        if expected_size == filled_cells:
            return 'CIRCLE'

    # A triangle maybe ?
    if top_lft == top_rgt or top_lft == btm_lft:
        expected_size = -1

        # equilateral triangle
        if diff_x == diff_y:
            expected_size = sum(range(0, diff_x + 1))
        # isosceles triangle
        elif top_lft['y'] < btm_lft['y'] or btm_rgt['y'] > top_lft['y']:
            expected_size = sum(range(diff_x, 0, -2))

        # random triangle
        #if (top_lft == top_rgt and btm_rgt != top_lft) or (top_lft == btm_lft and top_lft != btm_lft):
        #    print top_lft, top_rgt, btm_lft, btm_rgt
        #    print diff_x, diff_y

        if filled_cells == expected_size:
            return 'TRIANGLE'

    return 'UNKNOWN'


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
        'triangle_a.txt': 'TRIANGLE',
        'triangle_b.txt': 'TRIANGLE',
        'triangle_c.txt': 'TRIANGLE',
        'triangle_d.txt': 'TRIANGLE'
    }

    for current_file, assertion in files.items():
        f = open('./tests/sample/' + current_file)
        result = get_shape_name(f.readlines(), 'X')
        if assertion != result:
            print "KO for %s (expected %s - got %s)" % (current_file, assertion, result)
        f.close()