"""This module implements a Diagonal Sudoku solving algorithm
    using the elimination, only_choice, naked_twins and search strategies.
 """
ROWS = 'ABCDEFGHI'
COLS = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

boxes = cross(ROWS, COLS)
row_units = [cross(r, COLS) for r in ROWS]
column_units = [cross(ROWS, c) for c in COLS]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

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
    """
    # if there are no naked twins in the unit nothing to do
    if len(naked_twins) == 0:
        return values

    for naked_twin in naked_twins:
        values = eliminate_naked_twin(values, unit, naked_twin)

    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

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
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in ROWS:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in COLS))
        if r in 'CF': print(line)
    print

def only_choice(values):
    pass

def reduce_puzzle(values):
    pass

def solve(grid):
    return grid

def search(values):
    pass

diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
display(solve(grid_values(diag_sudoku_grid)))

try:
    from visualize import visualize_assignments
    visualize_assignments(assignments)
except:
    print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
