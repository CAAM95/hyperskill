import random



words = ['python', 'java', 'swift', 'javascript']


player_win_count = 0
player_lose_count = 0

print("H A N G M A N")

while True:
    random_word =  random.choice(words)
    attempt_counter = 8


    hinted_characters = list(len(random_word) * '-')
    chosen_word_char_list = list(random_word)
    letter_history = []
    start_input = input('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit: ')

    if start_input in ['play', 'results', 'exit']:
        if start_input == 'play':

            while True:
                if '-' not in hinted_characters:
                    print()
                    print(f'You guessed the word {"".join(hinted_characters)}!')
                    print('You survived!')
                    player_win_count += 1
                    break
                if attempt_counter == 0:
                    print()
                    print('You lost!')
                    player_lose_count += 1
                    break

                print()
                print("".join(hinted_characters))
                chosen_letter = input('Input a letter: ')

                if len(chosen_letter) != 1:
                    print("Please, input a single letter.")
                    continue

                if not chosen_letter.isalpha() or chosen_letter.isupper():
                    print("Please, enter a lowercase letter from the English alphabet.")
                    continue



                if chosen_letter not in chosen_word_char_list:
                    print("That letter doesn't appear in the word.")
                    attempt_counter -= 1
                    continue
                if chosen_letter in letter_history:
                    print("You've already guessed this letter.")
                    continue


                for index in range(len(hinted_characters)):
                    if chosen_word_char_list[index] == chosen_letter:
                        hinted_characters[index] = chosen_letter
                        letter_history.append(chosen_letter)
        elif start_input == 'results':
            print(f'You won: {player_win_count} times')
            print(f'You lost: {player_lose_count} times')
        elif start_input == 'exit':
            break
        else:
            print('Not a correct input.')






