"""
Statistical outlier layer using scikit-learn's IsolationForest.
Runs alongside the 3 rule-based signals as a 4th, independent check —
catches multivariate outliers the single-variable rules might miss
(e.g. a combination of moderate delay + moderate amount deviation
that's individually unremarkable but jointly unusual).
"""
import pandas as pd
from sklearn.ensemble import IsolationForest

CONTAMINATION = 0.05  # matches the 5% percentile used by the other signals


def flag_isolation_forest(df: pd.DataFrame) -> pd.Series:
    features = df[["gap_days", "sanction_amount", "amount_deviation_pct"]].fillna(0)
    model = IsolationForest(contamination=CONTAMINATION, random_state=42)
    predictions = model.fit_predict(features)
    return predictions == -1  # -1 means outlier