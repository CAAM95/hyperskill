# write your code here
import random

def create_board(cells="         "):
    board = []
    for i in range(int(len(cells) / 3)):
        board.append(list(cells[i * 3:(i + 1) * 3]))
    return board

def computer_random_move(board, difficulty):
    print(f"Making move level \"{difficulty}\"")
    choice_boundry = len(board)
    rand_coordinates = [random.randint(0, choice_boundry - 1) for _ in range(2)]
    while not check_coordinates(rand_coordinates, board):
        rand_coordinates = [random.randint(0, choice_boundry - 1) for _ in range(2)]
    next_move = coordinate_next_move(board)
    board = place_move(next_move, rand_coordinates, board)
    return board

def print_board(board):
    board_width = len(board) * len(board)
    print("-" * board_width)
    for i in range(len(board)):
        print("| " + " ".join(board[i]) + " |")
    print("-" * board_width)

def check_coordinates(coordinates, board):
    target = board[coordinates[0]][coordinates[1]]
    if target == "X" or target == "O":
        return False
    return True

def format_board(cells):
    cells = cells.upper()
    cells = cells.replace("_", " ")
    return cells

def get_coordinates(board):
    while True:
        coordinates = input("Enter the coordinates: ")
        coordinates = coordinates.split()

        # if len(coordinates) != 2:
        #     print("Provide two coordinates!")
        #     continue

        try:
            coordinates = [int(i) - 1 for i in coordinates]
        except ValueError:
            print("You should enter numbers!")
            continue

        if not 0 <= coordinates[0] < len(board) or not 0 <= coordinates[1] < len(board):
            print("Coordinates should be from 1 to 3!")
            continue

        if not check_coordinates(coordinates, board):
            print("This cell is occupied! Choose another one!")
            continue

        return coordinates

def defense_mode(board):
    i_am = coordinate_next_move(board)
    opponent = None
    if i_am == "X":
        opponent = "O"
    else:
        opponent = "X"
    return computer_winning_move(board, opponent)
    if opponent_winning_move:
        return place_move(i_am, opponent_winning_move, board)
    else:
        return None

def coordinate_next_move(board):
    x_count = 0
    o_count = 0

    for row in board:
        x_count += row.count("X")
        o_count += row.count("O")

    if x_count == o_count:
        return "X"
    else:
        return "O"

def place_move(move, coordinates, board):
    board[coordinates[0]][coordinates[1]] = move
    return board


def human_move(board, difficulty="easy"):
    coordinates = get_coordinates(board)
    next_move = coordinate_next_move(board)
    board = place_move(next_move, coordinates, board)
    return board

def check_complete(board):
    # when no side has three in a row, and the table is complete
    for row in board:
        if " " in row:
            return False
    return True

def check_rows(board):
    winner = None
    for row in board:
        if row.count("X") == 3:
            winner = "X"
        elif row.count("O") == 3:
            winner = "O"
    return winner

def check_columns(board):
    winner = None
    for i in range(len(board)):
        if [board[0][i], board[1][i], board[2][i]].count("X") == 3:
            winner = "X"
        elif [board[0][i], board[1][i], board[2][i]].count("O") == 3:
            winner = "O"
    return winner

def check_diagonals(board):
    winner = None
    left_to_right = [board[0][0], board[1][1], board[2][2]]
    right_to_left = [board[0][2], board[1][1], board[2][0]]

    if right_to_left.count("X") == 3 or left_to_right.count("X") == 3:
        winner = "X"
    elif right_to_left.count("O") == 3 or left_to_right.count("O") == 3:
        winner = "O"
    return winner

def check_game_state(board):
    winner = check_rows(board)
    if winner:
        return winner

    winner = check_columns(board)
    if winner:
        return winner

    return check_diagonals(board)

def ai_scan_rows(board, whoami):
    for i, row in enumerate(board):
        my_positions = []
        for j, cell in enumerate(row):
            if cell == whoami:
                my_positions.append(j)

        if len(my_positions) != 2:
            continue

        fill_index = len(row) - my_positions[0] - my_positions[1]
        if row[fill_index] == " ":
            return [i, fill_index]
            board = place_move(whoami, [i, fill_index], board)
            return True
    return None

