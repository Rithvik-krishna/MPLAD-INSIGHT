from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.db.models import Work
from app.models.schemas import WorkOut

router = APIRouter()

@router.get("/", response_model=list[WorkOut])
def list_works(
    state: Optional[str] = None,
    mp_name: Optional[str] = None,
    flagged_only: bool = False,
    limit: int = Query(50, le=500),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    q = db.query(Work)
    if state:
        q = q.filter(Work.state == state)
    if mp_name:
        q = q.filter(Work.mp_name == mp_name)
    if flagged_only:
        q = q.filter(Work.n_flags > 0)
    return q.offset(offset).limit(limit).all()

@router.get("/{work_id}", response_model=WorkOut)
def get_work(work_id: str, db: Session = Depends(get_db)):
    return db.query(Work).filter(Work.work_id == work_id).first()