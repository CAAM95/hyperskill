


from nt import write


def create_matrix(height, width):
    matrix = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(" ")
        matrix.append(row)

    return matrix


def format_tree(matrix):
    for row_indx, row in enumerate(matrix):
        height = len(matrix) - 1
        middle_indx = len(row) // 2

        if row_indx == 0:
            row[middle_indx] = "X"
        elif row_indx == 1:
            row[middle_indx] = "^"
        elif row_indx > 1 and row_indx < height:
            for indx in range(middle_indx, middle_indx + row_indx):
                row[indx] = "*"
            for indx in range(middle_indx - row_indx + 1, middle_indx):
                row[indx] = "*"
        elif row_indx == height:
            row[middle_indx - 1] = "|"
            row[middle_indx + 1] = "|"
    return matrix



def add_decorations_tree(tree_matrix, interval):
    for row_indx, row in enumerate(tree_matrix):
        if row_indx >= len(tree_matrix) - 1:
            continue

        if row_indx <= 1:
            continue

        # branches
        middle_indx = len(row) // 2
        row[middle_indx - row_indx + 1] = "/"
        row[middle_indx + row_indx - 1] = "\\"

    target_number = 0
    # starting at 0

    decoration_spot = 0
    target_number = 0
    start_spot = 0
    for row_indx, row in enumerate(tree_matrix): #manage row

        if row_indx <= 2 or row_indx >= len(tree_matrix) - 1:
            continue


        index = -1

        for indx, elem in enumerate(row): # manage elements in row
            if elem == "*":

                index += 1


            if index % 2 == 1 and elem == "*":
                decoration_spot += 1

                if decoration_spot == 1:
                    target_number = decoration_spot + interval
                    row[indx] = "O"
                elif decoration_spot == target_number:
                    target_number = decoration_spot + interval
                    row[indx] = "O"

    return tree_matrix


def create_postcard(postcard_matrix):

    for row_index in range(len(postcard_matrix)):
        if row_index == 0 or row_index == len(postcard_matrix) - 1:
            fill_char = "-"

            for col_index in range(len(postcard_matrix[row_index])):
                postcard_matrix[row_index][col_index] = fill_char
        else:
            for col_index in range(len(postcard_matrix[row_index])):
                if col_index == 0 or col_index == len(postcard_matrix[row_index]) - 1:
                    postcard_matrix[row_index][col_index] = "|"
                else:
                    postcard_matrix[row_index][col_index] = " "

                    postcard_matrix[row_index][col_index] = " "

        if row_index == 27:
            message = "Merry Xmas"
            msg_start_col = (len(postcard_matrix[0]) - len(message)) // 2
            for i, ch in enumerate(message):
                postcard_matrix[row_index][msg_start_col + i] = ch


    return postcard_matrix




def write_tree_in_postcard(post_card, decorated_tree, x_coordinate, y_coordinate):
    for row_index in range(len(decorated_tree)):
        shifter = 0
        for elem in  decorated_tree[row_index]:

            if elem == " ":
                continue
            else:
                shifter += 1

            if row_index == 0 or row_index == 1:
                post_card[x_coordinate + row_index][y_coordinate] = elem
            elif row_index == len(decorated_tree) - 1:
                post_card[x_coordinate + row_index][y_coordinate - shifter + 1] = elem
                if shifter == 1:
                    post_card[x_coordinate + row_index][y_coordinate - shifter + 1] = " "
                    post_card[x_coordinate + row_index][y_coordinate - shifter + 2] = elem
            else:
                post_card[x_coordinate + row_index][y_coordinate - row_index + shifter] = elem
    return post_card

def create_tree(height, decoration_interval):
    matrix = create_matrix(height + 2, height * 2 - 1)
    tree_matrix = format_tree(matrix)
    decorated_tree = add_decorations_tree(tree_matrix, decoration_interval)

    return decorated_tree


user_input = list(map(int, input().split()))


if len(user_input) == 2:
    decorated_tree = create_tree(int(user_input[0]), int(user_input[1]))
    for row in decorated_tree:
        print("".join(row))
elif len(user_input) % 4 == 0:
    post_card = create_postcard(create_matrix(30, 50))
    for i in range(0, len(user_input), 4):
        decorated_tree = create_tree(int(user_input[i]), int(user_input[i + 1]))
        post_card = write_tree_in_postcard(post_card, decorated_tree, user_input[i + 2], user_input[i + 3])
    for row in post_card:
        print("".join(row))
