"""
OOP-Class-And-Object-Lab — Student Record Management System
Concepts: Classes, Objects, Constructors, Methods, Attributes
Author  : Kushagra Bansal — Project Lab India
Run     : python main.py
"""
from datetime import datetime, date

class Address:
    """Value object representing a physical address"""
    def __init__(self, street, city, state, pincode):
        self.street  = street
        self.city    = city
        self.state   = state
        self.pincode = pincode

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} - {self.pincode}"

    def __repr__(self):
        return f"Address(city={self.city!r}, state={self.state!r})"


class Course:
    """Represents a course with grade tracking"""
    GRADE_MAP = {
        (90, 101): "A+", (80, 90): "A", (70, 80): "B+",
        (60, 70): "B",   (50, 60): "C", (0,  50): "F"
    }

    def __init__(self, code, name, credits):
        self.code    = code
        self.name    = name
        self.credits = credits
        self.score   = None

    def set_score(self, score):
        if not 0 <= score <= 100:
            raise ValueError(f"Score must be 0-100, got {score}")
        self.score = score

    def get_grade(self):
        if self.score is None:
            return "N/A"
        for (lo, hi), grade in self.GRADE_MAP.items():
            if lo <= self.score < hi:
                return grade
        return "F"

    def __str__(self):
        return f"{self.code} | {self.name:<25} | Credits: {self.credits} | Score: {self.score or 'N/A':>5} | Grade: {self.get_grade()}"


class Student:
    """Core Student class demonstrating all fundamental OOP concepts"""

    # Class variable — shared across all instances
    _total_students   = 0
    _institution_name = "Project Lab India University"

    def __init__(self, name, roll_number, branch, year, dob):
        # Instance variables — unique to each object
        self.name        = name
        self.roll_number = roll_number
        self.branch      = branch
        self.year        = year
        self.dob         = dob
        self.courses     = []
        self.address     = None
        self.enrolled_on = datetime.now()

        # Increment class counter
        Student._total_students += 1

    # ── Instance Methods ─────────────────────────────────────
    def enroll_course(self, course):
        """Add a course to student's enrollment"""
        if any(c.code == course.code for c in self.courses):
            raise ValueError(f"Already enrolled in {course.code}")
        self.courses.append(course)
        print(f"  ✅ {self.name} enrolled in {course.name}")

    def set_address(self, address):
        """Set student's home address"""
        self.address = address

    def calculate_cgpa(self):
        """Calculate cumulative GPA from enrolled courses"""
        scored = [c for c in self.courses if c.score is not None]
        if not scored:
            return 0.0
        total_points  = sum(c.score * c.credits for c in scored)
        total_credits = sum(c.credits for c in scored)
        return round((total_points / total_credits) / 10, 2)

    def get_age(self):
        """Calculate age from date of birth"""
        today = date.today()
        return today.year - self.dob.year - (
            (today.month, today.day) < (self.dob.month, self.dob.day)
        )

    def print_report_card(self):
        """Print formatted academic report"""
        print("\n" + "═"*65)
        print(f"  📋 ACADEMIC REPORT CARD")
        print(f"  {Student._institution_name}")
        print("═"*65)
        print(f"  Name         : {self.name}")
        print(f"  Roll Number  : {self.roll_number}")
        print(f"  Branch       : {self.branch} (Year {self.year})")
        print(f"  Age          : {self.get_age()} years")
        if self.address:
            print(f"  Address      : {self.address}")
        print("─"*65)
        print(f"  {'COURSE':>4}  {'NAME':<25}  {'CREDITS':>7}  {'SCORE':>5}  {'GRADE':>5}")
        print("─"*65)
        for c in self.courses:
            print(f"  {c}")
        print("─"*65)
        print(f"  CGPA: {self.calculate_cgpa():.2f} / 10.00")
        print("═"*65)

    # ── Special Methods (Dunder Methods) ─────────────────────
    def __str__(self):
        return f"Student({self.roll_number}, {self.name}, {self.branch} Y{self.year})"

    def __repr__(self):
        return f"Student(name={self.name!r}, roll={self.roll_number!r})"

    def __eq__(self, other):
        return isinstance(other, Student) and self.roll_number == other.roll_number

    def __lt__(self, other):
        return self.calculate_cgpa() < other.calculate_cgpa()

    def __hash__(self):
        return hash(self.roll_number)

    # ── Class Methods ────────────────────────────────────────
    @classmethod
    def get_total_students(cls):
        """Class method — access class state"""
        return cls._total_students

    @classmethod
    def get_institution(cls):
        return cls._institution_name

    # ── Static Methods ───────────────────────────────────────
    @staticmethod
    def validate_roll_number(roll):
        """Static utility — no access to class/instance"""
        return len(roll) >= 4 and roll.isalnum()

    @staticmethod
    def cgpa_to_percentage(cgpa):
        """Convert CGPA to percentage (approximate)"""
        return round(cgpa * 9.5, 2)


