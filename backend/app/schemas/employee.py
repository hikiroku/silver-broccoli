from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

from app.schemas.base import TimestampMixin

class EmployeeBase(BaseModel):
    employee_code: str
    name: str
    email: EmailStr

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class Employee(EmployeeBase, TimestampMixin):
    id: int

    class Config:
        from_attributes = True

class EmployeeWithHistory(Employee):
    assignments: List['AssignmentWithDepartment'] = []

    class Config:
        from_attributes = True

# 循環参照を避けるため、AssignmentWithDepartmentは後で定義
from app.schemas.department import Department

class AssignmentBase(BaseModel):
    employee_id: int
    department_id: int
    is_main: bool
    valid_from: datetime
    valid_until: Optional[datetime] = None

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(AssignmentBase):
    pass

class Assignment(AssignmentBase, TimestampMixin):
    id: int

    class Config:
        from_attributes = True

class AssignmentWithDepartment(Assignment):
    department: Department

    class Config:
        from_attributes = True
