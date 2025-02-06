from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.schemas.base import TimestampMixin, ValidityMixin
from app.schemas.employee import Employee

class DepartmentBase(BaseModel):
    department_code: str
    name: str
    parent_id: Optional[int] = None

class DepartmentCreate(DepartmentBase, ValidityMixin):
    pass

class DepartmentUpdate(DepartmentBase, ValidityMixin):
    pass

class Department(DepartmentBase, ValidityMixin, TimestampMixin):
    id: int

    class Config:
        from_attributes = True

class DepartmentTreeNode(Department):
    children: List['DepartmentTreeNode'] = []

    class Config:
        from_attributes = True

class DepartmentWithMembers(Department):
    main_members: List[Employee] = []
    concurrent_members: List[Employee] = []

    class Config:
        from_attributes = True
