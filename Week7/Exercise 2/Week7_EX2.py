import Week7_EX1 as factory
import platform
import csv

# Custom exception class
class NotEnoughStudentsException(Exception):
    
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

def get_3_almost_graduated_students(student_list):
    if len(student_list) >= 3:
        sorted_students = sorted(student_list, key=lambda student: student.get_progress(), reverse=True)
        res = []
        for i in range(3):
            res.append(sorted_students[i])
        return res
    else:
        raise NotEnoughStudentsException("Not enough students in list")

def save_3_almost_graduated_students(student_list, file_path):
    try:
        save_list = get_3_almost_graduated_students(student_list)
        factory.save_student_list(save_list, file_path)
    except NotEnoughStudentsException as e:
        #Save error in file
        if platform.system() == 'Windows':
            newline=''
        else:
            newline=None
        try:
            with open(file_path, 'w', newline=newline) as save_file:
                writer = csv.writer(save_file)
                writer.writerow({"Could not extract 3 students - given list was too short"})
                print(e.args[0])
        except OSError as e:
            print("Failed to write to file")
            print(e)
    except OSError as e:
        print("Failed to write to file")
        print(e)
    else:
        print("Everything went well...")

student_list = factory.create_random_students(2)
#three_students = get_3_almost_graduated_students(student_list)
#factory.print_students(three_students)
save_3_almost_graduated_students(student_list, "./download_dumps/almost_graduated_students.csv")
