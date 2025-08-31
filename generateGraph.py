import csv
import json
from collections import defaultdict

# bug_id -> set of developer IDs
bug_devs = defaultdict(set)

# Mapping author names to unique IDs
author_to_id = {}
next_id = 1

def get_author_id(author_name):
    global next_id
    if author_name not in author_to_id:
        author_to_id[author_name] = next_id
        next_id += 1
    return author_to_id[author_name]

# Load CSV file (bug_id, comment_author)
def print(period):
    with open(f"E:/fyp/data_202{period}.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # assumes first row has headers: bug_id, comment_author
        for row in reader:
            bug_id = row.get("bug_id")
            author_name = row.get("comment_author")

            if bug_id and author_name:  # Ensure both exist
                submitted_by = get_author_id(author_name)
                bug_devs[bug_id].add(submitted_by)

    # Save author mapping (author -> ID)
    with open("E:/fyp/author_mapping.json", "w", encoding="utf-8") as f:
        json.dump(author_to_id, f, indent=4)

    # (Optional) Save bug -> developers mapping
    with open("E:/fyp/bug_devs.json", "w", encoding="utf-8") as f:
        json.dump({k: list(v) for k, v in bug_devs.items()}, f, indent=4)

for period in range(1,6):
    print(period)