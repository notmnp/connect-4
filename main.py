""" Name: Milan Pattni
Date: July 18th, 2022
Description: Design and implement a (text based) Connect Four 
game in Python where a human player plays against the computer.
"""

import random
import time

# VERSION 8.2
# notes: condensed the almost_won function, and combined the prevent_three and smart_move functions
# additional: added comments and docstrings


def display_board(board, rownum, colnum):

    """ purpose: display the board in a visually appealing format - taking into account the number of rows and columns
    parameters: the nested board lists, the number of rows, and the number of columns
    return values: none
    """

    print()
    # print board according to selected number of rows and columns
    for i in range(1, colnum+1):
        print("  " + str(i), end=" ")
    print("\n")
    for rows in range(1, rownum + 1):
        print("│", end=" ")
        for columns in range(1, colnum + 1):
            print(board[rows][columns], end=" │ ")
        if rows != rownum: 
            print("\n├───┼" + "───┼" * (colnum-2) + "───┤")
        else:
            print("\n└───┴" + "───┴" * (colnum-2) + "───┘")
    print()


def make_user_move(board, rownum, colnum):

    """ purpose: ask the user for their next move, being what column they want to choose
    parameters: nested board lists, number of rows, number of columns
    return values: none
    """

    valid_move = False
    rowcount = 0
    # have user select a column in a set range, if column doesn't exist or is full: have them try again
    while not valid_move:
        col = input("What column would you like to move to (1-" + str(colnum) + "): ")
        try:
            if 1 <= int(col) <= colnum:
                for row in range(rownum, 0, -1):
                    rowcount += 1
                    if board[row][int(col)] == " ":
                        board[row][int(col)] = 'X'
                        valid_move = True
                        break
                    elif rowcount == rownum:
                        print("This column is full. Please try again!\n")
            else:
                print("Sorry, invalid column. Please try again!\n")
        except ValueError:
            print("Please enter a number.\n")


def make_computer_move(board, rownum, colnum):

    """ purpose: automated computer decision regarding what column to play, considering all possible scenarios
    parameters: nested board lists, number of rows, number of columns
    return values: none
    """

    valid_move = False
    rowcount = 0
    # prioritize almost won scenario - computer will always get 4 in a row, or block 3 first, if possible
    if almost_won(board, rownum, colnum):
        try:
            row, column = almost_won(board, rownum, colnum)
            print("I Chose Column", column)
            print("Almost Won Algorithm")
            board[row][column] = 'O'
        except ValueError:
            pass
    # if there is no 3 in a row scenarios, computer will either block 2 in a row, or get 3 in a row, if possible
    elif prevent_three(board, rownum, colnum):
        try:
            row, column, letter = prevent_three(board, rownum, colnum)
            print("I Chose Column", column)
            if letter == "X":
                print("Prevent Three Algorithm")
            elif letter == "O":
                print("Smart Move Algorithm")
            board[row][column] = 'O'
        except ValueError:
            pass
    # if there are no algorithmic moves possible, computer will select a random column, if full, will select another
    else:
        random_count = 1
        while not valid_move:
            col = random.randrange(1, colnum + 1)
            for row in range(rownum, 0, -1):
                rowcount += 1
                if board[row][col] == " ":
                    board[row][col] = 'O'
                    # if selecting a column randomly leads to an almost won scenario (either way), will select again
                    # computer will only select the column (almost win scenario) if it's the only column left
                    if not almost_won(board, rownum, colnum) or (random_count > 6):
                        print("I Chose Column", col)
                        print("Random Move Algorithm")
                        valid_move = True
                        break
                    else:
                        board[row][col] = " "
                        random_count += 1
                        valid_move = False
                        break
                elif rowcount == rownum:
                    pass


