from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    description: str
    year: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        # orm_mode = True  # pydantic version < 2.x
        from_attributes = True  # pydantic version > 2.x






class EmployeeBase(BaseModel):
    Employee_name: str
    Employee_phone: str
    Employee_address: str
    Employee_age: int

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True






class StudentBase(BaseModel):
    student_name: str
    student_age: str
    student_address: str
    student_phone: int

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True






class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
