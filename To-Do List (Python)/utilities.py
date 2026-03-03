from datetime import datetime, timedelta

def parse_time(user_input):
    return datetime.strptime(user_input, "%Y-%m-%d").date()

def find_dates_of_the_week():
    today = datetime.today().date()
    return [today + timedelta(days=i) for i in range(7)]

def format_date(date=None):
    if date is None:
        date = datetime.today().date()

    day_name = date.strftime('%A')
    day = date.day
    month = date.strftime('%b')

    return day_name, day, month

def get_today():
    return datetime.today().date()