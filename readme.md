# Bugzilla Data Analysis Toolkit

This repository contains a set of Python scripts to **extract, process, classify, and analyze bug reports and developer collaboration patterns** from Bugzilla data. The workflow enables fetching bug data, parsing historical dumps, classifying issues into periods, generating collaboration graphs, and computing network metrics.

---

## 📂 Repository Contents

### 1. `downloadBugs.py`
- Fetches **resolved bug reports** from the [Bugzilla API](https://bugzilla.mozilla.org/).
- Collects **comments between 2020–2025** with developer information.
- Saves data in:
  - `resolved_bugs_comments_2020_2025.json` (full structured data)
  - `resolved_bugs_comments_2020_2025.csv` (flattened table format for analysis)

--

### 2. `parseSQLDump.py`
- Parses a **MySQL dump** of the Bugzilla database to extract earliest change dates for issues.
- Updates an existing `master.csv` file by filling in:
  - `first_comment_date`
  - `last_comment_date`
- Ensures consistency for later classification.

---

### 3. `classifyBugs.py`
- Classifies bugs into **5 time periods** based on first/last comment dates.
- Uses fixed start (`2012-03-18`) and end (`2015-02-06`) dates.
- Adds a new column `period` to the dataset.
- Outputs `output.csv` with classification results.

---

### 4. `generateGraph.py`
- Processes classified CSV files (`data_202{period}.csv`).
- Builds **bug-to-developers mappings**.
- Assigns unique IDs to authors.
- Outputs:
  - `author_mapping.json` (developer name → ID)
  - `bug_devs.json` (bug ID → developer IDs)

---

### 5. `metricsComputation.py`
- Computes **graph/network metrics** from Pajek `.net` files (collaboration networks).
- Metrics include:
  - Degree, betweenness, closeness, eigenvector centralization
  - Global clustering coefficient
  - Assortativity
  - Density
  - Diameter
  - Average path length
  - Modularity
- Saves results into `allmetrics.csv`.

---

## ⚙️ Workflow Overview

1. **Download bugs** → `downloadBugs.py`  
2. **Parse SQL dump for dates** → `parseSQLDump.py`  
3. **Classify bugs into periods** → `classifyBugs.py`  
4. **Generate collaboration graph data** → `generateGraph.py`  
5. **Compute graph/network metrics** → `metricsComputation.py`  

---

## 🚀 Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bugzilla-analysis.git
   cd bugzilla-analysis

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run scripts in order depending on your dataset and analysis goals:
   ```bash
   python downloadBugs.py
   python parseSQLDump.py
   python classifyBugs.py
   python generateGraph.py
   python metricsComputation.py

## 📊 Example Outputs

- resolved_bugs_comments_2020_2025.csv → List of comments with metadata.
- output.csv → Bugs classified into 5 time periods.
- author_mapping.json → Developer ID mapping.
- bug_devs.json → Bug-to-developers relationships.
- graph202{period}.net → Pajek graph files.
- allmetrics.csv → Summary of computed graph/network metrics.
