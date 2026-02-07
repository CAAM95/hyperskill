# from arepl_dump import dump
from datetime import datetime

class Message:
    def __init__(self, message_type, date_time, contents):
        self.message_type = message_type
        self.date_time = date_time
        self.contents = contents

class Calendar:
    def __init__(self, messages):
        self.messages = messages

    def add_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def delete_message(self, message):
        self.messages.remove(message)

def find_difference_date_time(current_date_time, message_date_time):
    return abs(message_date_time - current_date_time)


def find_difference_date(current_date, message_date):
    current_date = current_date.date()
    try:
        target = datetime(current_date.year, message_date.month, message_date.day).date()
    except ValueError:
        target = datetime(current_date.year, message_date.month, message_date.day - 1).date()

    if target <= current_date:
        try:
            target = datetime(current_date.year + 1, message_date.month, message_date.day).date()
        except ValueError:
            target = datetime(current_date.year + 1, message_date.month, message_date.day - 1).date()

    return target - current_date


def calc_age(message):
    now = datetime.now().replace(second=0, microsecond=0)
    birth_year = message.date_time.year
    birthday_this_year = datetime(
        now.year,
        message.date_time.month,
        message.date_time.day
    ).date()

    age = now.year - birth_year
    if birthday_this_year > now.date():
        age -= 1
    return age

def create_note_notification(contents, days, hours, minutes):
    return f'Note: "{contents}" - {days} day(s), {hours} hour(s), {minutes} minute(s)'

def create_birthday_notification(contents, days, age):
    return f'Birthday: "{contents} (turns {age + 1})" - {days} day(s)'

def construct_note_notification(message):
    now = datetime.now().replace(second=0, microsecond=0)
    delta = find_difference_date_time(now, message.date_time)
    days, hours, minutes, seconds = format_delta(delta)
    notification = create_note_notification(message.contents, days, hours, minutes)
    return notification

def construct_birthday_notification(message):
    now = datetime.now().replace(second=0, microsecond=0)
    delta = find_difference_date(now, message.date_time)
    days, hours, minutes, seconds = format_delta(delta)
    age = calc_age(message)
    notification = create_birthday_notification(message.contents, days, age)
    return notification

def format_delta(delta):
    total_seconds = int(delta.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return days, hours, minutes, seconds

def handle_add_type():
    while True:
        message_type = input("Specify type (note, birthday): ")
        if message_type in ("note", "birthday"):
            return message_type
        print("Incorrect type")

def handle_add_count(message_type):
    while True:
        try:
            prompt = (
                "How many notes would you like to add: "
                if message_type == "note"
                else "How many dates of birth: "
            )
            count = int(input(prompt))
            if count > 0:
                return count
            print("Incorrect number")
        except ValueError:
            print("Incorrect number")

def is_leap_year(year):
    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)

def max_days_in_month(year, month):
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif month in (4, 6, 9, 11):
        return 30
    elif month == 2:
        return 29 if is_leap_year(year) else 28
    return 0

def tokenize_datetime(input_str):
    parts = input_str.replace("-", " ").replace(":", " ").split()
    if len(parts) not in (3, 5):
        return None
    return parts

def is_semantically_valid(parts):
    try:
        nums = list(map(int, parts))
    except ValueError:
        return False

    year, month, day = nums[0], nums[1], nums[2]

    if not (1 <= month <= 12):
        return False

    max_day = max_days_in_month(year, month)
    if not (1 <= day <= max_day):
        return False

    if len(nums) == 5:
        hour, minute = nums[3], nums[4]
        if not (0 <= hour <= 23):
            return False
        if not (0 <= minute <= 59):
            return False

    return True



