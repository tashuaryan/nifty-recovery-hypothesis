# AI Usage Note

## Tools used
Claude (Anthropic), via chat, throughout the project.

## How I used it
- Planning: turning the assignment into a research design (event and
  recovery definitions, entry/exit rules, test/OOS split) and a repo
  structure before writing code.
- Code: first drafts of config.py, data_loader.py, validation.py,
  events.py, stats.py, backtest.py and robustness.py, one file at a time.
- Writing: first drafts of research_note.md and README.md, which I then
  filled with the results of my own runs.
- Debugging: setup problems (VS Code, virtual environment, a Windows
  security policy blocking a pandas DLL, running scripts with `python`).

## My own decisions
- Created the GitHub repo, created and organised every file, and set up
  the Python environment on my machine.
- Ran every script locally and pasted the real outputs back; all numbers
  in the research note come from my own runs, not from the AI.
- When the GitHub file steps got confusing, I chose to delete that repo
  and start a new one, and I chose to work in VS Code instead.
- I kept the AI's proposed design choices (-2% threshold, next-day-open
  entry, 10 bps per side costs, skipping overlapping events) unchanged,
  and put them in config.py so they can be changed in one place.

## Suggestions I disagreed with or had corrected
- Told me to retype `src/` in the filename box when I was already inside
  the src folder. I pointed out I had not typed it and that it was
  already there, and the AI corrected itself.
- Claimed my README, AI note and other root files were inside `src` on
  GitHub. I checked and they were in the main folder; the AI had misread
  the file tree and withdrew the claim.

## What I learned
- Statistical significance is not the same as trading significance: the
  10-day effect is positive on average but not significant, and the
  strategy earns less than buy-and-hold.
- Bootstrap tests and confidence intervals show how uncertain an average
  is; here every interval includes zero.
- Overlapping events and testing many parameter combinations can inflate
  results (data snooping), so I report the whole robustness table instead
  of picking the best cell.

## Limits
I did not independently re-implement the calculations, and costs and the
overlap rule are assumptions. AI-generated code can produce
plausible-looking but wrong numbers, so results should be read with that
in mind.