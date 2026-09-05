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
    title: Optional[str] = None
    sector: Optional[str] = None
    location: Optional[str] = None
    mp: Optional[str] = None
    sanctioned: Optional[str] = None
    expended: Optional[str] = None
    agency: Optional[str] = None
    progress: Optional[str] = None
    score: Optional[int] = None
    severity: Optional[str] = None
    anomaly: Optional[str] = None
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
    total_registered: Optional[int] = 198116
    ai_scanned: Optional[int] = 171890
    coverage_pct: Optional[float] = 86.8
    critical_count: Optional[int] = 1137
    high_count: Optional[int] = 5507
    med_count: Optional[int] = 17761
    low_count: Optional[int] = 146407
    scrutiny_exposure_cr: Optional[float] = 2001.2
    isolation_forest_flagged: Optional[int] = 8563
    benford_flagged: Optional[int] = 1522