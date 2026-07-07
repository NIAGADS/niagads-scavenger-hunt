import json
from datetime import datetime, timezone

import streamlit as st


LEADERBOARD_HEADERS = [
    "id",
    "submitted_at_utc",
    "updated_at_utc",
    "team_name",
    "email",
    "assigned_gene",
    "score",
    "required_activities_completed",
    "required_activities_total",
    "progress",
    "skills_completed",
    "skills_completed_count",
    "hints_used_count",
]


def get_secret_section(name):
    try:
        return st.secrets.get(name)
    except Exception:
        return None


def leaderboard_configured():
    leaderboard = get_secret_section("leaderboard")
    service_account = get_secret_section("gcp_service_account")
    return bool(
        leaderboard
        and service_account
        and leaderboard.get("spreadsheet_id")
        and leaderboard.get("worksheet_name")
        and service_account.get("client_email")
        and service_account.get("private_key")
    )


def get_worksheet():
    if not leaderboard_configured():
        raise RuntimeError("Google Sheets leaderboard is not configured.")

    import gspread
    from google.oauth2.service_account import Credentials

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    leaderboard = get_secret_section("leaderboard")
    service_account = get_secret_section("gcp_service_account")
    credentials = Credentials.from_service_account_info(dict(service_account), scopes=scopes)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(leaderboard["spreadsheet_id"])
    worksheet_name = leaderboard["worksheet_name"]

    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=100, cols=len(LEADERBOARD_HEADERS))

    ensure_headers(worksheet)
    return worksheet


def ensure_headers(worksheet):
    current_headers = worksheet.row_values(1)
    if current_headers != LEADERBOARD_HEADERS:
        worksheet.update("A1", [LEADERBOARD_HEADERS])


def normalize_entry(row):
    entry = {header: row.get(header, "") for header in LEADERBOARD_HEADERS}
    for key in ["score", "required_activities_completed", "required_activities_total", "skills_completed_count", "hints_used_count"]:
        try:
            entry[key] = int(entry.get(key, 0))
        except (TypeError, ValueError):
            entry[key] = 0
    try:
        entry["skills_completed"] = json.loads(entry.get("skills_completed", "[]") or "[]")
    except json.JSONDecodeError:
        entry["skills_completed"] = []
    return entry


def load_leaderboard():
    worksheet = get_worksheet()
    return [normalize_entry(row) for row in worksheet.get_all_records()]


def entry_to_row(entry):
    return [
        entry.get("id", ""),
        entry.get("submitted_at_utc", ""),
        entry.get("updated_at_utc", ""),
        entry.get("team_name", ""),
        entry.get("email", ""),
        entry.get("assigned_gene", ""),
        entry.get("score", 0),
        entry.get("required_activities_completed", 0),
        entry.get("required_activities_total", 0),
        entry.get("progress", ""),
        json.dumps(entry.get("skills_completed", [])),
        entry.get("skills_completed_count", 0),
        entry.get("hints_used_count", 0),
    ]


def leaderboard_entry(summary, entry_id, existing_entry=None):
    now = datetime.now(timezone.utc).isoformat()
    required_done = summary["required_activities_completed"]
    required_total = summary["required_activities_total"]
    return {
        "id": entry_id,
        "submitted_at_utc": (existing_entry or {}).get("submitted_at_utc", now),
        "updated_at_utc": now,
        "team_name": summary["team_name"],
        "email": summary["email"],
        "assigned_gene": summary["assigned_gene"],
        "score": summary["score"],
        "required_activities_completed": required_done,
        "required_activities_total": required_total,
        "progress": f"{required_done}/{required_total}",
        "skills_completed": summary["skills_completed"],
        "skills_completed_count": len(summary["skills_completed"]),
        "hints_used_count": len(summary["hints_used"]),
    }


def submit_to_leaderboard(summary, entry_id):
    worksheet = get_worksheet()
    records = worksheet.get_all_records()
    existing_index = next((idx for idx, row in enumerate(records) if str(row.get("id", "")) == entry_id), None)
    existing_entry = normalize_entry(records[existing_index]) if existing_index is not None else None
    entry = leaderboard_entry(summary, entry_id, existing_entry)

    if existing_index is None:
        worksheet.append_row(entry_to_row(entry), value_input_option="USER_ENTERED")
    else:
        worksheet.update(f"A{existing_index + 2}", [entry_to_row(entry)])
    return entry


def sorted_leaderboard(entries):
    return sorted(
        entries,
        key=lambda entry: (
            entry.get("score", 0),
            entry.get("required_activities_completed", 0),
            entry.get("skills_completed_count", 0),
            -entry.get("hints_used_count", 0),
        ),
        reverse=True,
    )


def leaderboard_rows(entries, include_email=False):
    rows = []
    for rank, entry in enumerate(sorted_leaderboard(entries), start=1):
        row = {
            "Rank": rank,
            "Team name": entry.get("team_name", ""),
            "Gene": entry.get("assigned_gene", ""),
            "Score": entry.get("score", 0),
            "Progress": entry.get("progress", ""),
            "Skills": entry.get("skills_completed_count", 0),
            "Hints": entry.get("hints_used_count", 0),
            "Updated": entry.get("updated_at_utc", ""),
        }
        if include_email:
            row["Email"] = entry.get("email", "")
            row["Skills completed"] = "; ".join(entry.get("skills_completed", []))
        rows.append(row)
    return rows
