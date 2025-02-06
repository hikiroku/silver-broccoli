from app.crud.crud_employee import employee
from app.crud.crud_department import department
from app.crud.crud_assignment import assignment
from app.models.models import Employee, Department, Assignment as models

__all__ = ["employee", "department", "assignment", "models"]
