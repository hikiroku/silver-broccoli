from typing import List, Optional, Dict, Union
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.crud.base import CRUDBase
from app.models.models import MainAssignment, ConcurrentAssignment
from app.schemas.employee import AssignmentCreate

class CRUDMainAssignment(CRUDBase[MainAssignment, AssignmentCreate, AssignmentCreate]):
    def get_current(
        self, db: Session, *, employee_id: int, target_date: date = None
    ) -> Optional[MainAssignment]:
        """
        指定日時点の主務所属を取得
        """
        if target_date is None:
            target_date = date.today()

        return (
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

    def get_history(
        self, db: Session, *, employee_id: int
    ) -> List[MainAssignment]:
        """
        主務所属の履歴を取得
        """
        return (
            db.query(MainAssignment)
            .filter(MainAssignment.employee_id == employee_id)
            .order_by(MainAssignment.valid_from.desc())
            .all()
        )

class CRUDConcurrentAssignment(CRUDBase[ConcurrentAssignment, AssignmentCreate, AssignmentCreate]):
    def get_current(
        self, db: Session, *, employee_id: int, target_date: date = None
    ) -> List[ConcurrentAssignment]:
        """
        指定日時点の兼務所属を取得
        """
        if target_date is None:
            target_date = date.today()

        return (
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

    def get_history(
        self, db: Session, *, employee_id: int
    ) -> List[ConcurrentAssignment]:
        """
        兼務所属の履歴を取得
        """
        return (
            db.query(ConcurrentAssignment)
            .filter(ConcurrentAssignment.employee_id == employee_id)
            .order_by(ConcurrentAssignment.valid_from.desc())
            .all()
        )

main_assignment = CRUDMainAssignment(MainAssignment)
concurrent_assignment = CRUDConcurrentAssignment(ConcurrentAssignment)
