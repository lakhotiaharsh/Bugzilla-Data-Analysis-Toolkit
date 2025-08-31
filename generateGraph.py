import re
import csv
import networkx as nx
from collections import defaultdict

# ----------------------------
# Step 1: Load bug → period mapping
# ----------------------------
bug_period = {}
with open("E:/fyp/bugs_updated_eclipse2.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        bug_period[int(row["issue.id"])] = int(row["period"])
print("Load bug → period mapping")
# ----------------------------
# Step 2: Parse .mysql file to extract (bug_id, submitted_by)
# ----------------------------
bug_devs = defaultdict(set)  # bug_id -> set of developers

pattern = re.compile(
    r"\((\d+),\s*(\d+),\s*NULL,.*?,\s*(\d+),"
)  
# Matches: (id, issue_id, comment_id=NULL, text, submitted_by, ...)

with open("E:/fyp/tickets.mysql", "r", encoding="utf-8") as f:
    for line in f:
        for match in pattern.finditer(line):
            issue_id = int(match.group(2))
            submitted_by = int(match.group(3))
            bug_devs[issue_id].add(submitted_by)
print("Parse .mysql file to extract (bug_id, submitted_by)")
# ----------------------------
# Step 3: Build graphs per period
# ----------------------------
graphs = {p: nx.Graph() for p in range(1, 6)}

for bug, devs in bug_devs.items():
    if bug not in bug_period:
        continue
    period = bug_period[bug]
    G = graphs[period]

    devs = list(devs)
    for i in range(len(devs)):
        for j in range(i + 1, len(devs)):
            u, v = devs[i], devs[j]
            if G.has_edge(u, v):
                G[u][v]["weight"] += 1
            else:
                G.add_edge(u, v, weight=1)
print("Build graphs per period")
# ----------------------------
# Step 4: Save graphs as Pajek .net
# ----------------------------
for period, G in graphs.items():
    nx.write_pajek(G, f"period_{period}_eclipse2.net")
print("Save graphs as Pajek .net files")