def ai_scan_columns(board, whoami):
    for i in range(len(board)):
        my_positions = []
        column = [board[0][i], board[1][i], board[2][i]]

        for j, cell in enumerate(column):
            if cell == whoami:
                my_positions.append(j)

        if len(my_positions) != 2:
            continue

        fill_index = len(column) - my_positions[0] - my_positions[1]  # 3 - (a+b)
        if column[fill_index] == " ":
            return [fill_index, i]
            board = place_move(whoami, [fill_index, i], board)
            return True
    return None

def ai_scan_diagonals(board, whoami):
    diag = [board[0][0], board[1][1], board[2][2]]
    if diag.count(whoami) == 2 and diag.count(" ") == 1:
        k = diag.index(" ")
        return [k, k]
        board = place_move(whoami, [k, k], board)
        return True

    diag = [board[0][2], board[1][1], board[2][0]]
    if diag.count(whoami) == 2 and diag.count(" ") == 1:
        k = diag.index(" ")
        return [k, 2 - k]
        board = place_move(whoami, [k, 2 - k], board)
        return True
    return None

def computer_winning_move(board, whoami):
    if not whoami:
        return None

    target_row = ai_scan_rows(board, whoami)
    target_column = ai_scan_columns(board, whoami)
    target_diagnol = ai_scan_diagonals(board, whoami)

    if target_row:
        return target_row
    elif target_column:
        return target_column
    elif target_diagnol:
        return target_diagnol
    else:
        return None





def menu():
    while True:
        user_input = input("Input command: ")
        commands = user_input.split()

        if len(commands) == 1 and commands[0] in ["exit"]:
            return commands

        if len(commands) != 3:
            print("Bad parameters!")
            continue

        if (commands[0] not in ["start", "exit"]
                or commands[1] not in ["easy", "medium", "hard", "user"]
                or commands[2] not in ["easy", "medium", "hard", "user"]):
            print("Bad parameters!")
            continue

        return commands

def process_easy_difficulty(board, player):
    board = computer_random_move(board, player)
    return board

def process_medium_difficulty(board, player):
    next_move = coordinate_next_move(board)
    offense_move = computer_winning_move(board, next_move)
    if offense_move:
        board = place_move(next_move, offense_move, board)
    elif defense_mode(board):
        defense_move = defense_mode(board)
        board = place_move(next_move, defense_move, board)
    else:
        board = computer_random_move(board, player)
    return board

def minimax(board, is_maximizing, ai_player, human_player):
    winner = check_game_state(board)
    if winner == ai_player:
        return 1
    elif winner == human_player:
        return -1
    elif check_complete(board):
        return 0

    if is_maximizing:
        best = -float('inf')
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == " ":
                    board[i][j] = ai_player
                    score = minimax(board, False, ai_player, human_player)
                    board[i][j] = " "  # undo the move
                    best = max(best, score)
        return best
    else:
        best = float('inf')
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == " ":
                    board[i][j] = human_player
                    score = minimax(board, True, ai_player, human_player)
                    board[i][j] = " "  # undo the move
                    best = min(best, score)
        return best


def process_hard_difficulty(board, player):
    ai_player = coordinate_next_move(board)
    human_player = "O" if ai_player == "X" else "X"

    best_score = -float('inf')
    best_move = None

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == " ":
                board[i][j] = ai_player                          # try move
                score = minimax(board, False, ai_player, human_player)
                board[i][j] = " "                                # undo move
                if score > best_score:
                    best_score = score
                    best_move = [i, j]

    if best_move:
        board = place_move(ai_player, best_move, board)
    return board

def run_round(board, player_x, player_o):
    for player in [player_x, player_o]:
        if player != "user":
            if player == "easy":
                board = process_easy_difficulty(board, player)
            elif player == "medium":
                board = process_medium_difficulty(board, player)
            elif player == "hard":
                board = process_hard_difficulty(board, player)
        else:
            board = human_move(board)
        print_board(board)

        is_complete = check_complete(board)
        winner = check_game_state(board)
        if winner or is_complete:
            break

    return board

def main():
    # cells = input("Enter the cells: ")
    # cells = format_board(cells)
    commands = menu()
    if commands[0] == "exit":
        print("Bye!")
    elif commands[0] == "start":
        board = create_board()
        print_board(board)
        while True:
            player_x = commands[1]
            player_o = commands[2]

            board = run_round(board, player_x, player_o)

            is_complete = check_complete(board)
            winner = check_game_state(board)
            if winner:
                print(f"{winner} wins!")
                break
            elif is_complete and not winner:
                print("Draw!")
                break


if __name__ == "__main__":
    main()
