"""
Endpoints for anomaly/flagged-case data.
TODO: GET /anomalies (list flagged works, filter by severity)
TODO: GET /anomalies/{work_id} (dossier: flags + explanation)
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Work
from app.models.schemas import WorkOut, DossierOut, SeverityBreakdown

router = APIRouter()

@router.get("/", response_model=list[WorkOut])
def list_anomalies(
    signal: str = Query("delay", pattern="^(delay|amount|mp_drift|isolation_forest|high_severity)$"),
    limit: int = Query(50, le=500),
    db: Session = Depends(get_db),
):
    q = db.query(Work)
    if signal == "delay":
        q = q.filter(Work.flag_delay == True).order_by(Work.gap_days.desc())
    elif signal == "amount":
        q = q.filter(Work.flag_amount == True).order_by(Work.amount_deviation_pct.desc())
    elif signal == "mp_drift":
        q = q.filter(Work.flag_mp_drift == True).order_by(Work.mp_drift_zscore.desc())
    elif signal == "isolation_forest":
        q = q.filter(Work.flag_isolation_forest == True)
    elif signal == "high_severity":
        q = q.filter(Work.is_high_severity == True)
    return q.limit(limit).all()

@router.get("/{work_id}", response_model=DossierOut)
def get_dossier(work_id: str, db: Session = Depends(get_db)):
    return db.query(Work).filter(Work.work_id == work_id).first()

@router.get("/summary/breakdown", response_model=SeverityBreakdown)
def severity_breakdown(db: Session = Depends(get_db)):
    total = db.query(Work).count()
    return SeverityBreakdown(
        total_works=total,
        flagged_count=db.query(Work).filter(Work.n_flags > 0).count(),
        high_severity_count=db.query(Work).filter(Work.is_high_severity == True).count(),
        delay_flagged=db.query(Work).filter(Work.flag_delay == True).count(),
        amount_flagged=db.query(Work).filter(Work.flag_amount == True).count(),
        mp_drift_flagged=db.query(Work).filter(Work.flag_mp_drift == True).count(),
    )