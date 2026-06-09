# OOP Fundamentals — Learning Notes
# By Kushagra Bansal | Project Lab India

## Core Concepts Demonstrated

### 1. Classes and Objects
class Student:              # Blueprint (class)
    def __init__(self):     # Constructor
        self.name = ""      # Instance attribute

s = Student()               # Object (instance)

### 2. Instance vs Class vs Static Methods
| Method | Decorator | First Param | Access |
|--------|-----------|-------------|--------|
| Instance | none | self | instance + class state |
| Class | @classmethod | cls | class state only |
| Static | @staticmethod | none | no state access |

### 3. Dunder Methods (Magic Methods)
__init__  → Constructor
__str__   → str(obj) — human readable
__repr__  → repr(obj) — developer representation
__eq__    → == operator
__lt__    → < operator (enables sorting)
__len__   → len(obj)
__iter__  → for item in obj

### 4. Object Composition
"Has-a" relationship:
StudentRegistry has Students (composition)
Student has Address, Courses (aggregation)

### Interview Questions
1. Difference between class and instance variables?
2. When to use @classmethod vs @staticmethod?
3. What are dunder methods? Name 5 important ones.
4. Difference between __str__ and __repr__?
5. What is object composition vs inheritance?
