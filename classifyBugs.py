import pandas as pd
from datetime import datetime, timedelta

# ==== CONFIGURATION ====
input_csv = "inputFilePath.csv"   # input CSV file
output_csv = "output.csv"  # output CSV file
date_format = "%Y-%m-%d %H:%M:%S"

# ==== LOAD DATA ====
df = pd.read_csv(input_csv)

# Ensure datetime columns are parsed
df['first_comment_date'] = pd.to_datetime(df['first_comment_date'], format=date_format)
df['last_comment_date'] = pd.to_datetime(df['last_comment_date'], format=date_format)

# ==== DEFINE PERIODS ====
start_date = datetime(2012, 3, 18, 2, 25, 40)
end_date   = datetime(2015, 2, 6, 5, 18, 19)

total_duration = end_date - start_date
split_duration = total_duration / 5

periods = []
period_start = start_date
for i in range(5):
    period_end = period_start + split_duration
    periods.append((period_start, period_end))
    period_start = period_end

# Add a small buffer for the last period to include the end time exactly
periods[-1] = (periods[-1][0], end_date)

# ==== CLASSIFICATION FUNCTION ====
def classify_bug(row):
    first = row['first_comment_date']
    last = row['last_comment_date']

    # Calculate time spent in each period
    time_in_period = [timedelta(0)] * 5

    for i, (p_start, p_end) in enumerate(periods):
        overlap_start = max(first, p_start)
        overlap_end = min(last, p_end)
        if overlap_end > overlap_start:
            time_in_period[i] = overlap_end - overlap_start

    # Determine dominant period
    max_time = max(time_in_period)
    max_indices = [i for i, t in enumerate(time_in_period) if t == max_time]

    if len(max_indices) == 1:
        return max_indices[0] + 1  # period index starts at 1
    else:
        # Tie: use last_comment_date to decide
        for i in reversed(range(5)):
            if periods[i][0] <= last <= periods[i][1]:
                return i + 1

# ==== APPLY CLASSIFICATION ====
df['period'] = df.apply(classify_bug, axis=1)
df.dropna(subset=['period'], inplace=True)
df['period'] = df['period'].astype(float).astype(int)  # Remove rows where period could not be determined
# ==== SAVE UPDATED FILE ====
df.to_csv(output_csv, index=False)

# ==== DISPLAY LEGEND ====
print("\nPeriod Legend:")
for i, (p_start, p_end) in enumerate(periods, start=1):
    print(f"Period {i}: {p_start.strftime(date_format)} → {p_end.strftime(date_format)}")

print(f"\nUpdated CSV saved to: {output_csv}")
