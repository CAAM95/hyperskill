import random
import math

def format_snake(snake):  
    if len(snake) >= 6:
        return "".join(str(pair) for pair in snake[:3]) + "..." + \
            "".join(str(pair) for pair in snake[-3:])
    else:
        return "".join(str(pair) for pair in snake)

def format_player_deck(player_deck):
    return "\n".join(str(i+1) + ':' + str(player_deck[i]) for i in range(len(player_deck)))

def call_interface(stock_deck, computer_deck, player_deck, snake_deck):
    print("=" * 70)
    print('Stock size: ' + str(len(stock_deck)))
    print('Computer pieces: ' + str(len(computer_deck)))
    print()
    print(format_snake(snake_deck))
    print()
    print('Your pieces:')
    print(format_player_deck(player_deck))
    print()

def get_computer_choice(computer_deck):
    return random.randint(-len(computer_deck), len(computer_deck))

def check_game_is_draw(snake_deck):
    count = 0
    if snake_deck[0][0] == snake_deck[-1][1]:
        num = snake_deck[0][0]
        for pair in snake_deck:
            if num in pair:
                count += 1
    if count == 8:
        return True
    else:
        return False

def is_matching_end(user_input, domino, snake_deck):
    if user_input < 0:
        snake_head = snake_deck[0]
        if domino[1] == snake_head[0] or domino[0] == snake_head[0]:
            return True
    elif user_input > 0:
        snake_tail = snake_deck[-1]
        if domino[0] == snake_tail[1] or domino[1] == snake_tail[1]:
            return True
    return False

def check_if_need_to_flip(user_input, domino, snake_deck):
    if user_input < 0:
        if domino[0] == snake_deck[0][0]:
            return [domino[1], domino[0]]
        else:
            return domino
    elif user_input > 0:
        if domino[1] == snake_deck[-1][1]:
            return [domino[1], domino[0]]
        else:
            return domino


def get_score_and_count_of_dominoes(dominoes):
    count_0_pairs = [0,]
    count_1_pairs = [1,]
    count_2_pairs = [2,]
    count_3_pairs = [3,]
    count_4_pairs = [4,]
    count_5_pairs = [5,]
    count_6_pairs = [6,]
    count_7_pairs = [7,]
    count_8_pairs = [8,]
    count_9_pairs = [9,]
    count_10_pairs = [10,]
    count_11_pairs = [11,]
    count_12_pairs = [12,]

    for domino in dominoes:
        if sum(domino) == 0:
            count_0_pairs.append(domino)
        elif sum(domino) == 1:
            count_1_pairs.append(domino)
        elif sum(domino) == 2:
            count_2_pairs.append(domino)
        elif sum(domino) == 3:
            count_3_pairs.append(domino)
        elif sum(domino) == 4:
            count_4_pairs.append(domino)
        elif sum(domino) == 5:
            count_5_pairs.append(domino)
        elif sum(domino) == 6:
            count_6_pairs.append(domino)
        elif sum(domino) == 7:
            count_7_pairs.append(domino)
        elif sum(domino) == 8:
            count_8_pairs.append(domino)
        elif sum(domino) == 9:
            count_9_pairs.append(domino)
        elif sum(domino) == 10:
            count_10_pairs.append(domino)
        elif sum(domino) == 11:
            count_11_pairs.append(domino)
        elif sum(domino) == 12:
            count_12_pairs.append(domino)

    return [count_0_pairs, count_1_pairs, count_2_pairs, count_3_pairs, count_4_pairs, count_5_pairs, count_6_pairs, count_7_pairs, count_8_pairs, count_9_pairs, count_10_pairs, count_11_pairs, count_12_pairs]


player_deck = []
computer_deck = []
snake_deck = []
stock_deck = []
is_player_turn = True

    

for i in range(7):
    for j in range(i, 7):
        stock_deck.append([i, j])

