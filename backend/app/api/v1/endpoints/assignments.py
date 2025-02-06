from typing import Any, List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.employee import AssignmentCreate, Assignment

router = APIRouter()

@router.post("/main", response_model=Assignment)
async def create_main_assignment(
    *,
    db: Session = Depends(deps.get_db),
    assignment_in: AssignmentCreate,
) -> Any:
    """
    主務所属を作成
    """
    # 社員の存在チェック
    employee = crud.employee.get(db, id=assignment_in.employee_id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )
    
    # 組織の存在チェック
    department = crud.department.get(db, id=assignment_in.department_id)
    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found",
        )
    
    # 同一期間の主務所属が既に存在するかチェック
    current = crud.main_assignment.get_current(
        db, employee_id=assignment_in.employee_id, target_date=assignment_in.valid_from
    )
    if current:
        raise HTTPException(
            status_code=400,
            detail="Main assignment already exists for this period",
        )
    
    return crud.main_assignment.create(db, obj_in=assignment_in)

@router.post("/concurrent", response_model=Assignment)
async def create_concurrent_assignment(
    *,
    db: Session = Depends(deps.get_db),
    assignment_in: AssignmentCreate,
) -> Any:
    """
    兼務所属を作成
    """
    # 社員の存在チェック
    employee = crud.employee.get(db, id=assignment_in.employee_id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )
    
    # 組織の存在チェック
    department = crud.department.get(db, id=assignment_in.department_id)
    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found",
        )
    
    # 同一組織への兼務所属が既に存在するかチェック
    current = crud.concurrent_assignment.get_current(
        db, employee_id=assignment_in.employee_id, target_date=assignment_in.valid_from
    )
    for assignment in current:
        if assignment.department_id == assignment_in.department_id:
            raise HTTPException(
                status_code=400,
                detail="Concurrent assignment to this department already exists",
            )
    
    return crud.concurrent_assignment.create(db, obj_in=assignment_in)

@router.put("/main/{assignment_id}/end", response_model=Assignment)
async def end_main_assignment(
    *,
    db: Session = Depends(deps.get_db),
    assignment_id: int,
    end_date: date,
) -> Any:
    """
    主務所属を終了
    """
    assignment = crud.main_assignment.get(db, id=assignment_id)
    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found",
        )
    
    if assignment.valid_until and assignment.valid_until < end_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be before current end date",
        )
    
    return crud.main_assignment.update(
        db,
        db_obj=assignment,
        obj_in={"valid_until": end_date},
    )

@router.put("/concurrent/{assignment_id}/end", response_model=Assignment)
async def end_concurrent_assignment(
    *,
    db: Session = Depends(deps.get_db),
    assignment_id: int,
    end_date: date,
) -> Any:
    """
    兼務所属を終了
    """
    assignment = crud.concurrent_assignment.get(db, id=assignment_id)
    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found",
        )
    
    if assignment.valid_until and assignment.valid_until < end_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be before current end date",
        )
    
    return crud.concurrent_assignment.update(
        db,
        db_obj=assignment,
        obj_in={"valid_until": end_date},
    )
