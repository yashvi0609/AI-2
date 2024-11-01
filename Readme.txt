Name: Yashvi Thakkar
UTA ID: 1002184506
Programming Language: python 3.13.0
Pip version: 24.2

Code Structure:
The code is divided into the following functions:

computer_turn(count_ball, version, depth=3): Determines the optimal move for the computer by simulating possible moves using the minimax function.

minimax(count_ball, depth, maximize, version): A recursive algorithm to simulate the game tree up to the given depth and evaluate the best score for the computer's possible moves.

evaluate_position(count_ball, version): Evaluates the game state, checking if a winning or losing position has been reached.

human_turn(count_ball): Handles the human player's input and move choices, ensuring valid input and enforcing game rules.

get_balls_to_remove(count_ball, ball_color_num): Validates the number of balls the human player wishes to remove.

main(cr, cb, fp, version, depth): Initializes the game and alternates turns between the human player and the computer until a win condition is reached, then announces the winner.

Run Command:
To run this game from the command line, open a terminal or command prompt, navigate to the directory containing ball_game.py, and use the following format:

python ball_game.py <red_balls> <blue_balls> <version> <first_player> <depth>
