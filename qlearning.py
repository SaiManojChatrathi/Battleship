import numpy as np
import random

# Constants for board size and ship lengths
BOARD_SIZE = 10
SHIP_LENGTHS = [5, 4, 3, 3, 2]  # Example ship lengths, customize as needed

# Define symbols for board representation
EMPTY = '.'
SHIP = 'O'
HIT = 'X'
MISS = '-'

# Initialize player boards
red_board = np.full((BOARD_SIZE, BOARD_SIZE), EMPTY, dtype=str)
blue_board = np.full((BOARD_SIZE, BOARD_SIZE), EMPTY, dtype=str)

def place_ship(board, ship_length):
    # Randomly place a ship of given length on the board
    while True:
        orientation = random.choice(['horizontal', 'vertical'])
        if orientation == 'horizontal':
            x = random.randint(0, BOARD_SIZE - 1)
            y = random.randint(0, BOARD_SIZE - ship_length)
            if all(board[x][y + i] == EMPTY for i in range(ship_length)):
                for i in range(ship_length):
                    board[x][y + i] = SHIP
                break
        else:  # Vertical
            x = random.randint(0, BOARD_SIZE - ship_length)
            y = random.randint(0, BOARD_SIZE - 1)
            if all(board[x + i][y] == EMPTY for i in range(ship_length)):
                for i in range(ship_length):
                    board[x + i][y] = SHIP
                break

def user_make_move(board):
    # Function to accept user input for move
    while True:
        try:
            x = int(input("Enter row (0-9): "))
            y = int(input("Enter column (0-9): "))
            if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                return x, y
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def ai_make_move(board):
    # AI makes a random move and marks it as a hit if it's on an occupied coordinate
    while True:
        x = random.randint(0, BOARD_SIZE - 1)
        y = random.randint(0, BOARD_SIZE - 1)

        if red_board[x][y] == SHIP:
            if red_board[x][y] == HIT:  # Check if the coordinate was already hit on Red board
                continue  # If yes, try again
            else:
                red_board[x][y] = HIT  # Mark as hit on Red board
                print("AI (Blue) hit a ship at:", (x, y))
                return x, y  # Return the hit coordinate
        elif red_board[x][y] == EMPTY:
            red_board[x][y] = MISS
            print("AI (Blue) missed at:", (x, y))
            return x, y  # Return the missed coordinate

    
# Function to display both player boards
def display_boards(red_board, blue_board):
    print("\nRed player's board:")
    print("   " + " ".join(str(i) for i in range(BOARD_SIZE)))
    for i in range(BOARD_SIZE):
        row = str(i) + " |" + "|".join(red_board[i]) + "|"
        print(row)

    print("\nBlue player's board:")
    print("   " + " ".join(str(i) for i in range(BOARD_SIZE)))
    for i in range(BOARD_SIZE):
        row = str(i) + " |" + "|".join(blue_board[i]) + "|"
        print(row)

# Initialize Q-values for AI
q_values = np.zeros((BOARD_SIZE, BOARD_SIZE))

# Main game loop
epsilon = 0.1  # Exploration vs. exploitation parameter
learning_rate = 0.1
discount_factor = 0.9

for episode in range(1000):  # Number of training episodes
    # Place ships for Red player
    for length in SHIP_LENGTHS:
        place_ship(red_board, length)

    # Place ships for Blue player (AI)
    for length in SHIP_LENGTHS:
        place_ship(blue_board, length)

    while True:
        display_boards(red_board, blue_board)  # Show the current state of the boards

        # Red player makes a move
        print("\nYour turn (Red player):")
        red_x, red_y = user_make_move(blue_board)
        if blue_board[red_x][red_y] == SHIP:
            print("Red hit a ship at:", (red_x, red_y))
            blue_board[red_x][red_y] = HIT
        elif blue_board[red_x][red_y] == EMPTY:
            print("Red missed at:", (red_x, red_y))
            blue_board[red_x][red_y] = MISS
        else:
            print("Invalid move. You've already hit this position.")

        # Check if Blue player's ships are all sunk
        if not any(SHIP in row for row in blue_board):
            display_boards(red_board, blue_board)
            print("\nRed wins! All Blue's ships sunk.")
            break

        # AI (Blue) makes a move based on Q-learning
        print("\nAI's turn (Blue player):")
        ai_x, ai_y = ai_make_move(blue_board)  # Corrected call with only the board argument
        if red_board[ai_x][ai_y] == SHIP:
            print("AI (Blue) hit a ship at:", (ai_x, ai_y))
            red_board[ai_x][ai_y] = HIT
        elif red_board[ai_x][ai_y] == EMPTY:
            print("AI (Blue) missed at:", (ai_x, ai_y))
            red_board[ai_x][ai_y] = MISS
        else:
            continue  # Skip printing any message for invalid moves

        # Check if Red player's ships are all sunk
        if not any(SHIP in row for row in red_board):
            display_boards(red_board, blue_board)
            print("\nAI (Blue) wins! All Red's ships sunk.")
            break

        # Check if Red player's ships are all sunk
        elif not any(SHIP in row for row in blue_board):
            display_boards(red_board, blue_board)
            print("\nHuman (Red) wins! All AI's ships sunk.")
            break