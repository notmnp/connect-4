import random
import time
import math

# VERSION 10 UPDATE!!!!
# notes: implemented minimax algorith to make this better
# additional: added comments and docstrings

AI_PLAYER = 'O'
HUMAN_PLAYER = 'X'
EMPTY = " "
DEPTH = 4

def display_board(board, rownum, colnum):
    """ display the board in a visually appealing format """
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
    """ ask the user for their next move """
    valid_move = False
    # have user select a column in a set range, if column doesn't exist or is full: have them try again
    while not valid_move:
        col = input("What column would you like to move to (1-" + str(colnum) + "): ")
        try:
            col = int(col)
            if 1 <= col <= colnum:
                for row in range(rownum, 0, -1):
                    if board[row][col] == EMPTY:
                        board[row][col] = HUMAN_PLAYER
                        valid_move = True
                        break
                if not valid_move:
                    print("This column is full. Try again!")
            else:
                print("Invalid column. Try again!")
        except ValueError:
            print("Please enter a number.")

def get_valid_moves(board, rownum, colnum):
    """ returns a list of valid columns where a move can be made """
    return [col for col in range(1, colnum + 1) if board[1][col] == EMPTY]

def evaluate_window(window):
    """ assigns a score to a given window of four spaces """
    score = 0
    if window.count(AI_PLAYER) == 4:
        score += 100
    elif window.count(AI_PLAYER) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(AI_PLAYER) == 2 and window.count(EMPTY) == 2:
        score += 5
    if window.count(HUMAN_PLAYER) == 3 and window.count(EMPTY) == 1:
        score -= 50  # Higher penalty for allowing the human to win
    elif window.count(HUMAN_PLAYER) == 4:
        score -= 100
    return score

def evaluate_board(board, rownum, colnum):
    """ evaluates the board to determine how favourable a move is for the computer """
    score = 0
    # check rows, columns, and diagonals to see if there are possible winning lines
    for row in range(1, rownum + 1):
        for col in range(1, colnum - 2):
            window = [board[row][col + i] for i in range(4) if col + i <= colnum]
            score += evaluate_window(window)
    for col in range(1, colnum + 1):
        for row in range(1, rownum - 2):
            window = [board[row + i][col] for i in range(4) if row + i <= rownum]
            score += evaluate_window(window)
    for row in range(1, rownum - 2):
        for col in range(1, colnum - 2):
            window = [board[row + i][col + i] for i in range(4) if row + i <= rownum and col + i <= colnum]
            score += evaluate_window(window)
    for row in range(4, rownum + 1):
        for col in range(1, colnum - 2):
            window = [board[row - i][col + i] for i in range(4) if row - i > 0 and col + i <= colnum]
            score += evaluate_window(window)
    return score

def minimax(board, depth, alpha, beta, maximizing_player, rownum, colnum):
    """ minimax algorithm with alpha-beta pruning """
    valid_moves = get_valid_moves(board, rownum, colnum)
    is_terminal = winner(board, rownum, colnum) or len(valid_moves) == 0

    if depth == 0 or is_terminal:
        if winner(board, rownum, colnum) == AI_PLAYER:
            return (None, 1000000)
        elif winner(board, rownum, colnum) == HUMAN_PLAYER:
            return (None, -1000000)
        else:
            return (None, evaluate_board(board, rownum, colnum))

    if maximizing_player:
        max_eval = -math.inf
        best_col = random.choice(valid_moves)

        for col in valid_moves:
            row = max([r for r in range(1, rownum + 1) if board[r][col] == EMPTY])
            board[row][col] = AI_PLAYER
            _, score = minimax(board, depth - 1, alpha, beta, False, rownum, colnum)
            board[row][col] = EMPTY

            if score > max_eval:
                max_eval = score
                best_col = col

            alpha = max(alpha, score)
            if beta <= alpha:
                break

        return best_col, max_eval

    else:
        min_eval = math.inf
        best_col = random.choice(valid_moves)

        for col in valid_moves:
            row = max([r for r in range(1, rownum + 1) if board[r][col] == EMPTY])
            board[row][col] = HUMAN_PLAYER
            _, score = minimax(board, depth - 1, alpha, beta, True, rownum, colnum)
            board[row][col] = EMPTY

            if score < min_eval:
                min_eval = score
                best_col = col

            beta = min(beta, score)
            if beta <= alpha:
                break

        return best_col, min_eval

def make_computer_move(board, rownum, colnum):
    """ Uses minimax algorithm to determine the best move for the computer """
    depth = DEPTH  # depth limit for minimax search
    col, _ = minimax(board, depth, -math.inf, math.inf, True, rownum, colnum)

    for row in range(rownum, 0, -1):
        if board[row][col] == EMPTY:
            board[row][col] = AI_PLAYER
            break

    print("I Chose Column", col)

def winner(board, rownum, colnum):
    """ checks the board for 4 identical pieces in a row """
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

def game_size():
    """ asks the user how many rows and columns the board should include """
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
    """ displays a suitable message based on whether there is a winner, loser or stalemate """
    # checks the board for a user win, computer win, or a stalemate and displays an appropriate message
    if winner(board, rownum, colnum) == HUMAN_PLAYER:
        # if user wins, add their name to the HallOfFame.txt file
        print("YOU WON!")
    elif winner(board, rownum, colnum) == AI_PLAYER:
        print("THE COMPUTER WON!")
    else:
        print("STALEMATE...")
    print()


def who_starts():
    """ asks the user if they would like to make the first move, or let the computer """
    start = input("Would you like to go first (y/n)? ")
    while start not in ["y", "Y", "n", "N"]:
        start = input("Invalid response. Would you like to go first (y/n)? ")
    if start in ["y", "Y"]:
        users_turn = True
    elif start in ["n", "N"]:
        users_turn = False
    return users_turn

def main():
    """ main loop with play again option """
    while True:
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

        # ask if the user wants to play again
        play_again = input("Would you like to play again? (y/n): ").strip().lower()
        while play_again not in ['y', 'n']:
            play_again = input("Invalid response. Would you like to play again? (y/n): ").strip().lower()
        
        if play_again == 'n':
            print("Thanks for playing!")
            break 

# run the main function
main()
