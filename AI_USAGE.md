# AI Usage Note

## Tool used
Claude (Anthropic), via chat, throughout the project.

## What I used it for
- Planning: turning the assignment into a research design (event and
  recovery definitions, entry/exit rules, test/OOS split) and a repo
  structure before writing any code.
- Code: first drafts of config.py, data_loader.py, validation.py,
  events.py, stats.py, backtest.py and robustness.py, delivered one file
  at a time.
- Writing: a first draft of research_note.md and README.md, which I then
  filled with my own run results.
- Debugging: walking me through setup problems (VS Code, virtual
  environment, a Windows security policy blocking a pandas DLL, running
  scripts with `python`, files created in the wrong folder on GitHub).

## What I did myself
- Created the GitHub repo, created and organised every file, and set up
  the Python environment on my machine.
- Ran every script locally and pasted the real outputs back; all numbers
  in the research note (events, p-values, backtest and robustness
  tables, crash dates) come from my own runs, not from the AI.
- Fixed the environment and folder-structure problems that came up.
- Accepted the AI's proposed design choices (-2% event threshold,
  next-day-open entry, 10 bps per side costs, skipping overlapping
  events) and kept them in config.py so they can be changed in one place.

## How I checked the AI's work
- Data validation script checks the data before any analysis (duplicates,
  ordering, invalid OHLC, non-positive prices).
- Entry at the next day's open to avoid look-ahead bias.
- Compared results across two overlap-handling versions and reported the
  difference (-2%/5d: +0.44% vs -0.18%) instead of hiding it.
- Reported non-significant results as non-significant rather than
  claiming an edge; robustness covers 20 threshold/holding combinations
  to avoid relying on one setting.

## Limits of my verification
I have not independently re-implemented the calculations, and costs and
the overlap rule are assumptions. AI-generated code can contain errors
that produce plausible-looking numbers; the results should be read with
that in mind.