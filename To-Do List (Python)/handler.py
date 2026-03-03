import queries
import utilities

def menu(session):
    commands = {
        "1": get_tasks_today,
        "2": get_tasks_week,
        "3": get_tasks_all,
        "4": get_missed_tasks,
        "5": get_task,
        "6": remove_task,
        "0": exit_application
    }

    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add a task")
    print("6) Delete a task")
    print("0) Exit")

    while True:
        choice = input("command: ")

        if choice not in (key for key in commands.keys()):
            print("Not a valid choice. Try again.")
            continue

        result = commands[choice](session)

        if not result:
            break

def get_missed_tasks(session):
    print("Missed tasks:")

    tasks = queries.find_missed_tasks(session)
    if not tasks:
        print("All tasks have been completed!")
        return True
    else:
        print_tasks(tasks, "all")
    print()
    return tasks

def get_tasks_today(session):
    day_name, day, month = utilities.format_date()
    print(f"Today {day} {month}:")

    tasks = queries.filter_tasks(session)
    if not tasks:
        print("Nothing to do!")
        return True
    else:
        print_tasks(tasks)
    return tasks

def get_tasks_week(session):
    dates = utilities.find_dates_of_the_week()
    for date in dates:
        day_name, day, month = utilities.format_date(date)
        print(f"{day_name} {day} {month}:")

        tasks = queries.filter_tasks(session, date)
        if not tasks:
            print("Nothing to do!")
        else:
            print_tasks(tasks)

        print()
    return dates

def print_tasks(tasks, mode=None):
    for i, task in enumerate(tasks):
        day_name, day, month = utilities.format_date(task.deadline)
        if mode == "all":
            print(f"{i+1}. {task.task}. {day} {month}")
        else:
            print(f"{i+1}. {task}")

def get_tasks_all(session):
    tasks = queries.get_all_tasks(session)
    if not tasks:
        print("Nothing to do!")
        return True
    else:
        print_tasks(tasks, "all")
    return tasks

def get_task(session):
    name = input("Enter a task: ")
    deadline = utilities.parse_time(input("Enter a deadline: ")) # 2020-04-28
    task = queries.add_task(session, name, deadline)
    print(f"The task has been added!")
    return task

def remove_task(session):
    print("Choose the number of the task you want to delete:")
    tasks = get_tasks_all(session)
    print(tasks)
    task_number = int(input())
    task = tasks[task_number - 1]
    deleted_task = queries.delete_task(session, task.id)
    print(f"{deleted_task} has been deleted!")
    return deleted_task

def exit_application(session):
    return None