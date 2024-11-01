import sys
import random

# Function to determine the best move for the computer using depth-limited search
def computer_turn(count_ball, version, depth=3):
    best_move = None
    best_score = float('-inf')

    for i in range(2):  # 0 for red, 1 for blue
        for balls_to_remove in [1, 2]:  # Check removing 1 or 2 balls
            if count_ball[i] >= balls_to_remove:
                new_ball = count_ball[:]
                new_ball[i] -= balls_to_remove
                score = minimax(new_ball, depth - 1, False, version)
                
                if score > best_score:
                    best_score = score
                    best_move = (i, balls_to_remove)

    if best_move:
        count_ball[best_move[0]] -= best_move[1]
        print(f"Computer removes {best_move[1]} from {'red' if best_move[0] == 0 else 'blue'} ball.")

# Minimax algorithm with depth limit
def minimax(count_ball, depth, maximize, version):
    if depth == 0 or min(count_ball) == 0:
        return evaluate_position(count_ball, version)

    if maximize:
        best_score = float('-inf')
        for i in range(2):
            for balls_to_remove in [1, 2]:
                if count_ball[i] >= balls_to_remove:
                    new_ball = count_ball[:]
                    new_ball[i] -= balls_to_remove
                    score = minimax(new_ball, depth - 1, False, version)
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(2):
            for balls_to_remove in [1, 2]:
                if count_ball[i] >= balls_to_remove:
                    new_ball = count_ball[:]
                    new_ball[i] -= balls_to_remove
                    score = minimax(new_ball, depth - 1, True, version)
                    best_score = min(best_score, score)
        return best_score

# Function to evaluate the position
def evaluate_position(count_ball, version):
    if version == 'standard':
        return 1 if min(count_ball) == 0 else 0  # Win for computer
    else:  # Misère mode
        return -1 if max(count_ball) == 0 else 0  # Win for human

# Function to handle human's turn input
def human_turn(count_ball):
    while True:
        ball_color = input("Your turn - Choose One (red/blue)->").lower()
        if ball_color in ['red', 'blue']:
            ball_color_num = 0 if ball_color == 'red' else 1
            if count_ball[ball_color_num] <= 0:
                print("No balls left in this ball. Choose another color.")
                continue
            
            balls_to_remove = get_balls_to_remove(count_ball, ball_color_num)
            count_ball[ball_color_num] -= balls_to_remove
            break
        else:
            print("Invalid color. Please choose 'red' or 'blue'.")

# Function to get the number of balls to remove from the human player
def get_balls_to_remove(count_ball, ball_color_num):
    while True:
        try:
            balls_to_remove = int(input("Choose number of balls to remove (1 or 2)->"))
            if balls_to_remove in [1, 2] and count_ball[ball_color_num] >= balls_to_remove:
                return balls_to_remove
            else:
                print(f"Invalid move. You can only remove up to {count_ball[ball_color_num]} balls.")
        except ValueError:
            print("Please enter a valid number (1 or 2).")

# Main function
def main(cr, cb, fp, version, depth):
    count_ball = [cr, cb]

    if fp not in ('computer', 'human'):
        print("Write valid name human/computer.")
        return
    
    chance = fp == 'computer'
    last_player = None  # Track the last player

    while min(count_ball) > 0:
        print("Red -> ", count_ball[0], "\nBlue -> ", count_ball[1], "\n")

        if not chance:  # Human's turn
            human_turn(count_ball)
            last_player = "human"
        else:  # Computer's turn
            computer_turn(count_ball, version, depth)
            last_player = "computer"

        chance = not chance  # Switch turns

    # Determine the winner based on the last player and game mode
    if version == 'standard':
        winner = "Human" if last_player == "human" else "Computer"
    else:  # Misère mode
        winner = "Human" if last_player == "computer" else "Computer"

    score = 2 * count_ball[0] + 3 * count_ball[1]
    print("Winner ->", winner, "\tPoints Won By ->", score)

# Running the main function
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python ball_game.py <red_balls> <blue_balls> <version> <first_player> <depth>")
        print("<version>: standard or misere")
        print("<first_player>: human or computer")
        print("<depth>: depth for the minimax algorithm (integer)")
        sys.exit(1)

    cr = int(sys.argv[1])  # Number of red balls
    cb = int(sys.argv[2])  # Number of blue balls
    version = sys.argv[3].lower()  # Game mode
    fp = sys.argv[4].lower()  # First player
    depth = int(sys.argv[5])  # Depth for the minimax algorithm

    if fp not in ['human', 'computer'] or version not in ['standard', 'misere']:
        print("Invalid input. Ensure game mode is 'standard' or 'misere', and first player is 'human' or 'computer'.")
        sys.exit(1)

    main(cr, cb, fp, version, depth)
