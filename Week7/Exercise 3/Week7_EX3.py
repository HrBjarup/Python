import matplotlib.pyplot as plt
import Week7_EX1 as factory

def show_pie_student_progress(student_list):
    #Amount of students with given progress
    ECTS_count = {}

    for student in student_list:
        progress = student.get_progress()
        #Using "%.2f" % to shorten the floats
        if not ECTS_count.get("%.2f" % progress):
            ECTS_count["%.2f" % progress] = 1
        else:
            ECTS_count[ "%.2f" % progress] += 1

    # Pie chart
    #explode = (0.1, 0.2, 0, 0) # offset second slice
    fig1, ax1 = plt.subplots() # first returned is the containing figure (fig1), then the subplot Axe object(s) (ax1)
    ax1.pie(ECTS_count.values(), labels=ECTS_count.keys(), autopct=lambda p:'{:.2f}%({:.0f})'.format(p,(p/100)*sum(ECTS_count.values())), 
            #autopct=make_autopct(ECTS_count.values()), 
            #autopct='%.1f', 
            # autopct= a format string like '%1.2f%%' for showing pct sign and 2 decimals
            shadow=True, startangle=90)
    ax1.set_aspect('equal')
    ax1.legend(ECTS_count.keys(), loc='upper right') # use instead of labels in ax1.pie(...)
    #ax1.axis('equal')  
    #plt.tight_layout()
    plt.show()

#students = factory.create_random_students(12)
#show_pie_student_progress(students)

def show_bar_chart_course_stats(student_list):
    courses = {}

    for student in student_list:
        current_courses = student.get_courses()
        for course in current_courses:
            if course.name not in courses.keys():
                courses[course.name] = 1
            else:
                courses[course.name] += 1
            

    plt.bar(courses.keys(), courses.values(), width=0.9, align='center')

    plt.axis([0, len(courses) + 1, 0, len(student_list)])
    plt.title("Course statistics", fontsize=12)
    plt.xlabel("Course name", fontsize=10,)
    plt.ylabel("Amount of students taking the course", fontsize=10)
    #Making and empty space before the first shown person in the chart:
    plt.xlim(-1, len(courses))
    #Rotate x axis labels:
    plt.xticks(rotation=17)
    plt.tick_params(axis='both', which='major', labelsize=10)

    plt.show()

#students = factory.create_random_students(12)
#show_bar_chart_course_stats(students)

# --- Gender specific version ---
def show_bar_chart_course_stats_w_gender(student_list):
    male_list = []
    female_list = []
    
    courses_m = {}
    courses_f = {}

    for student in student_list:
        if student.gender == "Male":
            male_list.append(student)
        else:
            female_list.append(student)

    def loop(output, data_list):
        """Helper method"""
        for student in data_list:
            current_courses = student.get_courses()
            for course in current_courses:
                if course.name not in output:
                    output[course.name] = 1
                else:
                    output[course.name] += 1
        
    loop(courses_m, male_list)
    loop(courses_f, female_list)

    total_amount_of_courses = 0
    if len(courses_m) > len(courses_f):
        total_amount_of_courses = len(courses_m)
    else:
        total_amount_of_courses = len(courses_f)


    ax = plt.subplot(111)
    ax.bar(courses_m.keys(), courses_m.values(), width=0.3, color='b', align='center')
    ax.bar(courses_f.keys(), courses_f.values(), width=0.2, color='r', align='center')

    #plt.bar(courses.keys(), courses.values(), width=0.9, align='center')

    plt.axis([0, total_amount_of_courses + 1, 0, len(student_list)])
    plt.title("Course statistics - Male = blue | Female = red", fontsize=12)
    plt.xlabel("Course name", fontsize=10,)
    plt.ylabel("Amount of students taking the course", fontsize=10)
    #Making and empty space before the first shown person in the chart:
    plt.xlim(-1, total_amount_of_courses)
    #Rotate x axis labels:
    plt.xticks(rotation=17)
    plt.tick_params(axis='both', which='major', labelsize=10)

    plt.show()

students = factory.create_random_students(12)
show_bar_chart_course_stats_w_gender(students)