def almost_won(board, rownum, colnum):

    """ purpose: scans the board for all possible 4 in a row situations, allowing the computer to make an educated move
    parameters: nested board lists, number of rows, number of columns
    return values: a place on the board (row and column)
    """

    # check for O's first, then X's (prioritize computer win rather than user block)
    for iteration in range(2):
        if iteration == 0:
            letter = "O"
        elif iteration == 1:
            letter = "X"
        # check the rows for 3 in a row, or any space between 4 in a row
        for row in range(1, rownum + 1):
            for column in range(1, colnum - 2):
                if (board[row][column] == board[row][column + 1] == board[row][column + 2] == letter) and (board[row][column + 3] == " ") and (row == rownum or board[row + 1][column + 3] != " "):
                    return row, column + 3
                elif (board[row][column] == board[row][column + 1] == board[row][column + 3]) and (board[row][column] == letter) and (board[row][column + 2] == " ") and (row == rownum or board[row + 1][column + 2] != " "):
                    return row, column + 2
            for column in range(colnum, 3, -1):
                if (board[row][column] == board[row][column - 1] == board[row][column - 2] == letter) and (board[row][column - 3] == " ") and (row == rownum or board[row + 1][column - 3] != " "):
                    return row, column - 3
                elif (board[row][column] == board[row][column - 1] == board[row][column - 3] == letter) and (board[row][column - 2] == " ") and (row == rownum or board[row + 1][column - 2] != " "):
                    return row, column - 2
        # check the columns for 3 in a row
        for column in range(1, colnum + 1):
            for row in range(rownum, 3, -1):
                if (board[row][column] == board[row - 1][column] == board[row - 2][column] == letter) and (board[row - 3][column] == " "):
                    return row - 3, column
        # check diagonal left and right upwards for 3 in a row, or any space between 4 in a row
        for row in range(rownum, 3, -1):
            for column in range(1, colnum - 2):
                if (board[row][column] == board[row - 1][column + 1] == board[row - 2][column + 2] == letter) and (board[row - 3][column + 3] == " ") and (board[row - 2][column + 3] != " "):
                    return row - 3, column + 3
                elif (board[row][column] == board[row - 1][column + 1] == board[row - 3][column + 3] == letter) and (board[row - 2][column + 2] == " ") and (board[row - 1][column + 2] != " "):
                    return row - 2, column + 2
            for column in range(colnum, 3, -1):
                if (board[row][column] == board[row - 1][column - 1] == board[row - 2][column - 2] == letter) and (board[row - 3][column - 3] == " ") and (board[row - 2][column - 3] != " "):
                    return row - 3, column - 3
                elif (board[row][column] == board[row - 1][column - 1] == board[row - 3][column - 3] == letter) and (board[row - 2][column - 2] == " ") and (board[row - 1][column - 2] != " "):
                    return row - 2, column - 2
        # check diagonal left and right downwards for 3 in a row, or any space between 4 in a row
        for row in range(1, rownum - 2):
            for column in range(1, colnum - 2):
                if (board[row][column] == board[row + 1][column + 1] == board[row + 2][column + 2] == letter) and (board[row + 3][column + 3] == " ") and (row == rownum - 3 or board[row + 4][column + 3] != " "):
                    return row + 3, column + 3
                elif (board[row][column] == board[row + 1][column + 1] == board[row + 3][column + 3] == letter) and (board[row + 2][column + 2] == " ") and (board[row + 1][column + 2] != " "):
                    return row + 2, column + 2
            for column in range(colnum, 3, -1):
                if (board[row][column] == board[row + 1][column - 1] == board[row + 2][column - 2] == letter) and (board[row + 3][column - 3] == " ") and (row == rownum - 3 or board[row + 4][column - 3] != " "):
                    return row + 3, column - 3
                elif (board[row][column] == board[row + 1][column - 1] == board[row + 3][column - 3] == letter) and (board[row + 2][column - 2] == " ") and (board[row + 1][column - 2] != " "):
                    return row + 2, column - 2


