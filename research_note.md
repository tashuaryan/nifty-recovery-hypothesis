# Research Note: NIFTY Post-Fall Recovery

## Hypothesis
After a significant one-day fall in NIFTY, the index tends to recover
(show positive returns) over the subsequent N trading days.

## Event Definition
A day is flagged as a "significant fall" if the close-to-close daily
return is ≤ -2%. This threshold is roughly a 2+ sigma move given NIFTY's
typical daily volatility (~1%), rare enough to be meaningful while still
giving a workable sample size over the available history.

## Recovery Definition
Recovery = cumulative return from entry price to the close N trading
days later is positive. Reported across multiple holding periods rather
than a single cherry-picked N.

## Entry / Exit
- Entry: next trading day's open after the event day (the fall is only
  confirmed at that day's close, so next-day open is the earliest
  realistic, non-look-ahead entry point).
- Exit: close of day N after entry.

## Holding Periods
N = 1, 3, 5, 10 trading days, all reported.

## Test Period
[TO FILL IN once data is pulled — full available range from source]
Split into Research/Development (~75%) and Out-of-Sample (~25%, untouched
until final validation).

## Transaction Costs
Assumed 0.05%–0.10% per side (10–20 bps round trip), approximating
brokerage + market impact for a NIFTY index position via futures/ETF.

## Key Assumptions
- No leverage, single position at a time.
- Overlapping events (a second qualifying fall within a prior event's
  holding window) are excluded to avoid double-counting.
- Event detection uses close-to-close returns, not intraday extremes.