class StudentRegistry:
    """Manages a collection of students — demonstrates object composition"""

    def __init__(self, batch_year):
        self.batch_year = batch_year
        self._students  = {}   # roll_number → Student

    def add_student(self, student):
        if student.roll_number in self._students:
            raise ValueError(f"Roll {student.roll_number} already exists")
        self._students[student.roll_number] = student
        print(f"  ✅ Registered: {student}")

    def get_student(self, roll):
        if roll not in self._students:
            raise KeyError(f"Student {roll} not found")
        return self._students[roll]

    def get_all_sorted_by_cgpa(self):
        """Return students sorted by CGPA descending"""
        return sorted(self._students.values(), reverse=True)

    def get_branch_students(self, branch):
        return [s for s in self._students.values() if s.branch == branch]

    def print_topper_list(self, top_n=5):
        print(f"\n  🏆 TOP {top_n} STUDENTS — BATCH {self.batch_year}")
        print("  " + "─"*55)
        for rank, s in enumerate(self.get_all_sorted_by_cgpa()[:top_n], 1):
            pct = Student.cgpa_to_percentage(s.calculate_cgpa())
            print(f"  #{rank}  {s.name:<20}  {s.roll_number:<10}  CGPA: {s.calculate_cgpa():.2f}  ({pct}%)")
        print()

    def __len__(self):
        return len(self._students)

    def __iter__(self):
        return iter(self._students.values())


if __name__ == "__main__":
    print("═"*65)
    print("  OOP Class & Object Lab — Project Lab India")
    print("  Student Record Management System")
    print("═"*65)

    # Create students
    s1 = Student("Kushagra Bansal", "PLI2024001", "IT", 2, date(2005, 3, 15))
    s2 = Student("Priya Sharma",    "PLI2024002", "CS", 2, date(2005, 7, 22))
    s3 = Student("Rahul Verma",     "PLI2024003", "IT", 2, date(2004, 11, 8))

    # Set addresses
    s1.set_address(Address("12 Tech Park", "Jaipur", "Rajasthan", "302001"))
    s2.set_address(Address("45 MG Road",   "Jaipur", "Rajasthan", "302002"))

    # Create courses
    dsa    = Course("CS301", "Data Structures & Algorithms", 4)
    oops   = Course("CS302", "Object Oriented Programming",  3)
    dbms   = Course("CS303", "Database Management System",   4)
    iot    = Course("IT401", "Internet of Things",           3)
    ml     = Course("CS401", "Machine Learning",             4)

    # Enroll students in courses
    for c in [dsa, oops, dbms, iot]:
        s1.enroll_course(c)
    for c in [Course("CS301","Data Structures & Algorithms",4),
              Course("CS302","Object Oriented Programming",3),
              Course("CS303","Database Management System",4)]:
        s2.enroll_course(c)
    for c in [Course("CS301","Data Structures & Algorithms",4),
              Course("IT401","Internet of Things",3)]:
        s3.enroll_course(c)

    # Assign scores
    s1.courses[0].set_score(92); s1.courses[1].set_score(88)
    s1.courses[2].set_score(85); s1.courses[3].set_score(95)
    s2.courses[0].set_score(78); s2.courses[1].set_score(82); s2.courses[2].set_score(76)
    s3.courses[0].set_score(65); s3.courses[1].set_score(72)

    # Registry operations
    registry = StudentRegistry(2024)
    registry.add_student(s1)
    registry.add_student(s2)
    registry.add_student(s3)

    # Print report cards
    s1.print_report_card()
    s2.print_report_card()

    # Print topper list
    registry.print_topper_list()

    print(f"  Total students enrolled: {Student.get_total_students()}")
    print(f"  Institution: {Student.get_institution()}")
    print(f"  Valid roll 'PLI2024001': {Student.validate_roll_number('PLI2024001')}")
