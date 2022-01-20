# Sudoku
The repository contains a solver to game sudoku.

## Backgroud about sudoku:
Quoted from Wikipedia page: "In classic sudoku, the objective is to fill a 9 × 9 grid with digits so that each column, each row, and each of the nine 3 × 3 subgrids that compose the grid (also called "boxes", "blocks", or "regions") contain all of the digits from 1 to 9. The puzzle setter provides a partially completed grid, which for a well-posed puzzle has a single solution."
For details, check the [link](https://en.wikipedia.org/wiki/Sudoku).

## Input format of this solver:
Sudoku is stored as a list of tuples. The first two numbers are the row and column coordinates of a non-empty cell, while the last number is the number contained in the cell.

## Rules used:
We update all the possible numbers for each cell after filling in a new number. If no more updates can be done, we choose a number to fill in a cell and repeat the update-choice process multiple times until the sudoku is done or some contradiction comes up. The latter situation implies that the last choice is wrong. Then we redo the last choice, pick a different number for the chosen cell and repeat the process again.
For details, check the file:sudoku.py 

## Future work:
1. This file only contains a sudoku solver. It does not generate sudoku in the first place. We plan to add a sudoku generator.
2. We would like to make the input of sudoku more direct and more interactive. The user can directly fill numbers into cells on a $9 * 9$ grid via keyboard.
