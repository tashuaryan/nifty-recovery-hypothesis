# Do NIFTY 50 returns recover after significant one-day falls?

## Hypothesis
After a large one-day fall in the NIFTY 50, forward returns over the next
few days to weeks are higher than on normal days.

## Data
NIFTY 50 (^NSEI) daily OHLC from Yahoo Finance, 2007-09-18 to 2026-09-23
(4,664 rows). Validated: no duplicates, correctly ordered, no missing values,
no invalid OHLC or non-positive prices.

## Event Definition
A day is an event if its close-to-close return is <= -2%.
200 days qualified; 101 remained after skipping events that overlap the
holding window of an earlier event (no double counting).

## Recovery Definition
Cumulative return from entry to the close N trading days later, reported
for N = 1, 3, 5 and 10 (and 20 in robustness). Positive = recovery.

## Entry / Exit
Entry: next trading day's open (the fall is only known at the close, so
this avoids look-ahead bias). Exit: close of day N after the event day.

## Test Period
Full sample 2007-09-18 to 2026-09-23. In-sample: before 2021-01-01
(84 events). Out-of-sample: 2021-01-01 onwards (17 events).

## Transaction Costs
10 bps per side (20 bps round trip), an assumed approximation of brokerage
and market impact for a NIFTY instrument, not exchange-specific fee data.

## Statistical Evidence
Event forward returns vs all non-event days, bootstrap (10,000 resamples)
on the difference in means:
- Mean event return: +0.26% (1d), +0.58% (3d), +0.83% (5d), +1.14% (10d)
- Baseline: -0.00%, +0.08%, +0.15%, +0.35%
- Differences are positive at every horizon, but no 95% interval excludes
  zero (p = 0.115 to 0.298). Win rates are close to baseline
  (10d: 57.4% vs 56.3%).
Conclusion: suggestive, not statistically significant with 101 events.

## Backtest (net of costs)
- 10d: +0.81% mean, 55.4% win rate. 5d: +0.44%. 3d: +0.39%.
- 1d: +0.09% mean with a negative median, so effectively no edge.
- Out-of-sample (n=17): 10d +2.02%, 76% win rate. Small sample from one
  market regime; treated as encouraging, not confirming.

## Robustness
Thresholds -1.5% to -3.0%, holds 1 to 20 days (20 combinations):
- 10 and 20 day holds are positive in most cases; effect grows with
  deeper falls but trade counts shrink (31 trades at -3%/20d).
- 1 to 5 day holds are mostly negative or near zero after costs.
- Results are sensitive to how overlapping events are filtered
  (-2%/5d is +0.44% in the main backtest, -0.18% in robustness).
- Testing 20 combinations creates data-mining risk; no single best
  cell is claimed as the finding.

## Risk
Worst single trades: -21% (10d) and -29% (20d) at the -2% threshold;
-35% at -1.5%/20d. Buying falls fails badly when the fall is the start
of a crash.

## Conclusion
There is a modest positive drift after large NIFTY falls over 10 to 20
trading days, but it is not statistically proven, depends on design
choices, and carries severe drawdown risk. Not a validated trading strategy.

## Limitations
Single index, single event type; survivorship/regime effects; costs are
assumed; out-of-sample sample is small; no position sizing or stop-loss.