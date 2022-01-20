# Sudoku
The repository contains a solver to game sudoku.

## Backgroud about sudoku:
Quoted from Wikipedia page: "In classic sudoku, the objective is to fill a 9 × 9 grid with digits so that each column, each row, and each of the nine 3 × 3 subgrids that compose the grid (also called "boxes", "blocks", or "regions") contain all of the digits from 1 to 9. The puzzle setter provides a partially completed grid, which for a well-posed puzzle has a single solution."
For details, check the [link](https://en.wikipedia.org/wiki/Sudoku).


## Input format of this solver:
A sudoku is stored as a list of tuples, the first two numbers are the row and column coordinate of a nonempty cell and the last number is the number contained in the cell.

## Rules used:
We record all the possible numbers for each cell, and update the numbers, following 3 rules, after a number fills in. If no more is to be updated, we start to make a choice. Pick a cell and a number in this cell and update the possible numbers, and repeat the process until the sudoku is done or there is some contradition. The contradition implies that the last choice to cell A is wrong. Then we choose a different number for cell A and repeat the process.
For details, check the file:sudoku.py 

## Future work:
1. This file only contains a sudoku solver. It doese not generate a sudoku at first place. We would like to add a sudoku generator.
2. We would like to make the input process of a soduku more direct and more interactive. There will be a grid of $9 * 9$, the user can click empty cell can fill in the number via keyboard.
