# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?
A: Constraint Propagation is used to solve the _naked twins_ problem since the
_naked twins_ algorithm actually creates a constraint in the set of possible values
for boxes in the same unit of a sudoku board.

We call _naked twins_ to a pair of boxes, in a unit, that have exactly the same set
of possible values and this set has exactly two elements.

We know that these two values can only be in these two boxes and not in any other
box in the same unit so the constraint enforced by the naked twins algorithm is
such that, for all units, only the boxes that are naked twins contain the twin values.

The algorithm, for each unit, works as follows:

* first we find the boxes where there are only two remaining possible values
* if there is pair of different boxes with the exact same set of possible values (a naked twin) then:
  * we remove these two values from the set of possible values from the other boxes
    in the unit that are not the naked twins

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: By considering the diagonals as _units_ the constraints implented by the strategies are also propagated to the diagonals.

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