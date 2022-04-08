"""
Purpose:    Solve the longest substring problem 
Filename:   longest_substring.py
Author:     Siddharth Kapoor   
Date:       April 28, 2020

                            SUDOKU SOLVER

Write a program to solve a Sudoku puzzle by filling the empty cells.

A sudoku solution must satisfy all of the following rules:

Each of the digits 1-9 must occur exactly once in each row.
Each of the digits 1-9 must occur exactly once in each column.
Each of the the digits 1-9 must occur exactly once in each of the 9 3x3 
sub-boxes of the grid.
Empty cells are indicated by the character '.'.

Note:

The given board contain only digits 1-9 and the character '.'.
You may assume that the given Sudoku puzzle will have a single unique solution.
The given board size is always 9x9.

IMPLEMENTATION ANALYSIS
    On leetcode.com
    Runtime: 292 ms, faster than 49.92% of Python3 online submissions for 
    Sudoku Solver.
    Memory Usage: 14 MB, less than 10.71% of Python3 online submissions for 
    Sudoku Solver.

    Iteration is expected to be faster than recursion, however the solution is
    quite verbose. 
    
    There is also a lot of extra book keeping like recording the
    direction of iteration, and a lot of mathematical and comparitive operations
    to calculate the next and previous cells. This could have been elimiated by
    using the stack of pre-recorded moves.

    It is possible that we could have optimised for space and also time by using
    default dict as per the leetcode implementation.

    Aditionally recursion might cost more space, but might reduce overall 
    computation and therefore be faster.

    Setting the value of row to -1 to indicate we have solved the sudoku seems 
    inelegant and confusing for readers as well. A condition that check for 
    the first and last cell might be more intuitively understood. However,
    this is a great example of how recursion is generally more elegant and
    readable.

    Finally, filling out all necessary cells before starting the puzzle might
    improve performance considerably.

    SUMMARY OF POSSIBLE IMPROVEMENTS
    1. Using move stack to reverse direction, instead of prev_cell() function
    2. Using default dict instead of {}
    3. Using recursion

"""


def solveSudoku(board):
    """
    :type board: List[List[str]]
    :rtype: None Do not return anything, modify board in-place instead.
    """

    """
    Algorithm
    rows, cols, boxes = [{} for i in range(9)]

    1. Iterate over all the cells row by row
    2. When you find an empty cell, fill it with the 
        lowest possible valid number
    3. if no valid move is possible, backtrack to the previous
        cell
        - fill it with the next highest valid number
        - if no move is possible, repeat step 3
    4. When you reach the last cell, the puzzle is solved

    """
    class ImpossibleSudoku(Exception):
        pass

    def is_valid(r, c, n):
        if not (n in rows[r] or n in cols[c] or n in boxes[(r//3)*3 + (c//3)]):
            return True
        return False

    def next_valid_move(r, c):
        """
        given the state of the board, find the smallest
        valid number for boxes[r][c]
        if the box has a number in it, then the next valid move should be 
        """
        current_value = 0
        if board[r][c] != '.':
                current_value = int(board[r][c])
        for i in range(current_value + 1, 10):
            if is_valid(r, c, i):
                return i
        return -1

    def place_num(r, c, n):
        board[r][c] = str(n)
        rows[r][n] = 1
        cols[c][n] = 1
        boxes[(r//3)*3 + (c//3)][n] = 1

    def remove_num(r, c, n):
        board[r][c] = '.'
        del rows[r][n]
        del cols[c][n]
        del boxes[(r//3)*3 + (c//3)][n]

    def prev_cell(r, c):
        c -= 1
        if c < 0:
            c = 8
            r -= 1
        if r < 0:
            r, c = -2, -2
        return (r, c)

    def next_cell(r, c):
        c += 1
        if c > 8:
            c = 0
            r += 1
        if r > 8: 
            r, c = -1, -1
        return (r, c)
    
    def print_board():
        print(rows)
        print(moves)
        for row in board:
            print(row)
        print('')

    def solve():
        r, c, i = 0, 0, 0
        solved = False
        backtracking = False

        while not solved:
            #print_board()

            # check if we have reached the end of the board
            if r == -1:
                solved = True
            # check if there is no solution
            if r == -2:
                raise ImpossibleSudoku()
                break
            # if filled
            if board[r][c] != '.':
                # non-playable cell
                if (r, c) not in moves:
                    if backtracking:
                        r, c = prev_cell(r, c)
                    else:
                        r, c = next_cell(r, c)
                # playable cell - we have back tracked
                else:
                    next_move = next_valid_move(r, c)
                    # there is no valid move
                    if next_move == -1:
                        remove_num(r, c, int(board[r][c]))
                        moves.pop()
                        r, c = prev_cell(r, c)
                        backtracking = True
                    # these is a valid move
                    else:
                        remove_num(r, c, int(board[r][c]))
                        place_num(r, c, next_move)
                        r, c = next_cell(r, c)
                        backtracking = False
            # not filled
            else:
                next_move = next_valid_move(r, c)
                # there is a valid move
                if next_move != -1:
                    place_num(r, c, next_move)
                    moves.append((r, c))
                    r, c = next_cell(r, c)
                    backtracking = False
                # no valid move
                else:
                    r, c = prev_cell(r, c)
                    backtracking = True
        print("SOLVED!")


    # fill up rows and cols with starting numbers
    rows = [{} for i in range(9)]
    cols = [{} for i in range(9)]
    boxes = [{} for i in range(9)]
    moves = []

    for r in range(9):
        for c in range(9):
            num = board[r][c]
            if num != '.':
                num = int(num)
                rows[r][num] = 1
                cols[c][num] = 1
                boxes[(r//3)*3 + (c//3)][num] = 1

    solve()

board = [["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]]

solveSudoku(board)
print(board)