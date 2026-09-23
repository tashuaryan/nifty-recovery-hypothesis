"""
Central configuration for the NIFTY recovery research project.
Change values here — never hardcode thresholds/dates inside notebooks or scripts.
"""

# --- Date range ---
START_DATE = "2007-09-17"   # will confirm after checking actual data coverage
END_DATE = "2026-09-01"

# --- Event definition ---
EVENT_THRESHOLD = -0.02     # -2% single-day close-to-close fall

# --- Holding periods to test (in trading days) ---
HOLDING_PERIODS = [1, 3, 5, 10]

# --- Out-of-sample split ---
OOS_SPLIT_DATE = "2021-01-01"   # research/dev before this, OOS after

# --- Transaction costs (per side, in basis points) ---
ENTRY_COST_BPS = 10
EXIT_COST_BPS = 10

# --- Overlapping events handling ---
EXCLUDE_OVERLAPPING_EVENTS = True
