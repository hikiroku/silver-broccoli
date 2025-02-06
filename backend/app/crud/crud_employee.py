from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.crud.base import CRUDBase
from app.models.models import Employee, MainAssignment, ConcurrentAssignment
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

class CRUDEmployee(CRUDBase[Employee, EmployeeCreate, EmployeeUpdate]):
    def get_by_code(self, db: Session, *, employee_code: str) -> Optional[Employee]:
        """
        社員番号による取得
        """
        return db.query(Employee).filter(Employee.employee_code == employee_code).first()

    def get_with_assignments(
        self, db: Session, *, employee_id: int, target_date: date = None
    ) -> Optional[Employee]:
        """
        所属情報を含む社員情報の取得
        """
        if target_date is None:
            target_date = date.today()

        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if employee:
            # 主務所属を取得
            main_assignment = (
                db.query(MainAssignment)
                .filter(
                    MainAssignment.employee_id == employee_id,
                    MainAssignment.valid_from <= target_date,
                    or_(
                        MainAssignment.valid_until.is_(None),
                        MainAssignment.valid_until >= target_date
                    )
                )
                .first()
            )

            # 兼務所属を取得
            concurrent_assignments = (
                db.query(ConcurrentAssignment)
                .filter(
                    ConcurrentAssignment.employee_id == employee_id,
                    ConcurrentAssignment.valid_from <= target_date,
                    or_(
                        ConcurrentAssignment.valid_until.is_(None),
                        ConcurrentAssignment.valid_until >= target_date
                    )
                )
                .all()
            )

            return {
                **employee.__dict__,
                "main_assignment": main_assignment,
                "concurrent_assignments": concurrent_assignments
            }
        return None

    def get_assignment_history(
        self, db: Session, *, employee_id: int
    ) -> List[dict]:
        """
        異動履歴の取得
        """
        # 主務所属の履歴
        main_assignments = (
            db.query(MainAssignment)
            .filter(MainAssignment.employee_id == employee_id)
            .order_by(MainAssignment.valid_from.desc())
            .all()
        )

        # 兼務所属の履歴
        concurrent_assignments = (
            db.query(ConcurrentAssignment)
            .filter(ConcurrentAssignment.employee_id == employee_id)
            .order_by(ConcurrentAssignment.valid_from.desc())
            .all()
        )

        # 履歴を統合してソート
        history = []
        for assignment in main_assignments:
            history.append({
                "type": "main",
                "department": assignment.department,
                "valid_from": assignment.valid_from,
                "valid_until": assignment.valid_until
            })
        
        for assignment in concurrent_assignments:
            history.append({
                "type": "concurrent",
                "department": assignment.department,
                "valid_from": assignment.valid_from,
                "valid_until": assignment.valid_until
            })

        return sorted(history, key=lambda x: x["valid_from"], reverse=True)

employee = CRUDEmployee(Employee)
