import random

def get_rand_choice(choice_options):
    return random.choice(choice_options) 

def play_game(user_choice, user_score, computer_choice):
    if user_choice == computer_choice:
        user_score += 50
        return user_score, 'There is a draw ({})'.format(user_choice)
    elif (user_choice == 'scissors' and computer_choice == 'paper') or \
         (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'paper' and computer_choice == 'rock'):
        user_score += 100
        return user_score, 'Well done. The computer chose {} and failed'.format(computer_choice)
    else:
        return user_score, 'Sorry, but the computer chose {}'.format(computer_choice)

def read_from_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()

def capture_scores(file_content):
    words = file_content.split()
    scores = {}

    for i in range(len(words) - 1):
        user_name = words[i]
        score = words[i + 1]
        scores[user_name] = score
    
    return scores


def play_modified_game(user_choice, user_score, computer_choice, custom_options):
    index = custom_options.index(user_choice)
    num_winning = (len(custom_options) - 1) // 2  # Ensure integer division
    
    winning_choices = []
    for i in range(1, num_winning + 1):
        winning_choices.append(custom_options[(index + i) % len(custom_options)])
        
    if user_choice == computer_choice:
        user_score += 50
        return user_score, 'There is a draw ({})'.format(user_choice)
    elif computer_choice not in winning_choices:
        user_score += 100
        return user_score, 'Well done. The computer chose {} and failed'.format(computer_choice)
    else:
        return user_score, 'Sorry, but the computer chose {}'.format(computer_choice)


def process_input(user_input, user_score, options, play_function):
    if user_input == end_command:
        return None, user_score
    elif user_input == score_command:
        print('Your rating: {}'.format(user_score))
    elif user_input in options:
        user_score, match_result = play_function(user_input, user_score, get_rand_choice(options))
        print(match_result)
    else:
        print('Invalid input')
    return user_input, user_score


end_command = '!exit'
score_command = '!rating'
user_name = input('Enter your name: ')
user_score = 0
print('Hello, {}'.format(user_name))
file_content = read_from_file('rating.txt')
file_formatted = capture_scores(file_content)

mode_is_set = False
custom_options = []
default_options = ['rock', 'paper', 'scissors']

if user_name in file_formatted:
    user_score =  int(file_formatted[user_name])

user_mode = input()
if user_mode != '':
    mode_is_set = True
    for option in user_mode.split(','):
        custom_options.append(option)

while True:
    print("Okay, let's start")
    user_input = input()
    if mode_is_set:
        user_input, user_score = process_input(user_input, user_score, custom_options, play_modified_game)
    else:
        user_input, user_score = process_input(user_input, user_score, default_options, play_game)
    if user_input is None:
        break
