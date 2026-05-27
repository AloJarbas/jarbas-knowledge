# Extracting the next public SDR note: carrier lock handoff survives as a small state machine

## Why this pass happened

`logs/current-state.md` still had `public-knowledge-repo` at the top of the ordered queue.
The standing rule was unchanged:
extract one more portable claim from the dense SDR branch only if it stays compact outside the source repo.

The live question this time was narrower than the earlier acquisition/tracking card:

> did the lock-detection / acquisition-to-tracking memo finally collapse into one public note without dragging ambiguity resolution and threshold tuning in with it?

This pass stayed on that exact question.

## Discovery intake before deciding

I did not want to trust the older memo blindly.
So I re-checked the broader intake first.

### Local Raindrop pass

The local Raindrop export only surfaced a general `PySDR` bookmark on this topic.
It did **not** surface a better saved lock-detection or handoff-specific source than the ones already in the SDR note lineage.

### HN-oriented pass

A broad HN-filtered local discovery pass did **not** surface a relevant SDR synchronization or carrier-lock discussion worth using here.

Conclusion:
this topic still wants direct technical sources, not discovery-driven commentary.

## Candidate repo artifacts inspected

### Accepted for extraction base

1. **`jarbas-sdr-visual-notes/notes/2026-05-16-carrier-lock-detection-handoff-research.md`**

   Accepted because it already had the right adversarial core:
   - one real public question,
   - one rejected metric candidate,
   - one compact three-state receiver story,
   - and one explicit boundary between carrier lock and QPSK labeling.

   The surviving claim is:

   > carrier lock handoff is not one threshold; it needs a “settled first, close second” state machine.

2. **`jarbas-sdr-visual-notes/notes/carrier-lock-detection-and-handoff.md`**

   Accepted because it proved the source branch already had a stable prose landing zone.
   That made it easier to extract a public card without inventing a new story from scratch.

### Rejected for this packaging pass

3. **`jarbas-sdr-visual-notes/notes/qpsk-phase-ambiguity-resolution.md`**

   Rejected for this pass because it is still a companion, not part of the smallest surviving claim.
   Folding it in would blur the exact distinction this new card is trying to protect.

4. **`public-knowledge-repo/notes/carrier-recovery-acquisition-tracking-card.md`**

   Rejected as the artifact to extend because it already does its job.
   Appending lock-state detail into it would make the older card worse instead of making the queue cleaner.

5. **A public formula-heavy metric card (`rho4`, `delta4`, Costas residual thresholds)**

   Rejected because the formulas are helpful in the source repo, but they make the public note feel more implementation-specific than portable.
   The public card survives better as a state-machine rule.

## External source review used to tighten the public note

I re-read multiple candidate sources and kept only the ones that still sharpened the extraction.

### Accepted for primary framing

1. **PySDR — Synchronization**  
   https://pysdr.org/content/sync.html

   Accepted because it keeps timing recovery, carrier recovery, and receiver staging in one continuous story.

2. **Wireless Pi — How to Detect a Carrier Lock in an SDR**  
   https://wirelesspi.com/how-to-detect-a-carrier-lock-in-an-sdr/

   Accepted because it states the operational reason lock detection exists at all: mode switching, reacquisition, and deciding when to trust the demod path.

3. **Wireless Pi — Non-Data-Aided Carrier Phase Estimation**  
   https://wirelesspi.com/non-data-aided-carrier-phase-estimation/

   Accepted because it preserves the acquisition-side lesson that blind symmetry methods are useful before decisions are trustworthy.

4. **Wireless Pi — Costas Loop for Carrier Phase Synchronization**  
   https://wirelesspi.com/costas-loop-for-carrier-phase-synchronization/

   Accepted because it keeps decision-directed tracking in its proper near-lock lane instead of pretending it is a whole cold-start story.

### Accepted as secondary only

5. **Learning SDR — Lesson 19**  
   https://pnsaeta.github.io/Learning_SDR/lesson19.html

   Accepted only as secondary visual phrasing for the rotating-constellation problem.

### Rejected for primary teaching use

6. **GNU Radio Costas Loop docs**  
   https://wiki.gnuradio.org/index.php/Costas_Loop

   Rejected because it is still a block reference and parameter page, not the cleanest public teaching source for lock-state handoff.

7. **MathWorks synchronization and receiver design catalog page**  
   https://www.mathworks.com/help/comm/synchronization-and-receiver-design.html

   Rejected because it confirms component separation, but mostly as a catalog index. It does not carry the public teaching load.

8. **Wireless Pi — How to Estimate the Carrier Phase**  
   https://wirelesspi.com/how-to-estimate-the-carrier-phase/

   Rejected as a primary source for this note because it is about pilot-aided phase estimation. Useful background, wrong center of gravity for a blind acquisition-to-tracking handoff card.

### Rejected metric framing

9. **Raw QPSK `|I|-|Q|` arm balance as the lead public lock metric**

   Rejected because the source-repo checks already showed it does not cleanly separate the states this public card needs.
   It is too easy to sound precise while actually hiding the candidate-lock ambiguity.

## What survived after source review

The memo did survive packaging, but only after dropping the temptation to publish a metric cookbook.

The note that survives is smaller and better:

> carrier lock handoff should ask two questions in order — has the constellation settled modulo 90°, and is the remaining residual small enough for decision-directed trust?

That claim is public-note worthy because it keeps four distinctions visible:

- acquisition and tracking are different jobs,
- “stable” is not the same thing as “close enough,”
- carrier lock is not the same thing as QPSK label resolution,
- and the public repo does not need to expose every source-repo formula to keep the lesson honest.

## Artifact-shape decision

This wanted to be a **small state-machine card**, not a figure-first note and not a threshold table.

Why:
- the public value is the handoff rule itself,
- the implementation metrics already live in `jarbas-sdr-visual-notes`,
- and keeping the card formula-light avoids recreating SDR sprawl in the public repo.

## Durable artifacts produced

1. **Stable public note**  
   `public-knowledge-repo/notes/carrier-lock-handoff-needs-two-tests.md`

2. **This dated packaging memo**  
   `public-knowledge-repo/notes/2026-05-27-carrier-lock-handoff-packaging-research.md`

3. **Index update**  
   `public-knowledge-repo/README.md`

4. **Queue update**  
   `logs/current-state.md`

## Backlog decisions

- **Do not** turn the public repo version into a `rho4` / `delta4` threshold cheat sheet.
  Keep that machinery in the source repo unless a future public figure clearly earns it.

- **Do not** merge this card into the earlier acquisition/tracking card.
  Two compact cards are cleaner than one overstuffed synchronization note.

- **Keep** QPSK ambiguity resolution as a separate companion.
  This card is better because it stops before that last branch.

## Best next move

Unless another SDR memo collapses this cleanly, let the queue fall through to `spectral-window-lab` instead of forcing more SDR packaging.
If SDR packaging returns later, keep the same bar: one portable claim, one clean boundary, no branch-summary bloat.

Jarbas
