# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?
A: Constraint Propagation is used to solve the _naked twins_ problem since the
_naked twins_ algorithm actually creates a constraint in the set of feasible values
for boxes in the same unit of a sudoku board.

We call _naked twins_ to a pair of boxes, in a unit, that have exactly the same set
of feasible values and this set has exactly two elements.

We know that these two values can only be in these two boxes and not in any other
box in the same unit so the constraint enforced by the naked twins algorithm is
such that, for all units, only the boxes that are naked twins contain the twin values.

The algorithm, for each unit, works as follows:

* first we find the boxes where there are only two remaining feasible values
* if there is a pair of different boxes with the exact same set of feasible values (a naked twin) then:
  * we remove these two values from the set of feasible values from the other boxes in the unit that are not the naked twins

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: A _diagonal sudoku_ follows the same rules as the regular sudoku with the addition that
the among the main diagonals the numbers 1 to 9 should appear only once.

In the course lectures we have lernt two strategies to solve a _regular_ sudoku_:
* Constraint propagation using the _only choice_, _single possibility_ and _naked twins_ rules.
* Depth-first search

The constraint propagation strategy works by repeatedly applying a set of constraints
to each _unit_ in the sudoku board. Each of these constraints narrows the set of feasible values
for each of the _boxes_ that belong to the _unit_ until a solution is found (the set of
feasible values for each box contains only one element), a contradiction is found (the set
of feasible values for at least one box is empty), or it is not possible to reduce more the set of
feasible values by this strategy.

The aim of each of these constraints is to aproach to the solution of the board
in which each of the sudoku _units_ (rows, columns and squares) contains once
and only once all of the digits 1 to 9.

It is easy to see that in the _diagonal sudoku_, the diagonals are also _units_ 
and, by including them in the set of units, the constraint propagation strategy will
reduce, on each step, the set of feasible values also for the diagonals aproaching
to the solution of the diagonal sudoku.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.