def parse_datetime(input_str, parts_len):
    try:
        if parts_len == 3:
            return datetime.strptime(input_str, "%Y-%m-%d")
        else:
            return datetime.strptime(input_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return None

def print_birthdays(birthdays):
    if birthdays:
        for message in birthdays:
            handle_add_print_message(message[1])

def print_notes(notes):
    if notes:
        for message in notes:
            handle_add_print_message(message[1])

def filter_messages(messages, option=None, user_input=None):
    now = datetime.now().replace(second=0, microsecond=0)
    # minimum sort
    notes = []
    birthdays = []

    if not messages:
        return None, None

    for message in messages:
        if message.message_type == "note":
            notes.append(message)
        else:
            birthdays.append(message)

    sorted_notes = []
    for message in notes:
        delta = find_difference_date_time(now, message.date_time)
        days, hours, minutes, seconds = format_delta(delta)
        key = (days, hours, minutes, seconds)   # sort key
        sorted_notes.append((key, message))
    sorted_notes.sort(key=lambda x: x[0])

    sorted_bdays = []
    for message in birthdays:
        delta = find_difference_date(now, message.date_time)
        days, hours, minutes, seconds = format_delta(delta)
        key = (days, hours, minutes, seconds)   # sort key
        sorted_bdays.append((key, message))
    sorted_bdays.sort(key=lambda x: x[0])

    return sorted_notes, sorted_bdays

def handle_date_validation(i, message_type):
    while True:
        if message_type == "note":
            user_input = input(f'{i + 1}. Enter datetime in "YYYY-MM-DD HH:MM" format: ')
        elif message_type == "birthday":
            user_input = input(f'{i + 1}. Enter date of birth in "YYYY-MM-DD" format: ')

        # Stage 1 — tokenize
        parts = tokenize_datetime(user_input)
        if not parts:
            print("Incorrect format")
            continue

        # Stage 1.5 — enforce type-specific shape
        if message_type == "birthday" and len(parts) != 3:
            print("Incorrect format")
            continue
        if message_type == "note" and len(parts) != 5:
            print("Incorrect format")
            continue

        # Stage 2 — semantic validation
        if not is_semantically_valid(parts):
            print("Incorrect date or time values")
            continue

        # Stage 3 — format validation
        date_time = parse_datetime(user_input, len(parts))
        if not date_time:
            print("Incorrect format")
            continue

        if message_type == "note":
            contents = input("Enter text: ")
        elif message_type == "birthday":
            contents = input("Enter name: ")

        return date_time, contents

def handle_add_messages(calendar, message_type, count):
    messages = []
    for i in range(count):
        date_time, contents = handle_date_validation(i, message_type)
        messages.append(Message(message_type, date_time, contents))

    for message in messages:
        calendar.add_message(message)


    return messages

def handle_add_print_message(message):
    if message.message_type == "birthday":
        notification = construct_birthday_notification(message)
        print(notification)
    else:
        notification = construct_note_notification(message)
        print(notification)

def handle_add(calendar):
    message_type = handle_add_type()
    count = handle_add_count(message_type)
    messages = handle_add_messages(calendar, message_type, count)

    for message in messages:
        handle_add_print_message(message)

    update_file(calendar)

    return handle_main_menu

def update_file(calendar):
    messages = calendar.get_messages()
    with open("data.txt", "w") as file:
        for message in messages:
            if message.message_type == "note":
                dt_str = message.date_time.replace(second=0, microsecond=0).strftime("%Y-%m-%d %H:%M")
            else:
                dt_str = message.date_time.strftime("%Y-%m-%d")
            file.write(f"{message.message_type},{dt_str},{message.contents}\n")

def handle_view_filter():
    while True:
        filter_option = input('Specify filter (all, date, text, birthdays, notes, sorted): ').lower()
        if filter_option in ["all", "date", "text", "birthdays", "notes", "sorted"]:
            break
        print("Incorrect filter")
    return filter_option

def handle_view_date(birthdays, notes):
    while True:
        date = input("Enter date in \"YYYY-MM-DD\" format: ")
        parts = tokenize_datetime(date)
        if not parts or len(parts) != 3:
            print("Incorrect format")
            continue

        if not is_semantically_valid(parts):
            print("Incorrect date or time values")
            continue

        parsed = parse_datetime(date, len(parts))
        if not parsed:
            print("Incorrect format")
            continue

        date = parsed
        break

    if birthdays:
        for message in birthdays:
            if (message[1].date_time.month, message[1].date_time.day) == (date.month, date.day):
                handle_add_print_message(message[1])
    if notes:
        for message in notes:
            if message[1].date_time.date() == date.date():
                handle_add_print_message(message[1])

def handle_view_text(birthdays, notes):
    while True:
        text = input("Enter text: ")
        if not text:
            print("No text entered")
            continue
        break
    if birthdays:
        for message in birthdays:
            if text.lower() in message[1].contents.lower():
                handle_add_print_message(message[1])
    if notes:
        for message in notes:
            if text.lower() in message[1].contents.lower():
                handle_add_print_message(message[1])


def handle_view_sorted(calender):
    now = datetime.now().replace(second=0, microsecond=0)
    while True:
        sort_method = input("Specify way (ascending, descending): ")
        if sort_method not in ["ascending", "descending"]:
            print("Incorrect sort method")
            continue
        break

    messages = calender.get_messages()


    sorted_messages = []
    for message in messages:
        if message.message_type == "note":
            delta = find_difference_date_time(now, message.date_time)
        elif message.message_type == "birthday":
            delta = find_difference_date(now, message.date_time)

        days, hours, minutes, seconds = format_delta(delta)

        key = (
            days,
            hours,
            minutes,
            seconds,
            message.contents.lower()
        )
        sorted_messages.append((key, message))         # keep original msg!


    sorted_messages.sort(key=lambda x: x[0], reverse=sort_method == "descending")

    for _, message in sorted_messages:
        handle_add_print_message(message)
def handle_view(calendar):
    filter_option = handle_view_filter()

    notes, birthdays = filter_messages(calendar.get_messages())


    if filter_option == "all":
        print_birthdays(birthdays)
        print_notes(notes)
    elif filter_option == "date":
        handle_view_date(birthdays, notes)
    elif filter_option == "text":
        handle_view_text(birthdays, notes)
    elif filter_option == "birthdays":
        print_birthdays(birthdays)
    elif filter_option == "notes":
        print_notes(notes)
    elif filter_option == "sorted":
        handle_view_sorted(calendar)

    return handle_main_menu

def handle_delete(calendar):
    notes, birthdays = filter_messages(calendar.get_messages())

    messages = {}

    index = 1

    for message_list in [birthdays, notes]:
        if message_list:
            for message in message_list:
                messages[index] = message[1]
                index += 1
    if messages:
        for i, message in messages.items():
            if message.message_type == "birthday":
                notification = construct_birthday_notification(message)
            else:
                notification = construct_note_notification(message)
            print(f"{i}. {notification}")


    ids = input("Enter ids: ").strip()
    ids_lst = [part.strip() for part in ids.split(",") if part.strip()]

    if not ids:
        return handle_main_menu


    for id in ids_lst:
        try:
            calendar.delete_message(messages[int(id)])
        except (KeyError, ValueError):
            print(f"No message with id {id}")

    update_file(calendar)
    return handle_main_menu

def handle_exit(calendar):
    print("goodbye")
    exit()

def handle_main_menu(calendar):
    now = datetime.now().replace(second=0, microsecond=0)
    COMMANDS = {
        "add": handle_add,
        "view": handle_view,
        "delete": handle_delete,
        "exit": handle_exit
    }
    print("Current date and time:")
    print(now.strftime("%Y-%m-%d %H:%M"))

    while True:
        command = input("Enter the command (add, view, delete, exit): ")
        try:
            COMMANDS[command]
        except KeyError:
            print("Incorrect command")
            continue
        return COMMANDS[command]


def create_save_file():
    try:
        with open("data.txt", "r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        with open("data.txt", "w") as file:
            pass
        return []




def main():
    create_save_file()

    with open("data.txt", "r") as file:
        lines = file.readlines()

    calendar = Calendar([])

    for line in lines:
        text = line.strip().split(",")
        type = text[0]

        date_time = text[1]
        parts = tokenize_datetime(date_time)
        date_time = parse_datetime(date_time, len(parts))

        contents = text[2]
        message = Message(type, date_time, contents)
        calendar.add_message(message)

    handler = handle_main_menu(calendar)

    while handler:
        handler = handler(calendar)
        print()

if __name__ == "__main__":
    standard_input = "add", "note", "2", "2026-02-02 18:00", "A note at 18:00", "2026-02-02 12:00", "A note at 12:00", "add", "birthday", "2", "1995-10-14", "Chris Ascencio", "2015-06-24", "Ian Ascencio", "view", "all", "view", "birthdays", "view", "notes", "view", "date", "1995-10-14", "add", "birthday", "1", "1995-10-15", "Emily Mancia", "view", "all", "view", "birthdays", "view", "date", "1995-10-15", "view", "date", "2026-02-02"
    main()
