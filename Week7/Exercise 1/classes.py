
class Course():
    """A course class that contains name, classroom, teacher's name, ECTS points and optional grade"""

    def __init__(self, name, classroom, teacher, ECTS, grade=None):
        """Initialize course"""
        self.name = name
        self.classroom = classroom
        self.teacher = teacher
        self.ECTS = ECTS
        self.grade = grade
    
    def __repr__(self):
        return 'Course(%r, %r, %r, %r, %r)' % (self.name, self.classroom, self.teacher, self.ECTS, self.grade)

class DataSheet():
    """A data sheet class that contains courses"""
    
    def __init__(self, courses=[]):
        """Initialize courses"""
        self.courses = courses

    def __repr__(self):
        return 'DataSheet(%r)' % (self.courses)

    def get_grades_as_list(self):
        grades = []
        for course in self.courses:
            grades.append(int(course.grade))
        return grades


class Student():
    """A student class consisting of student name, gender, data about what they study 
    and an URL to an image of them"""

    def __init__(self, name, gender, data_sheet, image_url,):
        """Initialize name, gender, data_sheet and image_url."""
        self.name = name 
        self.gender = gender
        self.data_sheet = data_sheet
        self.image_url = image_url
    
    def __repr__(self):
        return 'Student(%r, %r, %r, %r)' % (self.name, self.gender, self.data_sheet, self.image_url)
    
    def __str__(self):
        return 'Student: {name}\nGender: {gender}\nAmount of courses: {sheet}\nImage URL: {image}'.format(
            name=self.name, gender=self.gender, sheet=len(self.data_sheet.courses), image=self.image_url)
    
    def get_courses(self):
        return self.data_sheet.courses

    def get_avg_grade(self):
        avg_grade = 0
        all_grades = self.data_sheet.get_grades_as_list()
        for grade in all_grades:
            avg_grade += grade
        avg_grade = avg_grade / len(all_grades)
        return avg_grade
    
    def get_progress(self):
        progress = 0
        for course in self.data_sheet.courses:
            progress += int(course.ECTS)
        total_progress = progress / 150 * 100
        return total_progress
