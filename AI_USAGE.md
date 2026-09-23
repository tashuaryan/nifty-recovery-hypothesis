 AI USAGE NOTE

Tools used
Claude (Anthropic).

 How I used it
- Planning: neatly planed the assignment into steps making it easier for me to focus and not become overwhelmed with the project as i had limited time because of my internals exam .
- Code: first drafts of config.py, data_loader.py, validation.py,
  events.py, stats.py, backtest.py and robustness.py, one file at a time.
- Writing: first drafts of research_note.md and README.md, which I then
  filled with the results of my own runs.

 My own decisions
- Created the GitHub repo, created and organised every file, and set up
  the Python environment on my machine.
- Ran every code and re checked my output and data and then confirmed from ai.
- Did research about the market 2% drop significance in real life and how much it generally effect.
- Talked to my friend who does investment in ipo asked about real opnion.

Suggestions I disagreed with or had corrected
- Told me to retype `src/` in the filename box when I was already inside
  the src folder. I pointed out I had not typed it and that it was
  already there, and the AI corrected itself.
- Claimed my README, AI note and other root files were inside `src` on
  GitHub. I checked and they were in the main folder; the AI had misread
  the file tree and withdrew the claim.
- opposed the idea of taking 1.2% drop because i wanted significant dip.

 What I learned
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
