import re
import pandas as pd
from datetime import datetime

# === CONFIG ===
MYSQL_DUMP_FILE = "dump.mysql"
MASTER_CSV_FILE = "master.csv"

# Pattern to match INSERT INTO changes
insert_pattern_changes = re.compile(
    r"INSERT INTO\s+`changes`(?:\s*\(.*?\))?\s*VALUES\s*(.+);",
    re.IGNORECASE | re.DOTALL
)
values_pattern = re.compile(r"\((.*?)\)")

# Column positions in the VALUES tuple
ISSUE_ID_INDEX_CHANGES = 1
CHANGED_ON_INDEX_CHANGES = 6

# Dictionary to store first changed_on date per issue_id
change_dates = {}

print("Parsing changes table...")
with open(MYSQL_DUMP_FILE, "r", encoding="utf-8", errors="ignore") as f:
    buffer = ""
    for line in f:
        buffer += line
        if ";" not in line:
            continue  # wait until end of INSERT statement

        match = insert_pattern_changes.search(buffer)
        if match:
            values_str = match.group(1)
            for row in values_pattern.findall(values_str):
                # Split respecting quoted strings
                parts = re.findall(r"(?:'[^']*'|[^,]+)", row)
                parts = [p.strip().strip("'") for p in parts]
                try:
                    issue_id = parts[ISSUE_ID_INDEX_CHANGES]
                    changed_on = parts[CHANGED_ON_INDEX_CHANGES]
                except IndexError:
                    continue

                try:
                    date_obj = datetime.strptime(changed_on, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue

                # Keep the earliest change date only
                if issue_id not in change_dates:
                    change_dates[issue_id] = date_obj

        buffer = ""  # reset buffer after each statement

print(f"Found {len(change_dates)} issue IDs with change dates.")

# -----------------------------------------------------------------------------
# UPDATE EXISTING MASTER FILE
# -----------------------------------------------------------------------------
df = pd.read_csv(MASTER_CSV_FILE)
df['id'] = df['id'].astype(str)

# Ensure the date columns exist
if 'first_comment_date' not in df.columns:
    df['first_comment_date'] = None
if 'last_comment_date' not in df.columns:
    df['last_comment_date'] = None

filled_count = 0
for i, row in df.iterrows():
    issue_id = str(row['id'])
    if pd.isna(row['first_comment_date']) and pd.isna(row['last_comment_date']):
        if issue_id in change_dates:
            date_str = change_dates[issue_id].strftime("%Y-%m-%d %H:%M:%S")
            df.at[i, 'first_comment_date'] = date_str
            df.at[i, 'last_comment_date'] = date_str
            filled_count += 1

print(f"Filled {filled_count} rows from changes table.")

# Save back to same file
df.to_csv(MASTER_CSV_FILE, index=False)
print(f"Updated file saved: {MASTER_CSV_FILE}")
