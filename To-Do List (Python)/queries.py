from sql import Table
from utilities import get_today

def add_task(session, task_name, deadline):
    new_task = Table(task=task_name, deadline=deadline)
    session.add(new_task)
    session.commit()
    return new_task

def get_all_tasks(session):
    return session.query(Table).order_by(Table.deadline).all()

def filter_tasks(session, date=None):
    if date is None:
        date = get_today()
    return session.query(Table).filter(Table.deadline == date).all()

def delete_task(session, task_id):
    task = session.query(Table).filter_by(id=task_id).first()
    if task:
        session.delete(task)
        session.commit()
    return task


def find_missed_tasks(session):
    todays_date = get_today()
    tasks_by_deadline = get_all_tasks(session)
    missed_tasks = []

    for task in tasks_by_deadline:
        if task.deadline < todays_date:
            missed_tasks.append(task)
    return missed_tasks