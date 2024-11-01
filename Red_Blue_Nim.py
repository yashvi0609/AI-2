import sys
import random

# Function to determine the best move for the computer using depth-limited search
def computer_turn(count_pile, game_mode, depth=3):
    best_move = None
    best_score = float('-inf')

    for i in range(2):  # 0 for red, 1 for blue
        for balls_to_remove in [1, 2]:  # Check removing 1 or 2 balls
            if count_pile[i] >= balls_to_remove:
                new_pile = count_pile[:]
                new_pile[i] -= balls_to_remove
                score = minimax(new_pile, depth - 1, False, game_mode)
                
                if score > best_score:
                    best_score = score
                    best_move = (i, balls_to_remove)

    if best_move:
        count_pile[best_move[0]] -= best_move[1]
        print(f"Computer removes {best_move[1]} from {'red' if best_move[0] == 0 else 'blue'} pile.")

# Minimax algorithm with depth limit
def minimax(count_pile, depth, is_maximizing, game_mode):
    if depth == 0 or min(count_pile) == 0:
        return evaluate_position(count_pile, game_mode)

    if is_maximizing:
        best_score = float('-inf')
        for i in range(2):
            for balls_to_remove in [1, 2]:
                if count_pile[i] >= balls_to_remove:
                    new_pile = count_pile[:]
                    new_pile[i] -= balls_to_remove
                    score = minimax(new_pile, depth - 1, False, game_mode)
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(2):
            for balls_to_remove in [1, 2]:
                if count_pile[i] >= balls_to_remove:
                    new_pile = count_pile[:]
                    new_pile[i] -= balls_to_remove
                    score = minimax(new_pile, depth - 1, True, game_mode)
                    best_score = min(best_score, score)
        return best_score

# Function to evaluate the position
def evaluate_position(count_pile, game_mode):
    if game_mode == 'standard':
        return 1 if min(count_pile) == 0 else 0  # Win for computer
    else:  # Misère mode
        return -1 if max(count_pile) == 0 else 0  # Win for human

# Function to handle human's turn input
def human_turn(count_pile):
    while True:
        pile_color = input("Your turn - Choose One (red/blue)->").lower()
        if pile_color in ['red', 'blue']:
            pile_color_num = 0 if pile_color == 'red' else 1
            if count_pile[pile_color_num] <= 0:
                print("No balls left in this pile. Choose another color.")
                continue
            
            balls_to_remove = get_balls_to_remove(count_pile, pile_color_num)
            count_pile[pile_color_num] -= balls_to_remove
            break
        else:
            print("Invalid color. Please choose 'red' or 'blue'.")

# Function to get the number of balls to remove from the human player
def get_balls_to_remove(count_pile, pile_color_num):
    while True:
        try:
            balls_to_remove = int(input("Choose number of balls to remove (1 or 2)->"))
            if balls_to_remove in [1, 2] and count_pile[pile_color_num] >= balls_to_remove:
                return balls_to_remove
            else:
                print(f"Invalid move. You can only remove up to {count_pile[pile_color_num]} balls.")
        except ValueError:
            print("Please enter a valid number (1 or 2).")

# Main function
def main(cr, cb, fp, game_mode, depth):
    count_pile = [cr, cb]

    if fp not in ('computer', 'human'):
        print("Write valid name human/computer.")
        return
    
    chance = fp == 'computer'
    last_player = None  # Track the last player

    while min(count_pile) > 0:
        print("Red -> ", count_pile[0], "\nBlue -> ", count_pile[1], "\n")

        if not chance:  # Human's turn
            human_turn(count_pile)
            last_player = "human"
        else:  # Computer's turn
            computer_turn(count_pile, game_mode, depth)
            last_player = "computer"

        chance = not chance  # Switch turns

    # Determine the winner based on the last player and game mode
    if game_mode == 'standard':
        winner = "Human" if last_player == "human" else "Human"
    else:  # Misère mode
        winner = "Computer" if last_player == "human" else "Human"

    score = 2 * count_pile[0] + 3 * count_pile[1]
    print("Winner ->", winner, "\tPoints Won By ->", score)

# Running the main function
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python ball_game.py <red_balls> <blue_balls> <game_mode> <first_player> <depth>")
        print("<game_mode>: standard or misere")
        print("<first_player>: human or computer")
        print("<depth>: depth for the minimax algorithm (integer)")
        sys.exit(1)

    cr = int(sys.argv[1])  # Number of red balls
    cb = int(sys.argv[2])  # Number of blue balls
    game_mode = sys.argv[3].lower()  # Game mode
    fp = sys.argv[4].lower()  # First player
    depth = int(sys.argv[5])  # Depth for the minimax algorithm

    if fp not in ['human', 'computer'] or game_mode not in ['standard', 'misere']:
        print("Invalid input. Ensure game mode is 'standard' or 'misere', and first player is 'human' or 'computer'.")
        sys.exit(1)

    main(cr, cb, fp, game_mode, depth)
