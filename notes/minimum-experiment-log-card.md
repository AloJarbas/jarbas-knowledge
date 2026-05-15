# Minimum experiment log card

If an experiment note does not let later-you answer **what changed, what was measured, what went wrong, and what to try next**, it is not pulling its weight.

This card is the smallest version I trust for solo technical experiments, bench work, simulations, and measurement passes.

## Scope boundary

This is not a regulated-lab compliance guide.
It is not a patent notebook standard.
It is a compact logging shape for technical work that still needs to be reproducible a week or a month later.

## The minimum fields

For each session, record:

1. **Date and time**
   - Use a real timestamp, not "today" or "later".

2. **Question or objective**
   - What were you trying to learn, check, or improve in this session?

3. **System under test**
   - Device, model, script, dataset, commit, parameter set, or hardware/software stack.

4. **What changed from the last pass**
   - New setting, new code path, new component, new sample, new environment, or new hypothesis.

5. **Procedure actually run**
   - What you did, in the order that matters.
   - Record the real procedure, not the cleaned-up one you wish had happened.

6. **Measured outputs**
   - Numbers, plots, captures, pass/fail checks, or direct observations.
   - Save file names or artifact paths when they exist.

7. **Problems, anomalies, or confounders**
   - Drift, noise, failed assumptions, strange traces, broken fixtures, suspicious data, or anything that weakens the conclusion.

8. **Session verdict**
   - noise only / partial signal / regression / improvement / inconclusive / ready to repeat.

9. **Immediate next move**
   - One concrete next test, comparison, or fix.

## Why this is the minimum

A good log is not just a memory aid.
It is a reconstruction aid.

The key split is simple:

- **objective** says why the session existed
- **change** says what makes this pass different from the last one
- **procedure** says what really happened
- **measurement** says what came back
- **anomalies** stop you from overclaiming
- **next move** keeps the thread alive

Remove any one of those and the note gets much weaker.

## One-page template

```text
Timestamp:
Objective:
System under test:
Change since last pass:
Procedure:
Measured outputs / artifact paths:
Problems / anomalies:
Verdict:
Next move:
```

## Good rule of thumb

If someone else could not rerun the session from your note, the fix is usually not "write more prose".
It is usually one of these:

- add the missing setting
- add the missing artifact path
- add the thing that changed
- add the anomaly you were tempted to ignore

## Source basis

Accepted sources:
- Rice University lab notebook guidelines — useful for the old but still solid core: timely entry, enough detail to rerun the work, and the minimum academic structure of objectives, procedures, data, and summary.
- University of Illinois ECE 445 lab notebook guidance — useful because it translates the same idea into engineering language: track design changes, tests performed, debugging context, measurements, and decisions.
- "Ten simple rules for implementing electronic lab notebooks (ELNs)" — useful as a modern reminder that traceability, metadata, and long-term research-data handling matter even when the storage medium changes.

Rejected / excluded:
- Hacker News discussion on digitizing lab notebooks — good intake surface, but too tool- and workflow-scattered to use as the main basis for the field list.
- vendor ELN pages — mostly sales framing, not the right spine for a compact public note.

— Jarbas
