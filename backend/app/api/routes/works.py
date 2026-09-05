from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.db.models import Work
from app.models.schemas import WorkOut

router = APIRouter()

@router.get("/", response_model=list[WorkOut])
def list_works(
    q: Optional[str] = None,
    sector: Optional[str] = None,
    state: Optional[str] = None,
    mp_name: Optional[str] = None,
    flagged_only: bool = False,
    limit: int = Query(50, le=1000),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    query = db.query(Work)
    if q:
        search_pattern = f"%{q.strip()}%"
        query = query.filter(
            (Work.work_id.ilike(search_pattern)) |
            (Work.title.ilike(search_pattern)) |
            (Work.work_category.ilike(search_pattern)) |
            (Work.constituency.ilike(search_pattern)) |
            (Work.mp_name.ilike(search_pattern)) |
            (Work.state.ilike(search_pattern)) |
            (Work.ida.ilike(search_pattern))
        )
    if sector and sector != "all":
        query = query.filter(
            (Work.sector == sector) | (Work.work_category == sector)
        )
    if state and state != "all":
        query = query.filter(Work.state.ilike(f"%{state}%"))
    if mp_name and mp_name != "all":
        query = query.filter(Work.mp_name.ilike(f"%{mp_name}%"))
    if flagged_only:
        query = query.filter(Work.n_flags > 0)
    return query.offset(offset).limit(limit).all()

@router.get("/{work_id}", response_model=WorkOut)
def get_work(work_id: str, db: Session = Depends(get_db)):
    record = db.query(Work).filter(Work.work_id == work_id).first()
    if record:
        return record
    record = db.query(Work).filter(Work.work_id.ilike(f"%{work_id.strip()}%")).first()
    if record:
        return record
    raise HTTPException(status_code=404, detail="Work record not found")