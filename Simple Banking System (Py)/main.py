from handlers import *

def main():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")
    connection.commit()

    data = {}
    main_menu(data)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()
