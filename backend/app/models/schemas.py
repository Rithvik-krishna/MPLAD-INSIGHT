from pydantic import BaseModel
from typing import Optional

class WorkOut(BaseModel):
    id: int
    work_id: str
    work_category: str
    state: str
    ida: str
    mp_name: str
    constituency: str
    sanction_amount: float
    gap_days: float
    flag_delay: bool
    flag_amount: bool
    flag_mp_drift: bool
    n_flags: int
    is_high_severity: bool
    flag_isolation_forest: bool
    class Config:
        from_attributes = True

class DossierOut(WorkOut):
    amount_deviation_pct: Optional[float] = None
    mp_drift_zscore: Optional[float] = None
    explanation: Optional[str] = None

class SeverityBreakdown(BaseModel):
    total_works: int
    flagged_count: int
    high_severity_count: int
    delay_flagged: int
    amount_flagged: int
    mp_drift_flagged: int