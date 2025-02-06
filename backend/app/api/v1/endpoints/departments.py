from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.models import Assignment, Employee
from app.schemas.department import Department, DepartmentCreate, DepartmentUpdate, DepartmentTreeNode, DepartmentWithMembers

router = APIRouter()

@router.get("/", response_model=List[Department])
def get_departments(
    db: Session = Depends(deps.get_db),
    target_date: Optional[datetime] = None,
):
    """
    組織一覧を取得
    """
    return crud.department.get_all(db=db, target_date=target_date)

@router.get("/tree", response_model=List[DepartmentWithMembers])
def get_organization_tree(
    db: Session = Depends(deps.get_db),
    target_date: Optional[datetime] = None,
):
    """
    組織構造をツリー形式で取得
    """
    if target_date is None:
        target_date = datetime.now()

    departments = crud.department.get_all(db=db, target_date=target_date)
    result = []
    
    for dept in departments:
        # 所属情報を取得
        assignments = db.query(Assignment).filter(
            Assignment.department_id == dept.id,
            Assignment.valid_from <= target_date,
            (Assignment.valid_until.is_(None) | 
             (Assignment.valid_until >= target_date))
        ).all()

        # 主務メンバーと兼務メンバーを分類
        main_members = []
        concurrent_members = []
        
        for assignment in assignments:
            employee = db.query(Employee).filter(
                Employee.id == assignment.employee_id
            ).first()
            
            if employee:
                if assignment.is_main:
                    main_members.append({
                        "id": employee.id,
                        "employee_code": employee.employee_code,
                        "name": employee.name,
                        "email": employee.email,
                        "created_at": employee.created_at,
                        "updated_at": employee.updated_at,
                    })
                else:
                    concurrent_members.append({
                        "id": employee.id,
                        "employee_code": employee.employee_code,
                        "name": employee.name,
                        "email": employee.email,
                        "created_at": employee.created_at,
                        "updated_at": employee.updated_at,
                    })

        result.append({
            "id": dept.id,
            "department_code": dept.department_code,
            "name": dept.name,
            "parent_id": dept.parent_id,
            "valid_from": dept.valid_from,
            "valid_until": dept.valid_until,
            "created_at": dept.created_at,
            "updated_at": dept.updated_at,
            "main_members": main_members,
            "concurrent_members": concurrent_members,
        })

    return result

@router.post("/", response_model=Department)
def create_department(
    *,
    db: Session = Depends(deps.get_db),
    department_in: DepartmentCreate,
):
    """
    組織を作成
    """
    return crud.department.create(db=db, obj_in=department_in)

@router.put("/{department_id}", response_model=Department)
def update_department(
    *,
    db: Session = Depends(deps.get_db),
    department_id: int,
    department_in: DepartmentUpdate,
):
    """
    組織を更新
    """
    department = crud.department.get(db=db, id=department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return crud.department.update(db=db, db_obj=department, obj_in=department_in)
