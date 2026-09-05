import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB = BASE_DIR / "nidhitrace.db"

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB.as_posix()}")

DELAY_PERCENTILE = 0.95
AMOUNT_DEVIATION_PCT = 100
MP_DRIFT_ZSCORE = 3.0