while True:
    random.shuffle(stock_deck)

    player_deck = stock_deck[:7]

    computer_deck = stock_deck[7:14]

    found_player_double = False
    found_computer_double = False  

    max_player_piece = max(player_deck, key=sum)
    if max_player_piece[0] == max_player_piece[1]:
        found_player_double = True

    max_computer_piece = max(computer_deck, key=sum)
    if max_computer_piece[0] == max_computer_piece[1]:
        found_computer_double = True


    if not found_player_double and not found_computer_double:
        continue

    stock_deck = stock_deck[14:]

    if max_player_piece > max_computer_piece:
        domino = player_deck.pop(player_deck.index(max_player_piece))
        snake_deck.append(domino)
        is_player_turn = False
    elif max_computer_piece > max_player_piece:
        domino = computer_deck.pop(computer_deck.index(max_computer_piece))
        snake_deck.append(domino)
        is_player_turn = True

    break


while True:
    call_interface(stock_deck, computer_deck, player_deck, snake_deck)

    if check_game_is_draw(snake_deck):
        print("Status: The game is over. It's a draw!")
        break

    if len(stock_deck) == 0:
        print("Status: The game is over. It's a draw!")
        break
    
    if len(player_deck) == 0:
        print("Status: The game is over. You won!")
        break

    if len(computer_deck) == 0:
        print("Status: The game is over. The computer won!")
        break
    
    if is_player_turn:
        print('Status: It\'s your turn to make a move. Enter your command.')
        while True:
            try:
                user_input = int(input())
            except ValueError:
                print("Invalid input. Please try again.")
                continue

            # check if input is 0 pick up stock
            if user_input == 0:
                stock_piece = stock_deck.pop(random.randint(0, len(stock_deck) - 1))
                player_deck.append(stock_piece)
                is_player_turn = False
                break
            
            # adjust input for 0 based indexing
            domino_index = abs(user_input) - 1

            # check if index is valid
            if domino_index < 0 or domino_index >= len(player_deck):
                print("Invalid input. Please try again.")
                continue

            # get domino from deck
            domino = player_deck[domino_index]

            # place to left or right of snake
            if user_input > 0:
                if is_matching_end(user_input, domino, snake_deck):
                    domino = check_if_need_to_flip(user_input, domino, snake_deck)
                    snake_deck.append(domino)
                else:
                    print("Illegal move. Please try again.")
                    continue
            elif user_input < 0:
                if is_matching_end(user_input, domino, snake_deck):
                    domino = check_if_need_to_flip(user_input, domino, snake_deck)
                    snake_deck.insert(0, domino)
                else:
                    print("Illegal move. Please try again.")
                    continue

            player_deck.pop(domino_index)
            is_player_turn = False
            break
    else:
        print('Status: Computer is about to make a move. Press Enter to continue...')
        input()
        while True:
            # computer will sort its pieces by rarity
            dominoes_by_rarity = sorted(get_score_and_count_of_dominoes(computer_deck), key=lambda x: x[0], reverse=True)


            # create a list of all dominoes that can be placed by highest rarity first
            domino_options = []
            for score_group in dominoes_by_rarity:
                temp_dominoes = list(score_group[1:])
                for i in range(len(temp_dominoes)):
                    domino_options.append(temp_dominoes[i])
            
            # try to place all dominoes on left and right of snake
            target_domino = None
            choose_stock = True
            for domino in domino_options:
                if is_matching_end(-1, domino, snake_deck): # left
                    target_domino = domino
                    domino = check_if_need_to_flip(-1, domino, snake_deck)
                    snake_deck.insert(0, domino)
                    is_player_turn = True
                    choose_stock = False
                    break
                elif is_matching_end(1, domino, snake_deck): # right
                    target_domino = domino
                    domino = check_if_need_to_flip(1, domino, snake_deck)
                    snake_deck.append(domino)
                    is_player_turn = True
                    choose_stock = False
                    break

            if choose_stock:
                stock_piece = stock_deck.pop(random.randint(0, len(stock_deck) - 1))
                computer_deck.append(stock_piece)
                is_player_turn = True
                break

            target_domino_index = computer_deck.index(target_domino)
            computer_deck.pop(target_domino_index)
            is_player_turn = True
            break


    







