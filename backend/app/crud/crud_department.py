from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.models import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate

class CRUDDepartment(CRUDBase[Department, DepartmentCreate, DepartmentUpdate]):
    def get_by_code(self, db: Session, *, code: str, target_date: datetime = None) -> Optional[Department]:
        if target_date is None:
            target_date = datetime.now()
        
        return db.query(self.model).filter(
            and_(
                self.model.department_code == code,
                self.model.valid_from <= target_date,
                (self.model.valid_until.is_(None) | (self.model.valid_until >= target_date))
            )
        ).first()

    def get_all(self, db: Session, *, target_date: datetime = None) -> List[Department]:
        if target_date is None:
            target_date = datetime.now()
        
        return db.query(self.model).filter(
            and_(
                self.model.valid_from <= target_date,
                (self.model.valid_until.is_(None) | (self.model.valid_until >= target_date))
            )
        ).all()

    def get_tree(self, db: Session, *, target_date: datetime = None) -> List[Department]:
        if target_date is None:
            target_date = datetime.now()
        
        # ルート組織(parent_idがNullの組織)を取得
        roots = db.query(self.model).filter(
            and_(
                self.model.parent_id.is_(None),
                self.model.valid_from <= target_date,
                (self.model.valid_until.is_(None) | (self.model.valid_until >= target_date))
            )
        ).all()

        return roots

department = CRUDDepartment(Department)
