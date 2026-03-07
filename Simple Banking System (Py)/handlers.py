import random
from logic import *

def create_account(data):
    while True:
        issuer_identification_number = "400000"
        account_number = ''.join(str(random.randint(0, 9)) for _ in range(9))
        checksum = str(random.randint(0, 9))
        card_number = issuer_identification_number + account_number + checksum
        if checkLuhn(card_number):
            break

    pin = str(random.randint(0, 9999)).zfill(4)
    data[card_number] = pin
    print("Your card number:")
    print(card_number)
    print("Your card PIN:")
    print(pin)

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO card (number, pin) VALUES (?, ?)", (card_number, pin))
    connection.commit()
    connection.close()
    return data


def check_balance(card_number):
    card_tuple = fetch_db_card_data(card_number)
    print(f"Balance: {card_tuple["balance"]}")
    return card_tuple

def log_out(data):
    print("You have successfully logged out!")
    return data



def get_income(card_number):
    income = int(input("Enter income:\n"))
    card_balance = add_income(card_number, income)
    print(f"Income was added!\nBalance: {card_balance}")


def do_transfer(card_number):
    transfer_card_number = input("Enter card number:\n")
    target_card_tuple = fetch_db_card_data(transfer_card_number)
    if not checkLuhn(transfer_card_number):
        print("Probably you made a mistake in the card number. Please try again!")
        return card_number
    if not target_card_tuple:
        print("Such a card does not exist.")
        return card_number
    if target_card_tuple["number"] == card_number:
        print("You can't transfer money to the same account!")
        return card_number



    amount = int(input("Enter how much money you want to transfer:\n"))

    if amount > fetch_db_card_data(card_number)["balance"]:
        print("Not enough money!")
        return card_number
    else:
        card_balance = remove_income(card_number, amount)
        transfer_card_balance = add_income(transfer_card_number, amount)
        print(amount)
        print(fetch_db_card_data(card_number)['number'], fetch_db_card_data(card_number)['balance'])
        print(fetch_db_card_data(transfer_card_number)['number'], fetch_db_card_data(transfer_card_number)['balance'])
        print("Transfer was successful!")
    return card_number

def close_account(card_number):
    result = delete_db_tuple(card_number)
    if result == 1:
        print("The account has been closed!")
    else:
        print("The account has not been closed!")
    return result

def account_manager(card_number):
    commands = {
        "1": check_balance,
        "2": get_income,
        "3": do_transfer,
        "4": close_account,
        "5": log_out,
        "0": exit_application
    }
    while True:
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")
        choice = input("choice:\n")
        if choice not in commands:
            print("Invalid choice. Please try again.")
            continue

        result = commands[choice](card_number)
        if choice == "0":
            return result
        elif choice == "5" or choice == "4":
            return result
        else:
            continue

def create_connection():
    return get_connection()

def log_in(data):
    card_number = input("Enter your card number:\n")
    pin = input("Enter your PIN:\n")

    if not checkLuhn(card_number):
        print("Wrong, fake card detected")
        return data

    is_card_found = lookup_card(card_number)
    if not is_card_found:
        print("Wrong card number or PIN!")
        return data

    is_matching_pin = match_pin(card_number, pin)
    if not is_matching_pin:
        print("Wrong card number or PIN!")
        return data

    print("You have successfully logged in!")
    result = account_manager(card_number)
    return result

def exit_application(data):
    print("Bye!")
    return None

def main_menu(data):

    commands = {
        "1": create_account,
        "2": log_in,
        "0": exit_application
    }

    while True:
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        choice = input("choice:\n")
        if choice not in commands:
            print("Invalid choice. Please try again.")
            continue

        result = commands[choice](data)
        if result is None:
            break