def prevent_three(board, rownum, colnum):

    """ purpose: scans the board for possible 3 in a row scenarios, allowing the computer to make an educated move
    parameters: nested board lists, number of rows, number of columns
    return values: a place on the board (row and column)
    """

    # Check X's first, then O's (prioritize user block, rather than smart move)
    for iteration in range(2):
        if iteration == 0:
            letter = "X"
            opposite = "O"
        elif iteration == 1:
            letter = "O"
            opposite = "X"
        # check the rows for 2 in a row
        for row in range(1, rownum + 1):
            for column in range(1, colnum - 2):
                if (board[row][column] == board[row][column + 1] == letter) and (board[row][column + 2] == " ") and (row == rownum or board[row + 1][column + 2] != " ") and (board[row][column + 3] != opposite):
                    return row, column + 2, letter
                elif (board[row][column] == board[row][column + 2] == letter) and (board[row][column + 1] == " ") and (row == rownum or board[row + 1][column + 1] != " ") and (board[row][column + 3] != opposite):
                    return row, column + 1, letter
            for column in range(colnum, 3, -1):
                if (board[row][column] == board[row][column - 1] == letter) and (board[row][column - 2] == " ") and (row == rownum or board[row + 1][column - 2] != " ") and (board[row][column - 3] != opposite):
                    return row, column - 2, letter
                elif (board[row][column] == board[row][column - 2] == letter) and (board[row][column - 1] == " ") and (row == rownum or board[row + 1][column - 1] != " ") and (board[row][column - 3] != opposite):
                    return row, column - 1, letter
        # check diagonal left and right upwards for 2 in a row
        for row in range(rownum, 3, -1):
            for column in range(1, colnum - 2):
                if (board[row][column] == board[row - 1][column + 1] == letter) and (board[row - 2][column + 2] == " ") and (board[row - 1][column + 2] != " "):
                    return row - 2, column + 2, letter
                elif (board[row][column] == board[row - 2][column + 2] == letter) and (board[row - 1][column + 1] == " ") and (board[row][column + 1] != " "):
                    return row - 1, column + 1, letter
            for column in range(colnum, 3, -1):
                if (board[row][column] == board[row - 1][column - 1] == letter) and (board[row - 2][column - 2] == " ") and (board[row - 1][column - 2] != " "):
                    return row - 2, column - 2, letter
                elif (board[row][column] == board[row - 2][column - 2] == letter) and (board[row - 1][column - 1] == " ") and (board[row][column - 1] != " "):
                    return row - 1, column - 1, letter
        # check diagonal left and right downwards for 2 in a row
        for row in range(1, rownum - 2):
            for column in range(1, colnum - 1):
                if (board[row][column] == board[row + 1][column + 1]  == letter) and (board[row + 2][column + 2] == " ") and (row == rownum - 2 or board[row + 3][column + 2] != " "):
                    return row + 2, column + 2, letter
                elif (board[row][column] == board[row + 2][column + 2] == letter) and (board[row + 1][column + 1] == " ") and (board[row + 2][column + 1] != " "):
                    return row + 1, column + 1, letter
            for column in range(colnum, 3, -1):
                if (board[row][column] == board[row + 1][column - 1] == letter) and (board[row + 2][column - 2] == " ") and (row == rownum - 2 or board[row + 3][column - 2] != " "):
                    return row + 2, column - 2, letter
                elif (board[row][column] == board[row + 2][column - 2] == letter) and (board[row + 1][column - 1] == " ") and (board[row + 2][column - 1] != " "):
                    return row + 1, column - 1, letter
        # check the columns for 2 in a row
        for column in range(1, colnum + 1):
            for row in range(rownum, 3, -1):
                if (board[row][column] == board[row - 1][column] == letter) and (board[row - 2][column] == " "):
                    return row - 2, column, letter


def winner(board, rownum, colnum):

    """ purpose: checks the board for 4 identical pieces in a row
    parameters: nested board lists, number of rows, number of columns
    return values: the value of the winning 4 in a row piece (X or O)
    """

    # check rows for winner
    for row in range(1, rownum + 1):
        for columns in range(1, colnum - 2):
            if (board[row][columns] == board[row][columns + 1] == board[row][columns + 2] == board[row][columns + 3]) and (board[row][columns] != " "):
                return board[row][columns]
    # check columns for winner
    for column in range(1, colnum + 1):
        for row in range(rownum, 3, -1):
            if (board[row][column] == board[row - 1][column] == board[row - 2][column] == board[row - 3][column]) and (board[row][column] != " "):
                return board[row][column]
    # check diagonal right for winner
    for row in range(rownum, 3, -1):
        for column in range(1, colnum - 2):
            if (board[row][column] == board[row - 1][column + 1] == board[row - 2][column + 2] == board[row - 3][column + 3]) and (board[row][column] != " "):
                return board[row][column]
    # check diagonal left for winner
    for row in range(rownum, 3, -1):
        for column in range(colnum, 3, -1):
            if (board[row][column] == board[row - 1][column - 1] == board[row - 2][column - 2] == board[row - 3][column - 3]) and (board[row][column] != " "):
                return board[row][column]


