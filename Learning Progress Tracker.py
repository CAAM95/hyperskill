# Classes
class Id_Manager():
    def __init__(self, counter):
        self.counter = counter

    def generate_id(self):
        self.counter += 1
        return self.counter

class Student():
    def __init__(self, id, first_name, last_name, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def get_student_infomation(self):
        return [self.id, self.first_name, self.last_name, self.email]

class Course():
    def __init__(self, id, name):
        self.id = id
        self.name = name



# Application
def handle_add_student(student_db, id_manager):
    print("Enter student credentials or 'back' to return.")
    student_lst = []
    while True:

        user_input = input().strip()
        if user_input == "":
            print("Incorrect credentials")
            continue

        if user_input == "back":
            break

        tokens = user_input.split()
        if len(tokens) < 3:
            print("Incorrect credentials")
            continue

        first_name = tokens[0]
        last_name = "".join(tokens[1:-1])
        email = tokens[-1]

        if is_valid_name(first_name) == False:
            print("Incorrect first name")
            continue
        if is_valid_name(last_name) == False:
            print("Incorrect last name")
            continue
        if is_valid_email(email) == False:
            print("Incorrect email")
            continue
        if is_unique_email(student_db, email) == False:
            print("This email is already taken.")
            continue

        student = Student(id_manager.generate_id(), first_name, last_name, email)

        student_lst.append(student)
        student_db[student.id] = student
        print("The student has been added.")

    return student_lst


def handle_add_points(students_db, records):
    print("Enter an id and points or 'back' to return")
    while True:
        user_input = input().strip()
        if user_input == "":
            print("Incorrect points format.")
            continue

        if user_input == "back":
            break

        tokens = user_input.split()
        if len(tokens) < 5 or len(tokens) > 5:
            print("Incorrect points format.")
            continue

        try:
            student_id = int(tokens[0])
        except ValueError:
            print(f"No student is found for id={tokens[0]}.")
            continue

        is_valid_id = False
        for id_key in students_db.keys():
            if int(id_key) == student_id:
                is_valid_id = True
                break

        if is_valid_id != True:
            print(f"No student is found for id={student_id}.")
            continue

        is_valid_grade = True
        student_grades = tokens[1:]
        try:
            student_grades = [int(grade) for grade in student_grades]
        except ValueError:
            print("Incorrect points format.")
            continue


        for grade in student_grades:
            if grade < 0:
                print("Incorrect points format.")
                is_valid_grade = False
                break

        if is_valid_grade != True:
            continue

        records[student_id].append([student_grades[0], student_grades[1], student_grades[2], student_grades[3]])

        print("Points updated.")


def handle_find(students_db, records):
    print("Enter an id and points or 'back' to return")
    while True:
        user_input = input().strip()
        if user_input == "":
            print("No student is found for id={}")
            continue

        if user_input == "back":
            break

        try:
            student_id = int(user_input)
        except ValueError:
            print(f"No student is found for id={user_input}")
            continue

        is_valid_id = False
        for id_key in students_db.keys():
            if int(id_key) == student_id:
                is_valid_id = True
                break

        if is_valid_id != True:
            print(f"No student is found for id={user_input}.")
            continue

        student_records = records[student_id]
        sum_of_grades_lst = add_student_points(student_records)
        print(f"{student_id} points: Python={sum_of_grades_lst[0]}; DSA={sum_of_grades_lst[1]}; Databases={sum_of_grades_lst[2]}; Flask={sum_of_grades_lst[3]}")


def handle_statistics(records):
    print("Type the name of a course to see details or 'back' to quit:")
    stats_report = get_class_stats(records)
    student_count_lst = stats_report["student_count"]
    task_activity_lst = stats_report["task_count"]
    total_grades_lst = stats_report["total_grades"]

    course_lst = ["python", "dsa", "databases", "flask"]

    most_popular = []
    least_popular = []
    highest_activity = []
    lowest_activity = []
    easiest_course = []
    hardest_course = []


    for index in range(len(course_lst)):
        if max(student_count_lst) == 0:
            continue

        if student_count_lst[index] == max(student_count_lst):
            most_popular.append(course_lst[index])
        elif student_count_lst[index] == min(student_count_lst):
            least_popular.append(course_lst[index])

        if task_activity_lst[index] == max(task_activity_lst):
            highest_activity.append(course_lst[index])
        elif task_activity_lst[index] == min(task_activity_lst):
            lowest_activity.append(course_lst[index])

        if total_grades_lst[index] == max(total_grades_lst):
            easiest_course.append(course_lst[index])
        elif total_grades_lst[index] == min(total_grades_lst):
            hardest_course.append(course_lst[index])

    if most_popular:
        print(f"Most popular: {', '.join(most_popular)}")
    else:
        print(f"Most popular: n/a")
    if least_popular:
        print(f"Least popular: {', '.join(least_popular)}")
    else:
        print(f"Least popular: n/a")

    if highest_activity:
        print(f"Highest activity: {', '.join(highest_activity)}")
    else:
        print(f"Highest activity: n/a")

    if lowest_activity:
        print(f"Lowest activity: {', '.join(lowest_activity)}")
    else:
        print(f"Lowest activity: n/a")

    if easiest_course:
        print(f"Easiest course: {', '.join(easiest_course)}")
    else:
        print(f"Easiest course: n/a")

    if hardest_course:
        print(f"Hardest course: {', '.join(hardest_course)}")
    else:
        print(f"Hardest course: n/a")

    while True:
        user_input = input().strip()
        if user_input == "back":
            break

        if user_input.lower() not in course_lst:
            print("Unknown course.")
            continue

        print_class_stats(user_input, records)

def handle_notify(students_db, records, notified_ids):
    students = {}
    max_grades = [600, 400, 480, 550]
    courses = ["Python", "DSA", "Databases", "Flask"]
    emails = []

    for student_id, student_records in records.items():
        total_grades = [0, 0, 0, 0]
        grades = add_student_points(student_records)

        for i in range(len(grades)):
            total_grades[i] += grades[i]

        students[student_id] = total_grades

    for student_id, grades in students.items():
        for i in range(len(grades)):
            if grades[i] >= max_grades[i]:
                emails.append([
                    student_id,
                    students_db[student_id].first_name,
                    students_db[student_id].last_name,
                    students_db[student_id].email,
                    courses[i]
                ])

    ids = set()
    for email in emails:
        if email[0] in notified_ids:
            continue
        ids.add(email[0])
        print_email(email[3], email[1], email[2], email[4])

    print(f"Total {len(ids)} students have been notified.")
    return ids


def print_class_stats(course_name, records):
    student_data = []

    for student_id, student_records in records.items():
        total_grades = [0, 0, 0, 0]
        grades = add_student_points(student_records)

        for i in range(len(grades)):
            total_grades[i] += grades[i]

        student_data.append({student_id: total_grades})

    python_students = []
    dsa_students = []
    databases_students = []
    flask_students = []

    for i in range(len(student_data)):
        for id, grades in student_data[i].items():
            if grades[0] > 0:
                python_students.append({id: grades[0]})
            if grades[1] > 0:
                dsa_students.append({id: grades[1]})
            if grades[2] > 0:
                databases_students.append({id: grades[2]})
            if grades[3] > 0:
                flask_students.append({id: grades[3]})

    if course_name.lower() == "python":
        print_student_grades("python", python_students, 600)
    if course_name.lower() == "dsa":
        print_student_grades("dsa", dsa_students, 400)
    if course_name.lower() == "databases":
        print_student_grades("databases", databases_students, 480)
    if course_name.lower() == "flask":
        print_student_grades("flask", flask_students, 550)

def print_student_grades(course_name, students, max_points):
    if course_name == "dsa":
        print(course_name.upper())
    else:
        print(course_name.title())

    print(f"{'id':<8}{'points':<10}{'completed':<12}")
    records = []
    for student in students:
        for id, grades in student.items():
            records.append([id, grades, grades / max_points * 100])

    records.sort(key=lambda x: x[1], reverse=True)
    records.sort(key=lambda x: (-x[1], x[0]))

    for record in records:
        print(f"{record[0]:<8}{record[1]:<10}{record[2]:.1f}%")


def print_email(email_address, first_name, last_name, course_name):
    print(f"To: {email_address}\nRe: Your Learning Progress \nHello, {first_name} {last_name}! You have accomplished our {course_name} course!")

# LOGIC (focused, input driven, return based, effect free)

def add_student_points(lst_of_grades):
    sum_of_grades_lst = [0, 0, 0, 0]

    for grades in lst_of_grades:
        for i in range(4):
            sum_of_grades_lst[i] += grades[i]

    return sum_of_grades_lst

def get_class_stats(records):
    python_task_count = 0
    dsa_task_count = 0
    databases_task_count = 0
    flask_task_count = 0

    python_student_count = 0
    dsa_student_count = 0
    databases_student_count = 0
    flask_student_count = 0

    total_grades = [0, 0, 0, 0]

    for student_id, student_records in records.items():
        grades = add_student_points(student_records)

        for i in range(len(grades)):
            total_grades[i] += grades[i]

        for i in range(len(student_records)):
            record = student_records[i]

            for j in range(len(record)):

                if j == 0 and record[j] > 0:
                    python_task_count += 1

                if j == 1 and record[j] > 0:
                    dsa_task_count += 1

                if j == 2 and record[j] > 0:
                    databases_task_count += 1

                if j == 3 and record[j] > 0:
                    flask_task_count += 1

        if grades[0] > 0:
            python_student_count += 1
        if grades[1] > 0:
            dsa_student_count += 1
        if grades[2] > 0:
            databases_student_count += 1
        if grades[3] > 0:
            flask_student_count += 1

    return {"task_count": [python_task_count, dsa_task_count, databases_task_count, flask_task_count],
            "student_count": [python_student_count, dsa_student_count, databases_student_count, flask_student_count],
            "total_grades": total_grades}



def is_valid_name(name):
    uppper_alphas = [65, 90]
    lower_alphas = [97, 122]
    allowed_specials = [45, 39]
    if len(name) == 1:
        return False
    if not name:
        return False
    if name.isdigit():
        return False
    if name[0] in {"'", "-"} or name[-1] in {"'", "-"}:
        return False
    for i in range(1, len(name)):
        if name[i] in {"'", "-"} and name[i - 1] in {"'", "-"}:
            return False

    for char in name:
        if char.isdigit():
            return False
        if not (
                uppper_alphas[0] <= ord(char) <= uppper_alphas[1]
                or lower_alphas[0] <= ord(char) <= lower_alphas[1]
                or ord(char) in allowed_specials
        ):
            return False

    return True

def is_valid_email(email):
    if not email:
        return False

    if "@" not in email:
        return False

    if "." not in email:
        return False

    if email.count("@") > 1 :
        return False

    return True

def is_unique_email(student_db, email):
    for elem in student_db.values():
        if elem.email == email:
            return False
    return True

def list_students(student_db):
    lst = []
    for student_id, student_obj in student_db.items():
        student_attrributes = student_obj.get_student_infomation()
        lst.append(student_attrributes)
    return lst



# UI (prints, input, program flow)
print("Learning Progress Tracker")

students_db = {}
records = {}
student_id_manager = Id_Manager(9999)
class_stats = {}
notified_ids = set()

while True:
    user_input = input().strip()
    if user_input == "":
        print("No input")
        continue

    if user_input == "add students":
        student_lst = handle_add_student(students_db, student_id_manager)
        for student in student_lst:
            records[student.id] = []

        print(f"Total {len(student_lst)} students have been added.")
        continue

    if user_input == "list":
        # get the list of student objects and put in a list of lists
        # if the len of the list is NOne
        # print no students found
        # print each students information inline
        studenst_lst = list_students(students_db)

        if len(studenst_lst) == 0:
            print("No students found")
            continue

        print("Students:")
        for student_attributes in studenst_lst:
            print(student_attributes[0])
        continue

    if user_input == "add points":
        handle_add_points(students_db, records)
        continue

    if user_input == "find":
        handle_find(students_db, records)
        continue

    if user_input == "statistics":
        class_stats = handle_statistics(records)
        continue
    if user_input == "notify":
        notified_ids = handle_notify(students_db, records, notified_ids)
        continue

    if user_input == "back":
        print("Enter 'exit' to exit the program")
        continue

    if user_input == "exit":
        print("Bye!")
        exit()

    print("Unknown command")

