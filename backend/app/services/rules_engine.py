"""
Real anomaly detection on the full merged dataset — no injection, no
synthetic data. All 3 rule-based signals use a consistent percentile-based
cutoff (matching delay's original design) rather than fixed thresholds,
which were over-flagging on real data variance. A 4th, independent
IsolationForest signal is layered on top to catch multivariate outliers.
Agency concentration intentionally excluded — see docs/architecture.md.
"""
import numpy as np
import pandas as pd
from app.core.config import DELAY_PERCENTILE
from app.services.isolation_forest import flag_isolation_forest

FLAG_PERCENTILE = 0.95  # top 5% by each signal's own score


def flag_delay(df: pd.DataFrame) -> pd.Series:
    thresh = df["gap_days"].quantile(DELAY_PERCENTILE)
    return df["gap_days"] > thresh


def flag_amount(df: pd.DataFrame) -> pd.DataFrame:
    cat_stats = df.groupby("work_category")["sanction_amount"].agg(["mean", "std"])
    df = df.merge(cat_stats, left_on="work_category", right_index=True, how="left")
    df["amount_deviation_pct"] = ((df["sanction_amount"] - df["mean"]) / df["mean"]).abs() * 100
    thresh = df["amount_deviation_pct"].quantile(FLAG_PERCENTILE)
    df["flag_amount"] = df["amount_deviation_pct"] > thresh
    return df.drop(columns=["mean", "std"])


def flag_mp_drift(df: pd.DataFrame) -> pd.DataFrame:
    def robust_center_scale(x):
        med = x.median()
        mad = (x - med).abs().median() * 1.4826
        floor = max(mad, abs(med) * 0.02)
        return med, floor if floor > 0 else np.nan

    stats = df.groupby(["mp_name", "work_category"])["sanction_amount"].apply(
        lambda x: pd.Series(robust_center_scale(x), index=["med", "scale"])
    ).unstack()
    df = df.merge(stats, left_on=["mp_name", "work_category"], right_index=True, how="left")
    df["mp_drift_zscore"] = (df["sanction_amount"] - df["med"]) / df["scale"]

    abs_z = df["mp_drift_zscore"].abs()
    thresh = abs_z.quantile(FLAG_PERCENTILE)
    df["flag_mp_drift"] = (abs_z > thresh).fillna(False)
    return df.drop(columns=["med", "scale"])


def run_all_flags(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["flag_delay"] = flag_delay(df)
    df = flag_amount(df)
    df = flag_mp_drift(df)
    df["flag_isolation_forest"] = flag_isolation_forest(df)
    df["n_flags"] = df[["flag_delay", "flag_amount", "flag_mp_drift", "flag_isolation_forest"]].sum(axis=1)
    df["is_high_severity"] = df["n_flags"] >= 2
    return df
