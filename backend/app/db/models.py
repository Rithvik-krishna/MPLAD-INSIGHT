from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from app.db.database import Base

class Work(Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True, index=True)
    work_id = Column(String, index=True)
    work_category = Column(String)
    state = Column(String, index=True)
    ida = Column(String)
    mp_name = Column(String, index=True)
    constituency = Column(String)
    sanction_amount = Column(Float)
    gap_days = Column(Float)

    flag_delay = Column(Boolean, default=False)
    flag_amount = Column(Boolean, default=False)
    flag_mp_drift = Column(Boolean, default=False)
    n_flags = Column(Integer, default=0)
    is_high_severity = Column(Boolean, default=False)

    amount_deviation_pct = Column(Float, nullable=True)
    mp_drift_zscore = Column(Float, nullable=True)

    explanation = Column(Text, nullable=True)
    flag_isolation_forest = Column(Boolean, default=False)