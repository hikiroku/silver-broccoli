from fastapi import APIRouter

from app.api.v1.endpoints import departments, employees, assignments

api_router = APIRouter()

api_router.include_router(departments.router, prefix="/departments", tags=["departments"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(assignments.router, prefix="/assignments", tags=["assignments"])
