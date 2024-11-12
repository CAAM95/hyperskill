def print_board(board):
    print('---------')
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('---------')

def create_lst_matrix():
    matrix = []
    for index in range(0, 3):
        temp_lst = []
        for index in range(0,3):
            temp_lst.append(' ')
        matrix.append(temp_lst)
    return matrix


def all_elements_are(lst, char):
    return all(element == char for element in lst)

def check_horizontal(matrix, choice):
    for row in matrix:
        result = all_elements_are(row, choice)
        if result:
            return result
    return False

def check_vertical(matrix, choice):
    if matrix[0][0] == choice and matrix[1][0] == choice and matrix[2][0] == choice:
        return True
    elif matrix[0][1] == choice and matrix[1][1] == choice and matrix[2][1] == choice:
        return True
    elif matrix[0][2] == choice and matrix[1][2] == choice and matrix[2][2] == choice:
        return True

def check_diagnol(matrix, choice):
    if matrix[0][0] == choice and matrix[1][1] == choice and matrix[2][2] == choice:
        return True
    elif matrix[0][2] == choice and matrix[1][1] == choice and matrix[2][0] == choice:
        return True

def check_wins(matrix, choice):
    if check_horizontal(matrix, choice):
        return True
    elif check_vertical(matrix, choice):
        return True
    elif check_diagnol(matrix, choice):
        return True
    else:
        return False

matrix = create_lst_matrix()
print_board(matrix)
current_player = "X"
play_count = 0
while True:
    try:
        user_coordinates = input().split()
        
        # used to format user coordinated on 0-based index
        for i in range(0, len(user_coordinates)):
            user_coordinates[i] = int(user_coordinates[i]) - 1
        
        # checking index range of coords
        if user_coordinates[0] < 0 or user_coordinates[0] > 2 or user_coordinates[1] < 0 or user_coordinates[1] > 2:
            raise IndexError

        if matrix[user_coordinates[0]][user_coordinates[1]] in ['X', 'O']:
            print("This cell is occupied! Choose another one!")
        else:
            # adds the move of the current player
            matrix[user_coordinates[0]][user_coordinates[1]] = current_player
            play_count += 1
            print_board(matrix)

            # swaps the player
            if current_player == 'X':
                current_player = 'O'
            else:
                current_player = 'X'
            
            
        is_x_who_wins = check_wins(matrix, 'X')
        is_o_who_wins = check_wins(matrix, 'O')
        if is_x_who_wins:
            print("X wins")
            break
        elif is_o_who_wins:
            print("O wins")
            break
        if play_count == 9:
                print("Draw")
                break
    except IndexError:
        print('Coordinates should be from 1 to 3!')
    except (ValueError, TypeError):
        print('You should enter numbers!')
