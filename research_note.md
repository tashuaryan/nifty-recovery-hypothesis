# Do NIFTY 50 returns recover after significant one-day falls?

## Hypothesis
After a large one-day fall in the NIFTY 50, forward returns over the next
few days to weeks are higher than on normal days.

## Data
NIFTY 50 (^NSEI) daily OHLC from Yahoo Finance via yfinance, 2007-09-18 to
2026-09-23 (4,664 rows). Validated: no duplicates, correctly ordered, no
missing values, no invalid OHLC or non-positive prices.

## Event and Recovery Definitions
Event: close-to-close return <= -2%. 200 days qualified; 101 remained
after skipping events that overlap the holding window of an earlier event
(no double counting). Recovery: cumulative return from entry to the close
N trading days later, for N = 1, 3, 5, 10 (and 20 in robustness).

## Entry / Exit, Holding Period, Test Period
Entry: next trading day's open (the fall is only known at the close, so
this avoids look-ahead bias). Exit: close N days after the event day.
Full sample 2007-09-18 to 2026-09-23. In-sample: before 2021-01-01
(84 events). Out-of-sample: 2021-01-01 onwards (17 events).

## Transaction Costs
10 bps per side (20 bps round trip), an assumed approximation of brokerage
and market impact, not exchange-specific fee data.

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
Entry at next day's open, exit at the close N days after the event day,
one position at a time, 10 bps per side, cash earns 0% while flat.
- 101 trades per holding period. 10d: +0.81% mean net (median +1.05%,
  std 5.7%), win rate 55.4%. 5d: +0.44%. 3d: +0.39%. 1d: +0.09% with a
  negative median, so no edge.
- Out-of-sample (n=17): 10d +2.02% mean, 76% win rate. Small sample from
  one market regime, treated as encouraging, not confirming.
- Equity curve (daily mark-to-market), 10d hold: +91% total (3.5% CAGR),
  max drawdown -46%, in the market 22% of days. Buy and hold over the
  same period: +416% (9.0% CAGR), max drawdown -60%. The event strategy
  earns far less than holding NIFTY and still suffers a deep drawdown,
  so it is not an attractive standalone strategy.

## Robustness
Thresholds -1.5% to -3.0%, holds 1 to 20 days (20 combinations):
- 10 and 20 day holds are positive in most cases; the effect grows with
  deeper falls but trade counts shrink (31 trades at -3%/20d).
- 1 to 5 day holds are mostly negative or near zero after costs.
- Results are sensitive to how overlapping events are filtered
  (-2%/5d is +0.44% in the main backtest, -0.18% in robustness).
- Testing 20 combinations creates data-mining risk; no single best
  cell is claimed as the finding.

## Risk
Worst single trades: -21% (10d) and -29% (20d) at the -2% threshold;
-35% at -1.5%/20d. The worst 10-day outcomes cluster in the 2008
financial crisis (events on 2008-01-15, 2008-02-20, 2008-09-23,
2008-10-10, with 10-day forward returns of roughly -7% to -23%) and in
the pre-COVID fall of 2020-02-24 (about -12%). Buying falls fails badly
when the fall is the start of a crash.

## Challenging the Result
What would make me reject the hypothesis:
- A larger or later sample where the event-minus-baseline difference
  stays indistinguishable from zero (already true here: p = 0.115 to
  0.298) or turns negative.
- Out-of-sample means falling to zero or below as more post-2021 events
  accumulate (only 17 so far).
- Higher costs: the 10d edge disappears at about 100 bps round trip
  (+0.81% net at 20 bps). Slippage in a crash could approach this.
- Results that flip under a reasonable change of overlap rule (already
  seen: -2%/5d is +0.44% vs -0.18%).

Risks checked:
- Look-ahead bias: entry is the next open. Parameters (-2%, holds of
  1/3/5/10 days, the 2021-01-01 split) were fixed before results were seen.
- Out-of-sample purity: the robustness table prints out-of-sample means
  for every setting, so that period was viewed, though not used to
  choose parameters.
- Overlapping events, regimes (2008, 2020), sample size (101 overall,
  17 out-of-sample) and data quality are discussed above.

Statistical vs economic significance: no test is significant at 95%, and
economically the 10d strategy earns less than buy and hold (3.5% vs 9.0%
CAGR) with a -46% drawdown, so even a real drift would not make this a
worthwhile standalone strategy.

## Conclusion
Hypothesis: NIFTY recovers after big one-day falls. Method: -2% events,
next-open entry, bootstrap vs baseline, cost-adjusted backtest,
robustness sweep, out-of-sample split. Evidence: a modest positive drift
over 10 to 20 trading days, not statistically proven. Baseline: only
modestly above normal days. Robustness: fragile to overlap rules,
weaker at short holds. Out-of-sample: persisted but on just 17 events.
Verdict: not a validated trading strategy.

## Limitations
Single index and event type; regime effects; assumed costs; small
out-of-sample sample; no position sizing or stop-loss; 20 tested
parameter combinations.