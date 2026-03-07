import sqlite3

def get_connection():
    connection = sqlite3.connect("card.s3db")
    connection.row_factory = sqlite3.Row  # lets you access columns by name
    return connection

def checkLuhn(cardNo):
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False

    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')

        if (isSecond == True):
            d = d * 2

        # We add two digits to handle
        # cases that make two digits after
        # doubling
        nSum += d // 10
        nSum += d % 10

        isSecond = not isSecond

    if (nSum % 10 == 0):
        return True
    else:
        return False

def add_income(card_number, income):
    card_tuple = fetch_db_card_data(card_number)
    balance = card_tuple["balance"]
    balance += income
    update_db_card_data(card_number, balance=balance)
    return fetch_db_card_data(card_number)["balance"]

def remove_income(card_number, income):
    card_tuple = fetch_db_card_data(card_number)
    balance = card_tuple["balance"]
    balance -= income
    update_db_card_data(card_number, balance=balance)
    return fetch_db_card_data(card_number)["balance"]

def delete_db_tuple(card_number):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM card WHERE number = ?", (card_number,))
    deleted = cursor.rowcount
    connection.commit()
    connection.close()
    return deleted # 1 if deleted, 0 if card wasn't found

def update_db_card_data(card_number, **kwargs):
    connection = get_connection()
    cursor = connection.cursor()
    query = "UPDATE card SET "
    values = []
    for key, value in kwargs.items():
        query += f"{key} = ?, "
        values.append(value)
    query = query[:-2] + " WHERE number = ?"
    values.append(card_number)
    cursor.execute(query, tuple(values))
    connection.commit()
    connection.close()

def fetch_db_card_data(card_number):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM card WHERE number = ?", (card_number,))
    card_tuple = cursor.fetchone()
    connection.close()
    return card_tuple

def lookup_card(card_number):
    card_tuple = fetch_db_card_data(card_number)
    if card_tuple:
        return True
    else:
        return False

def match_pin(card_number, pin):
    card_tuple = fetch_db_card_data(card_number)
    if card_tuple["pin"] == pin:
        return True
    else:
        return False