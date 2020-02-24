import matplotlib.pyplot as plt
#Random selecter thing:
import secrets
#Used to make deep copies:
import copy
import platform
import csv
from custom_modules import classes
Course = classes.Course
DataSheet = classes.DataSheet
Student = classes.Student

# ---------------------------------
# --- DATA FOR STUDENT CREATION ---
# ---------------------------------
student_names_m = ["Johnny", "George", "Andy", "Dave", "Mathias", "Luke", "Simon", "Aiden"]
img_urls_m = ["https://www.flaticon.com/premium-icon/icons/svg/2589/2589017.svg", "https://www.flaticon.com/premium-icon/icons/svg/2589/2589026.svg",
"https://www.flaticon.com/premium-icon/icons/svg/2589/2589036.svg", "https://www.flaticon.com/premium-icon/icons/svg/2589/2589051.svg"]
img_urls_f = ["https://www.flaticon.com/premium-icon/icons/svg/2589/2589033.svg", "https://www.flaticon.com/premium-icon/icons/svg/2589/2589039.svg",
"https://www.flaticon.com/premium-icon/icons/svg/2589/2589067.svg", "https://www.flaticon.com/premium-icon/icons/svg/2589/2589116.svg"]
student_names_f = ["Izalith", "Hazel", "Jenny", "Kalinka", "Lana", "Katarina"]
genders = ["Male", "Female"]
grades = [-3, 0, 2, 4, 7, 10, 12]
fsjs = Course("FullStack JavaScript", "1.05", "Lars", 10)
security = Course("Security", "1.62", "Anders", 10)
python = Course("Python & Data Science", "1.60", "Thomas", 10)
gaming = Course("Game dev w/ Unity", "2.60", "Tobias", 10)
music = Course("Classical music", "2.62", "Mozart", 10)
java = Course("Java", "2.03", "Tobias", 30)
AP = Course("Advanced Programming", "1.03", "Tobias", 10)
web = Course("Web dev w/ Maven", "2.62", "Niels", 30)

courses = [fsjs, security, python, gaming, music, java, AP, web]

# -------------------------
# --- STUDENT GENERATOR ---
# -------------------------
def create_random_students(amount):
    """Generates a given amount of students based on hardcoded data"""
    students = []
    for i in range(amount):
        gender = secrets.choice(genders)
        
        if gender == "Male":
            name = secrets.choice(student_names_m)
            image_url = secrets.choice(img_urls_m)
        else:
            name = secrets.choice(student_names_f)
            image_url = secrets.choice(img_urls_f)
        
        temp_courses = copy.deepcopy(courses)
        student_courses = []
        
        for j in range(3):
            course = secrets.choice(temp_courses)
            temp_courses.remove(course)
            course.grade = secrets.choice(grades)
            student_courses.append(course)
        
        data_sheet = DataSheet(student_courses)
        
        student = Student(name, gender, data_sheet, image_url)

        students.append(student)
    return students

# -----------------------------
# --- STUDENT SAVE FUNCTION ---
# -----------------------------
def save_student_list(students, file_path):
    """Used to save a list of student objects in a .csv file"""
    if platform.system() == 'Windows':
        newline=''
    else:
        newline=None
    with open(file_path, 'w', newline=newline) as save_file:
        writer = csv.writer(save_file)
        writer.writerow(['stud_name', 'gender', 'course_name', 'teacher', 'ects', 'classroom', 'grade', 'img_url'])
        for student in students:
            for course in student.data_sheet.courses:
                writer.writerow([student.name, student.gender, course.name, course.teacher, course.ECTS, course.classroom, course.grade, student.image_url])
            writer.writerow(['-'])
    print("Saved generated students to: " + file_path)

# -----------------------------
# --- STUDENT LOAD FUNCTION ---
# -----------------------------
def load_students(file_path):
    """Used to load students from a .csv file."""
    students = []
    with open(file_path) as file_obj:
        reader = csv.reader(file_obj)
        next(reader)
        data_sheet = DataSheet([])
        student = Student('', '', data_sheet, '')
        for row in reader:
            if row[0] == '-':
                students.append(copy.deepcopy(student))
                student.name = ''
                data_sheet.courses = []
                continue
            if student.name == '':
                student.name = row[0]
                student.gender = row[1]
                student.image_url = row[7]
            course = Course(row[2], row[5], row[3], row[4], row[6])
            student.data_sheet.courses.append(course)

    return students

# ------------------------------
# --- STUDENT PRINT FUNCTION ---
# ------------------------------
def print_students(students):
    for student in students:
        print("Name: " + student.name + "\nImage URL: " + student.image_url + "\nAvg grade: ", student.get_avg_grade(), "\n")

# Creating data etc.
#stdts = create_random_students(5)
#save_student_list(stdts, "./download_dumps/students.csv")
#students = load_students("./download_dumps/students.csv")
#sorted_students = sorted(students, key=lambda student: student.get_avg_grade(), reverse=True)
#print_students(sorted_students)

# ----------------------
# --- STUDENT GRADES ---
# ----------------------
def create_and_show_grade_chart(sorted_student_list):
    student_names = []
    student_avg_grades = []
    for i in range(len(sorted_student_list)):
        student_names.append("{i} ".format(i = i + 1) + sorted_student_list[i].name)
        student_avg_grades.append(sorted_student_list[i].get_avg_grade())

    plt.bar(student_names, student_avg_grades, width=0.9, align='center')

    plt.axis([-3, len(sorted_student_list) + 1, 0, 12])
    plt.title("Students", fontsize=12)
    plt.xlabel("Name", fontsize=10)
    plt.ylabel("AVG grade", fontsize=10)
    #Making and empty space before the first shown person in the chart:
    plt.xlim(-1, len(sorted_student_list))
    plt.tick_params(axis='both', which='major', labelsize=10)

    plt.show()

#create_and_show_grade_chart(sorted_student_list)

# ------------------------
# --- STUDENT PROGRESS ---
# ------------------------
def create_and_show_progress_chart(student_list):
    #ECTS progress
    x_values = set([])
    #Amount of students with given progress
    temp_y_values = {}
    y_values = []

    for student in student_list:
        progress = student.get_progress()
        x_values.add(progress)
        if not temp_y_values.get(progress):
            temp_y_values[progress] = 1
        else:
            temp_y_values[progress] += 1

    x_values = sorted(x_values, key=lambda value: value)
    for key in sorted(temp_y_values.keys()):
        y_values.append(temp_y_values[key])

    plt.bar(x_values, y_values, width=0.9, align='center')

    plt.axis([0, max(x_values) + 5, 0, max(y_values) + 1])
    plt.title("Students' ECTS progress", fontsize=12)
    plt.xlabel("Progress (in %)", fontsize=10)
    plt.ylabel("Amount of students", fontsize=10)
    #Making and empty space before the first shown person in the chart:
    plt.tick_params(axis='both', which='major', labelsize=10)

    plt.show()

#create_and_show_progress_chart(students)




