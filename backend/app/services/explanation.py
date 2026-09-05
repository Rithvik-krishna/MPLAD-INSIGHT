def generate_explanation(row) -> str:
    reasons = []
    if row.get("flag_delay"):
        reasons.append(f"work has been delayed {int(row['gap_days'])} days beyond the normal recommend-to-sanction window")
    if row.get("flag_amount"):
        reasons.append(f"sanctioned amount deviates {row['amount_deviation_pct']:.0f}% from the category norm")
    if row.get("flag_mp_drift"):
        z = row.get("mp_drift_zscore")
        reasons.append(f"amount is {abs(z):.1f} standard deviations from this MP's own historical norm for this category" if z is not None else "flagged for MP baseline drift")

    if not reasons:
        return "No anomaly flags triggered."
    prefix = "High severity — multiple factors: " if row.get("is_high_severity") else "Flagged: "
    return prefix + "; ".join(reasons) + "."