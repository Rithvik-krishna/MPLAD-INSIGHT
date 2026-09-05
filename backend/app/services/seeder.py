"""
NidhiTrace Database Seeder
Auto-populates the SQLite database with authentic works and anomaly flags
from the verified NIDHI TRACE datasets if the database table is empty.
"""

import os
import json
from pathlib import Path
from sqlalchemy.orm import Session
from app.db.models import Work
from app.services.explanation import generate_explanation

def seed_database_if_empty(db: Session):
    try:
        existing_count = db.query(Work).count()
        if existing_count > 0:
            return existing_count

        project_root = Path(__file__).resolve().parent.parent.parent.parent
        cases_path = project_root / "assets" / "data" / "cases_index.json"
        ledger_path = project_root / "assets" / "data" / "ledger_works.json"

        works_to_insert = []
        seen_work_ids = set()

        if cases_path.exists():
            with open(cases_path, "r", encoding="utf-8") as f:
                cases_data = json.load(f)

            for cid, c in cases_data.items():
                if cid in seen_work_ids:
                    continue
                seen_work_ids.add(cid)

                flags = c.get("flags") or {}
                flag_delay = bool(flags.get("flag_delay", False))
                flag_amount = bool(flags.get("flag_amount", False))
                flag_mp_drift = bool(flags.get("flag_mp_drift", False))
                flag_iso = bool(flags.get("iso_flag", False))
                is_high_sev = bool(flags.get("rule_high_severity", c.get("severity") in ("critical", "high")))
                n_flags = sum([flag_delay, flag_amount, flag_mp_drift, flag_iso])

                sanc_val = c.get("sanctioned_raw")
                if sanc_val is None:
                    raw_str = str(c.get("sanctioned", "0")).replace("₹", "").replace(",", "").strip()
                    if "Cr" in raw_str:
                        sanc_val = float(raw_str.replace("Cr", "").strip()) * 1e7
                    elif "L" in raw_str:
                        sanc_val = float(raw_str.replace("L", "").strip()) * 1e5
                    else:
                        try:
                            sanc_val = float(raw_str)
                        except ValueError:
                            sanc_val = 0.0

                work_row = {
                    "work_id": cid,
                    "work_category": c.get("sector") or "Public Infrastructure",
                    "state": c.get("state") or "India",
                    "ida": c.get("agency") or "District Authority",
                    "mp_name": c.get("mp") or "Member of Parliament",
                    "constituency": c.get("constituency") or c.get("location") or "District",
                    "sanction_amount": float(sanc_val),
                    "gap_days": float(c.get("gapDays") or 0.0),
                    "flag_delay": flag_delay,
                    "flag_amount": flag_amount,
                    "flag_mp_drift": flag_mp_drift,
                    "n_flags": n_flags,
                    "is_high_severity": is_high_sev,
                    "amount_deviation_pct": float(flags.get("amount_zscore", 0.0) or 0.0) * 25.0,
                    "mp_drift_zscore": float(flags.get("mp_drift_zscore", 0.0) or 0.0),
                    "flag_isolation_forest": flag_iso,
                }
                expl = c.get("anomaly") or generate_explanation(work_row)
                work_row["explanation"] = expl
                works_to_insert.append(Work(**work_row))

        if ledger_path.exists() and len(works_to_insert) < 2000:
            with open(ledger_path, "r", encoding="utf-8") as f:
                ledger_data = json.load(f)

            for item in ledger_data:
                wid = item.get("id")
                if not wid or wid in seen_work_ids:
                    continue
                seen_work_ids.add(wid)

                raw_sanc = str(item.get("sanctioned", "0")).replace("₹", "").replace(",", "").strip()
                if "Cr" in raw_sanc:
                    sval = float(raw_sanc.replace("Cr", "").strip()) * 1e7
                elif "L" in raw_sanc:
                    sval = float(raw_sanc.replace("L", "").strip()) * 1e5
                else:
                    try:
                        sval = float(raw_sanc)
                    except ValueError:
                        sval = 0.0

                loc = item.get("location", "")
                parts = loc.split(",") if "," in loc else [loc, loc]
                dist = parts[0].strip()
                st = parts[-1].strip() if len(parts) > 1 else dist

                is_flagged = bool(item.get("isFlagged", False))
                w_row = {
                    "work_id": wid,
                    "work_category": item.get("sector") or "General Infrastructure",
                    "state": st or "India",
                    "ida": item.get("agency") or "District Implementing Agency",
                    "mp_name": item.get("mp") or "District MP",
                    "constituency": dist or "Constituency",
                    "sanction_amount": float(sval),
                    "gap_days": 180.0 if is_flagged else 45.0,
                    "flag_delay": is_flagged,
                    "flag_amount": False,
                    "flag_mp_drift": False,
                    "n_flags": 1 if is_flagged else 0,
                    "is_high_severity": False,
                    "amount_deviation_pct": 12.0 if is_flagged else 0.0,
                    "mp_drift_zscore": 1.2 if is_flagged else 0.0,
                    "flag_isolation_forest": False,
                    "explanation": "Flagged during cross-constituency surveillance." if is_flagged else "Normal expenditure within compliance limits.",
                }
                works_to_insert.append(Work(**w_row))
                if len(works_to_insert) >= 3000:
                    break

        if works_to_insert:
            db.bulk_save_objects(works_to_insert)
            db.commit()
            print(f"[NidhiTrace Seeder] Successfully seeded {len(works_to_insert)} records.")
            return len(works_to_insert)
    except Exception as e:
        db.rollback()
        print(f"[NidhiTrace Seeder] Seeding error: {e}")
        return 0
