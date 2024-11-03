import string
import random

def create_set(start, number):
    losing_set = {1}
    winning_set = {2, 3, 4, 6, 7, 8}

    if start == 1:
        while start < number:
            start += 4
            losing_set.add(start)
        return sorted(list(losing_set))
    elif start == 4:
        while start < number:
            start += 4
            winning_set.add(start) 
        return sorted(list(winning_set))


def gen_rand_choice(max):
    if max == 1 or max == 2:
        return 1
    elif max == 3:
        return 2
    elif max == 4:
        return 3
    else:
        return random.randint(1,3)

def check_position_for_choice(bool1, bool2):
    if bool1:
        return True
    elif bool2:
        return False
    else:
        return None

def find_next_position_number(number, some_list):
    for element in some_list:
        if number >= element:
            continue
        else:
            return some_list[(some_list.index(element) - 1)]
        

def check_initial_pencils():
    int_digits = []
    for e in string.digits:
        int_digits.append(int(e))

    # check if num is an int, no letters
    while True:
        try:
            pencil_count = int(input())
            var_conv = int(pencil_count)
        except ValueError:
            print('The number of pencils should be numeric')
            continue
        # check if num is equal to 0, should be positive
        if var_conv <= 0:
            print('The number of pencils should be positive')
            continue
        else:
            break
    return pencil_count


def check_player():
    # choice should be in the list of players
    names_list = ['John', 'Jack']
    while True:
        print('Who will be the first (John, Jack):')
        name = input()
        if name in names_list:
            break
        else:
            print("Choose between 'John' and 'Jack'")
    return name

def check_pencil_removal():
    # number can only be 1,2,3 or string version
    while True:
        number = input()
        try:
            number = int(number)
            if number in [1,2,3]:
                break
            else:
                print("Possible values: '1', '2' or '3'")
                continue
        except ValueError:
            print("Possible values: '1', '2' or '3'")

    return number

def check_total_pencil_removal(number, total):
    difference = total - number
    return difference

def give_jack_john(name):
    if name == 'John':
        name  = 'Jack'
    elif name == 'Jack':
        name = 'John'
    return name

print('How many pencils would you like to use:')
total_pencils = check_initial_pencils()


player_name = check_player()
bot_name = 'Jack'
current_player = player_name


winning_list = create_set(4, total_pencils)
losing_list = create_set(1, total_pencils)


while True:
    if total_pencils == 0:
        print('{} won!'.format(current_player))
        break
    else:
        pencil_template = total_pencils * '|'
        print(pencil_template)
        print("{}'s turn:".format(current_player))

    while True:
        if current_player == bot_name:
            if total_pencils in winning_list: # on winning position, send player to losing pos
                losing_num = find_next_position_number(total_pencils, losing_list)
                bot_choice = total_pencils - losing_num
            elif total_pencils in losing_list: # on a loosing position find winning pos
                if total_pencils == 1:
                    bot_choice = 1
                else:
                    winning_num = find_next_position_number(total_pencils, winning_list)
                    bot_choice = total_pencils - winning_num
            else: # on null pos, make player lose
                losing_num = find_next_position_number(total_pencils, losing_list)
                bot_choice = total_pencils - losing_num

            if check_total_pencil_removal(bot_choice, total_pencils) < 0:
                print('Too many pencils were taken')
            else:
                print(bot_choice)
                total_pencils -= bot_choice
                current_player = give_jack_john(current_player)
                break
        else:
            remove_pencil_count = check_pencil_removal()
            if check_total_pencil_removal(remove_pencil_count, total_pencils) < 0:
                print('Too many pencils were taken')
            else:
                total_pencils -= remove_pencil_count
                current_player = give_jack_john(current_player)
                break
