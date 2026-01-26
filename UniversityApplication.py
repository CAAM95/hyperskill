
import os
import json
import copy

def convert_to_json():
    path = os.getcwd()
    json_path = os.path.join(path, "applicants.json")

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump({}, json_file, indent=4)


    with open(json_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    with open(os.getcwd() + "\\applicants.txt", 'r', encoding='utf-8') as txt_file:
        student_id = 0
        for line in txt_file:
            json_data[student_id] = process_student(line)
            student_id += 1

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=4)


def read_json():
    path = os.getcwd()
    json_path = os.path.join(path, "applicants.json")
    with open(json_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)



def process_student(stringy):
    stringy_parts = stringy.split()
    json_entry = {
        "first_name": stringy_parts[0],
        "last_name": stringy_parts[1],
        "academics" : {
            "physics": stringy_parts[2],
            "chemistry": stringy_parts[3],
            "math": stringy_parts[4],
            "compsci": stringy_parts[5]
        },
        "special_exam": stringy_parts[6],
        "deptartment_a": stringy_parts[7],
        "deptartment_b": stringy_parts[8],
        "deptartment_c": stringy_parts[9]
    }
    return json_entry


def sort_dept_by_ids(students, choice):
    department_ids = {
        "Physics": [],
        "Chemistry": [],
        "Mathematics": [],
        "Engineering": [],
        "Biotech": []
    }

    for student in list(students.keys()):
        dept = students[student][choice]
        department_ids[dept].append(student)
    return department_ids


def print_accepted_students(dept_student_dic, all_students, lookup_table):
    for dept in sorted(dept_student_dic):
        students = dept_student_dic[dept]
        students = sorted(students, key=lambda id: (-float(get_score(all_students[id], dept, lookup_table)),
                                                    all_students[id]["first_name"] + " " + all_students[id]["last_name"]))
        with open(f"{dept.lower()}.txt", 'w') as file:
            for student in students:
                student_details = all_students[student]
                first_name = student_details["first_name"]
                last_name = student_details["last_name"]
                score = get_score(student_details, dept, lookup_table)
                file.write(f"{first_name} {last_name} {score}\n")


def get_score(student, department, lookup_table):
    subjects = lookup_table[department]
    grade = 0.0
    admission_exam_grade = int(student["special_exam"])

    for subject in subjects:
        subject_grade = student["academics"][subject]
        grade += float(subject_grade)

    mean_grade = grade / len(subjects)

    if admission_exam_grade > mean_grade:
        return admission_exam_grade
    else:
        return mean_grade

def lookup_grade_given_choice_x(student_details, choice, lookup_table):
    choice = student_details[choice]
    subjects = lookup_table[choice]
    grade = 0.0
    admission_exam_grade = int(student_details["special_exam"])

    for subject in subjects:
        subject_grade = student_details["academics"][subject]
        grade += float(subject_grade)

    mean_grade = grade / len(subjects)

    if admission_exam_grade > mean_grade:
        return admission_exam_grade
    else:
        return mean_grade

def main():
    convert_to_json()
    students_json = read_json()
    remaining_students = copy.deepcopy(students_json)

    max_applicants = int(input())

    student_choices = ["deptartment_a", "deptartment_b", "deptartment_c"]
    department_ids = {
        "Physics": [],
        "Chemistry": [],
        "Mathematics": [],
        "Engineering": [],
        "Biotech": []
    }

    student_choices = ["deptartment_a",
                       "deptartment_b",
                       "deptartment_c"
                       ]

    lookup_table = {
        "Engineering": ["compsci","math"],
        "Biotech": ["chemistry", "physics"],
        "Chemistry": ["chemistry"],
        "Mathematics": ["math"],
        "Physics": ["physics", "math"]
    }

    for choice in student_choices:
        depts_to_ids = sort_dept_by_ids(remaining_students, choice)
        depts_sorted_aplha = dict(sorted(depts_to_ids.items(), key=lambda x: x[0]))
        depts_sorted_alpha_gpa = {}

        for department, ids in depts_sorted_aplha.items():
            depts_sorted_alpha_gpa[department] = sorted(ids, key=lambda id: (-float(lookup_grade_given_choice_x(remaining_students[id], choice, lookup_table)),f"{remaining_students[id]['first_name']} {remaining_students[id]['last_name']}"))

        for  department, ids in depts_sorted_alpha_gpa.items():
            current_len = len(department_ids[department])
            spots_available = max_applicants - current_len
            if spots_available > 0:
                for id in ids[:spots_available]:
                    department_ids[department].append(id)
                    if id in remaining_students:
                        del remaining_students[id]

    print_accepted_students(department_ids, students_json, lookup_table)

if __name__== "__main__":
    standard_input = "25"
    main()