def prev_winners():

    """ purpose: checks the HallOfFame text file for any text, if it exists, displays the previous winners
    parameters: none
    return values: none
    """

    hof = open("HallOfFame.txt", "r")
    hof_contents = hof.read()
    hof.close()
    name_count = 1
    # check if HallOfFame.txt has any winners, if so: list them, if not: print message
    if hof_contents:
        hof = open("HallOfFame.txt", "r")
        print("PREVIOUS WINNERS: ")
        for line in hof:
            print(str(name_count) + ".", line.strip())
            name_count += 1
        hof.close()
    else:
        print("No Human Has Ever Beat Me.. mwah-ha-ha-ha!")


def game_size():

    """ purpose: asks the user how many rows and columns the board should include
    parameters: none
    return values: number of rows, number of columns
    """

    valid_rows = False
    valid_cols = False
    # ask user to input how many rows + columns they would like the board to be (includes exception handling)
    while not valid_rows:
        rownum = input("How many rows should the board have (5-7)? ")
        try:
            while (int(rownum) < 5) or (int(rownum) > 7):
                rownum = input("Invalid response. How many rows should the board have (5-7)? ")
            rownum = int(rownum)
            valid_rows = True
        except ValueError:
            print("Please enter a number. ")
    while not valid_cols:
        colnum = input("How many columns should the board have (6-8)? ")
        try:
            while (int(colnum) < 6) or (int(colnum) > 8):
                colnum = input("Invalid response. How many columns should the board have (6-8)? ")
            colnum = int(colnum)
            valid_cols = True
        except ValueError:
            print("Please enter a number. ")
    return rownum, colnum


def game_results(board, rownum, colnum):

    """ purpose: displays a suitable message based on whether there is a winner, loser or stalemate
    parameters: nested board lists, number of rows, number of columns
    return values: none
    """

    # checks the board for a user win, computer win, or a stalemate and displays an appropriate message
    if winner(board, rownum, colnum) == 'X':
        # if user wins, add their name to the HallOfFame.txt file
        print("YOU WON!")
        winner_name = input("What is your name (for the record)? ")
        print("Thank You. ")
        hof = open("HallOfFame.txt", "a")
        hof.write(winner_name + "\n")
    elif winner(board, rownum, colnum) == 'O':
        print("THE COMPUTER WON!")
    else:
        print("STALEMATE...")
    print("\nTHE GAME HAS ENDED\n")


def who_starts():

    """ purpose: asks the user if they would like to make the first move, or let the computer
    parameters: none
    return values: whether the user starts or not (users_turn = True or False)
    """

    # ask user if they would like to make the first move, using exception handling
    start = input("Would you like to go first (y/n)? ")
    while start not in ["y", "Y", "n", "N"]:
        start = input("Invalid response. Would you like to go first (y/n)? ")
    if start in ["y", "Y"]:
        users_turn = True
    elif start in ["n", "N"]:
        users_turn = False
    return users_turn


def main():

    """ purpose: function that combines and orders all other functions in an organized manner
    parameters: none
    return values: none
    """

    prev_winners()
    rownum, colnum = game_size()
    free_cells = rownum * colnum
    users_turn = who_starts()
    # the following list is what the display_board function uses (each item in each nested list is a board square)
    # each nested list represents a row, and each item in the lists are the specific column.
    cf_board = [[" ", " ", " ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "]]
    # while there is no winner, or the board is not full, the game continues
    while not winner(cf_board, rownum, colnum) and (free_cells > 0):
        display_board(cf_board, rownum, colnum)
        if users_turn:
            make_user_move(cf_board, rownum, colnum)
            users_turn = False
        else:
            # add 1-second delay before computer moves.
            time.sleep(1)
            make_computer_move(cf_board, rownum, colnum)
            users_turn = True
        free_cells -= 1
    display_board(cf_board, rownum, colnum)
    game_results(cf_board, rownum, colnum)


# run the main function
main()
