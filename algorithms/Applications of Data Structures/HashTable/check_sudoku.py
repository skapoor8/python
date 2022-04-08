"""
Purpose:    Solve the longest substring problem 
Filename:   longest_substring.py
Author:     Siddharth Kapoor   
Date:       April 28, 2020

Determine if a 9x9 Sudoku board is valid. Only the filled cells need to be 
validated according to the following rules:

Each row must contain the digits 1-9 without repetition.
Each column must contain the digits 1-9 without repetition.
Each of the 9 3x3 sub-boxes of the grid must contain the digits 1-9 without 
repetition.

The Sudoku board could be partially filled, where empty cells are filled with 
the character '.'.

Example 1:

Input:
[
  ["5","3",".",".","7",".",".",".","."],
  ["6",".",".","1","9","5",".",".","."],
  [".","9","8",".",".",".",".","6","."],
  ["8",".",".",".","6",".",".",".","3"],
  ["4",".",".","8",".","3",".",".","1"],
  ["7",".",".",".","2",".",".",".","6"],
  [".","6",".",".",".",".","2","8","."],
  [".",".",".","4","1","9",".",".","5"],
  [".",".",".",".","8",".",".","7","9"]
]
Output: true
Example 2:

Input:
[
  ["8","3",".",".","7",".",".",".","."],
  ["6",".",".","1","9","5",".",".","."],
  [".","9","8",".",".",".",".","6","."],
  ["8",".",".",".","6",".",".",".","3"],
  ["4",".",".","8",".","3",".",".","1"],
  ["7",".",".",".","2",".",".",".","6"],
  [".","6",".",".",".",".","2","8","."],
  [".",".",".","4","1","9",".",".","5"],
  [".",".",".",".","8",".",".","7","9"]
]
Output: false
Explanation: Same as Example 1, except with the 5 in the top left corner being 
modified to 8. Since there are two 8's in the top left 3x3 sub-box, it is 
invalid.

Note:

A Sudoku board (partially filled) could be valid but is not necessarily 
solvable. Only the filled cells need to be validated according to the mentioned 
rules. The given board contain only digits 1-9 and the character '.'.
The given board size is always 9x9.

"""


def isValidSudoku(board):
    """
    :type board: List[List[str]]
    :rtype: bool

    ALGORITHM
    1. Let's represent the rows, cols and boxes as an array of 9 maps {}
    2. For every box, sudoku[r][c] = n
        - check if n is in r, c, or box (r//3) + c
        - if yes, then sudoku is  invalid
        - if no, then add n to respective r, c and box
    3. If sudoku has not been invalidated so far, then sudoku is valid

    O(81) -> single pass, constant number of boxes
    """
    # init data
    rows = [{} for i in range(9)]
    columns = [{} for i in range(9)]
    boxes = [{} for i in range(9)]

    # validate a board
    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num != '.':
                num = int(num)
                box_index = (i // 3 ) * 3 + j // 3
                
                # keep the current cell value
                rows[i][num] = rows[i].get(num, 0) + 1
                columns[j][num] = columns[j].get(num, 0) + 1
                boxes[box_index][num] = boxes[box_index].get(num, 0) + 1
                
                # check if this value has been already seen before
                if rows[i][num] > 1 or columns[j][num] > 1 or boxes[box_index][num] > 1:
                    return False         
    return True