import sys, pytest
sys.path.insert(0, '..')
from datetime import date
from main import Student, Course, Address, StudentRegistry

def make_student(roll="S001", name="Test User"):
    return Student(name, roll, "CS", 1, date(2003, 1, 1))

def test_student_creation():
    s = make_student()
    assert s.name == "Test User"
    assert s.roll_number == "S001"
    assert s.calculate_cgpa() == 0.0

def test_course_grade():
    c = Course("CS101","Test",3); c.set_score(92)
    assert c.get_grade() == "A+"
    c.set_score(55); assert c.get_grade() == "C"
    c.set_score(35); assert c.get_grade() == "F"

def test_cgpa_calculation():
    s = make_student()
    c1 = Course("C1","Subject1",4); c1.set_score(80)
    c2 = Course("C2","Subject2",4); c2.set_score(90)
    s.enroll_course(c1); s.enroll_course(c2)
    assert s.calculate_cgpa() == round((80*4+90*4)/(8*10), 2)

def test_duplicate_enrollment():
    s = make_student()
    c = Course("C1","Sub",3)
    s.enroll_course(c)
    with pytest.raises(ValueError): s.enroll_course(c)

def test_invalid_score():
    c = Course("C1","Sub",3)
    with pytest.raises(ValueError): c.set_score(110)
    with pytest.raises(ValueError): c.set_score(-5)

def test_class_variables():
    before = Student.get_total_students()
    s = make_student("S999")
    assert Student.get_total_students() == before + 1

def test_equality():
    s1 = make_student("R001","Alice")
    s2 = make_student("R001","Bob")
    assert s1 == s2  # Same roll number

def test_registry():
    reg = StudentRegistry(2024)
    s = make_student("RR001")
    reg.add_student(s)
    assert reg.get_student("RR001") == s
    assert len(reg) == 1
