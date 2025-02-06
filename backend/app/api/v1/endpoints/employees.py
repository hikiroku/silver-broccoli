from typing import Any, List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.employee import (
    Employee,
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeInfo,
)

router = APIRouter()

@router.get("/", response_model=List[Employee])
async def list_employees(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    社員一覧を取得
    """
    return crud.employee.get_multi(db, skip=skip, limit=limit)

@router.get("/{employee_id}", response_model=EmployeeInfo)
async def get_employee(
    *,
    db: Session = Depends(deps.get_db),
    employee_id: int,
    target_date: Optional[date] = None,
) -> Any:
    """
    社員情報を取得(所属情報を含む)
    """
    employee = crud.employee.get_with_assignments(
        db, employee_id=employee_id, target_date=target_date
    )
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )
    return employee

@router.get("/{employee_id}/history", response_model=List[dict])
async def get_employee_history(
    *,
    db: Session = Depends(deps.get_db),
    employee_id: int,
) -> Any:
    """
    社員の異動履歴を取得
    """
    employee = crud.employee.get(db, id=employee_id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )
    return crud.employee.get_assignment_history(db, employee_id=employee_id)

@router.post("/", response_model=Employee)
async def create_employee(
    *,
    db: Session = Depends(deps.get_db),
    employee_in: EmployeeCreate,
) -> Any:
    """
    社員を新規作成
    """
    # 社員番号の重複チェック
    if crud.employee.get_by_code(db, employee_code=employee_in.employee_code):
        raise HTTPException(
            status_code=400,
            detail="Employee code already registered",
        )
    return crud.employee.create(db, obj_in=employee_in)

@router.put("/{employee_id}", response_model=Employee)
async def update_employee(
    *,
    db: Session = Depends(deps.get_db),
    employee_id: int,
    employee_in: EmployeeUpdate,
) -> Any:
    """
    社員情報を更新
    """
    employee = crud.employee.get(db, id=employee_id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )
    return crud.employee.update(db, db_obj=employee, obj_in=employee_in)

@router.delete("/{employee_id}", response_model=Employee)
async def delete_employee(
    *,
    db: Session = Depends(deps.get_db),
    employee_id: int,
) -> Any:
    """
    社員を削除
    """
    employee = crud.employee.get(db, id=employee_id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )
    return crud.employee.remove(db, id=employee_id)
