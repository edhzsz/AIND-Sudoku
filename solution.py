# pylint: disable=C0103
"""This module implements a Diagonal Sudoku solving algorithm
    using the elimination, only_choice, naked_twins and search strategies.
 """
ROWS = 'ABCDEFGHI'
COLS = '123456789'
DIGITS = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

boxes = cross(ROWS, COLS)
row_units = [cross(r, COLS) for r in ROWS]
column_units = [cross(ROWS, c) for c in COLS]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = [[a+b for a, b in zip(ROWS, COLS)], [a+b for a, b in zip(ROWS, COLS[::-1])]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def find_naked_twins(values, unit):
    """
    Find all instances of naked twins in the unit
    Args:
        values(dict): A sudoku in a dictionary of the form {'box_name': '123456789', ...}
        unit(list): a list of boxes that belong to a unit

    Returns:
        a list of values that appear exactly in two boxes in the unit
    """
    # find all boxes in the unit that have only two possible values
    boxes_with_pairs = [b for b in unit if len(values[b]) == 2]

    # list the boxes for each pair
    pairs = {}
    for box_pair in boxes_with_pairs:
        value = values[box_pair]
        pairs[value] = pairs.get(value, [])
        pairs[value].append(box_pair)

    # return the pairs that exist in exactly two boxes
    return [pairs[p] for p in pairs.keys() if len(pairs[p]) == 2]

def eliminate_naked_twin(values, unit, naked_twin):
    """
    Eliminate a single naked twin as possibilities for the peers in the unit
    Args:
        values(dict): A sudoku in a dictionary of the form {'box_name': '123456789', ...}
        unit(list): a list of boxes that belong to a unit
        naked_twin(list): pair of boxes in the unit with the same value

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    val = values[naked_twin[0]]

    # for each box in the unit that does not belong to the naked twins
    for box in set(unit) - set(naked_twin):
        for d in val:
            assign_value(values, box, values[box].replace(d, ""))

    return values

def eliminate_naked_twins(values, unit, naked_twins):
    """
    Eliminate all the naked twins as possibilities for their peers in the unit
    Args:
        values(dict): A sudoku in a dictionary of the form {'box_name': '123456789', ...}
        unit(list): a list of boxes that belong to a unit
        naked_twins(list): list of pairs of boxes in the unit with the same value

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # if there are no naked twins in the unit nothing to do
    if len(naked_twins) == 0:
        return values

    for naked_twin in naked_twins:
        values = eliminate_naked_twin(values, unit, naked_twin)

    return values

def naked_twins(values):
    """
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): A sudoku in a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # calculate the naked twins in all the units
    naked_twins_units = [(unit, find_naked_twins(values, unit)) for unit in unitlist]

    for naked_twin_unit in naked_twins_units:
        unit, naked_twins = naked_twin_unit
        values = eliminate_naked_twins(values, unit, naked_twins)

    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
                then the value will be '123456789'.
    """
    chars = []
    for c in grid:
        if c in DIGITS:
            chars.append(c)
        if c == '.':
            chars.append(DIGITS)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): A sudoku in a dictionary of the form {'box_name': '123456789', ...}
    Output: None
    """
    if values is False:
        return

    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in ROWS:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in COLS))
        if r in 'CF':
            print(line)
    print

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value,
        eliminate this value from the values of all its peers.
    Args:
        values(dict): A sudoku in a dictionary of the form {'box_name': '123456789', ...}
    Output: The resulting sudoku in dictionary form.
    """
    solved_boxes = [b for b in boxes if len(values[b]) == 1]

    for box in solved_boxes:
        value = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(value, ""))

    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that
        only fits in one box, assign the value to this box.
    Args:
        values(dict): A sudoku in a dictionary of the form {'box_name': '123456789', ...}
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in DIGITS:
            dcount = [b for b in unit if digit in values[b]]
            if len(dcount) == 1:
                assign_value(values, dcount[0], digit)

    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with
        no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Args:
        values(dict): A sudoku in a dictionary of the form {'box_name': '123456789', ...}
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate
        values = eliminate(values)

        # Use the Only Choice Strategy
        values = only_choice(values)

        # Use the Naked Twins Strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid. Example:
        '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    return search(grid_values(grid))

def search(values):
    """
    Using depth-first search and propagation, try all possible values.
    Args:
        values(dict): A sudoku in a dictionary of the form {'box_name': '123456789', ...}
    Output: The resulting sudoku in dictionary form.
    """
     # First, reduce the puzzle
    values = reduce_puzzle(values)

    if values is False:
        return False ## Found an inconsistency. Fail

    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!

    # Chose one of the unfilled square s with the fewest possibilities
    length, min_box = min([(len(values[b]), b) for b in boxes if len(values[b]) > 1])

    # Now use recursion to solve each one of the resulting sudokus
    for digit in values[min_box]:
        new_vals = values.copy()
        assign_value(new_vals, min_box, digit)
        attempt = search(new_vals)

        if attempt:
            return attempt

    return False

if __name__ == '__main__':
    diag_sudoku_grid = ('2.............62....1....7.'
                        '..6..8...3...9...7...6..4..'
                        '.4....8....52.............3')

    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print ('We could not visualize your board due to a pygame issue. ' +
               'Not a problem! It is not a requirement.')
