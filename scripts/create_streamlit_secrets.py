#!/usr/bin/env python3
"""Create Streamlit secrets from a Google service-account JSON key."""

import argparse
import json
from pathlib import Path


def toml_string(value):
    return json.dumps(str(value))


def build_secrets(service_account, spreadsheet_id, worksheet_name):
    required = ["client_email", "private_key"]
    missing = [field for field in required if field not in service_account]
    if missing:
        raise SystemExit(f"Missing required JSON key fields: {', '.join(missing)}")

    lines = [
        "[leaderboard]",
        f"spreadsheet_id = {toml_string(spreadsheet_id)}",
        f"worksheet_name = {toml_string(worksheet_name)}",
        "",
        "[gcp_service_account]",
    ]
    lines.extend(
        f"{field} = {toml_string(value)}"
        for field, value in service_account.items()
    )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Create .streamlit/secrets.toml from a Google service-account JSON key."
    )
    parser.add_argument("--json-key", required=True, help="Path to the downloaded Google service-account JSON key.")
    parser.add_argument("--spreadsheet-id", required=True, help="Google Sheet ID from the spreadsheet URL.")
    parser.add_argument("--worksheet-name", default="Leaderboard", help="Leaderboard worksheet/tab name.")
    parser.add_argument("--output", default=".streamlit/secrets.toml", help="Output TOML path.")
    parser.add_argument("--force", action="store_true", help="Overwrite output file if it already exists.")
    args = parser.parse_args()

    json_path = Path(args.json_key)
    output_path = Path(args.output)

    if output_path.exists() and not args.force:
        raise SystemExit(f"{output_path} already exists. Re-run with --force to overwrite it.")

    service_account = json.loads(json_path.read_text(encoding="utf-8"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        build_secrets(service_account, args.spreadsheet_id, args.worksheet_name),
        encoding="utf-8",
    )
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
