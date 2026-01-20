import random
import time
import os

random.seed(int(time.time() * 1000))

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def process_equation(equation):
    equation_parts = equation.split()
    var1 = int(equation_parts[0])
    operator = equation_parts[1]
    var2 = int(equation_parts[2])

    return var1, operator, var2

def generate_equation():
    a = random.randint(2, 9)
    b = random.randint(2, 9)
    operator = ["+", "-", "*"]
    rand_op = random.randint(0, len(operator) - 1)
    return f"{a} {operator[rand_op]} {b}"

def determine_operation(var1, operator, var2):
    if operator == "+":
        return add(var1, var2)
    elif operator == "-":
        return subtract(var1, var2)
    elif operator == "*":
        return multiply(var1, var2)


def cycle_tests(difficulty):
    correct = 0
    for i in range(5):
        generated_equation = process_difficulty(difficulty)
        print(generated_equation)
        if difficulty == 1:
            var1, operator, var2 = process_equation(generated_equation)
            solution = determine_operation(var1, operator, var2)
        elif difficulty == 2:
            solution = generated_equation**2

        while True:
            try:
                users_solution = int(input())
                break
            except ValueError:
                print("Incorrect format.")

        if users_solution == solution:
            print("Right!")
            correct += 1
        else:
            print("Wrong!")
    return correct

def ask_difficulty():
    while True:
        try:
            print("Which level do you want? Enter a number:\n1 - simple operations with numbers 2-9\n2 - integral squares of 11-29")
            difficulty = int(input())
            if difficulty not in range(1, 3):
                raise ValueError
        except ValueError:
            print("Incorrect format.")
            continue

        return difficulty

def generate_square():
    n = random.randint(11, 29)
    return n

def process_difficulty(difficulty):
    if difficulty == 1:
        return generate_equation()
    elif difficulty == 2:
        return generate_square()

def handle_save_file(result):


    cwd = os.getcwd()
    file_path = f"{cwd}/results.txt"
    if not os.path.isfile(file_path):
        with open(file_path, 'w') as file:
            file.write(result)
    else:
        with open(file_path, 'a') as file:
            file.write('\n'+result)

def ask_to_save(grade, difficulty):
    while True:
        response = input("Would you like to save your result to the file? Enter yes or no.\n").lower()
        if response not in ["yes", "no", "y", "n"]:
            exit()
        elif response == "yes" or response == "y":
            username = input("Enter your username: ")
            result = f"{username}: {grade}/5 in level {difficulty} ({"1 - simple operations with numbers 2-9" if difficulty == 1 else "2 - integral squares of 11-29"})"
            handle_save_file(result)
            print("The results are saved in \"results.txt\".")
            break
        elif response == "no" or response == "n":
            exit()


def main():
    random.seed(time.time())
    difficulty = ask_difficulty()
    grade = cycle_tests(difficulty)
    print(f"your mark is {grade}/5")
    ask_to_save(grade,difficulty)




if __name__ == "__main__":
    #standard_input = 's', '3';
    main()
