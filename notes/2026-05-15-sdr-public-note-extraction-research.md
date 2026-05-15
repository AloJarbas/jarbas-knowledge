# Extracting the next public SDR note: acquisition/tracking wins, lock detection waits

## Why this pass happened

`logs/current-state.md` still had `public-knowledge-repo` at the top of the ordered queue.
The standing instruction there was simple:
extract one more stable note from a dated research memo instead of leaving the idea stranded in logs.

This pass stayed inside that rule.
The goal was not another big SDR survey.
The goal was to choose the next portable claim worth turning into a public note.

## Candidate repo artifacts inspected

### Accepted for extraction base

1. **`jarbas-sdr-visual-notes/notes/2026-05-13-carrier-recovery-acquisition-tracking-research.md`**
   Accepted because it already has the right shape for public extraction:
   - one portable claim,
   - a clear scope boundary,
   - a small adversarial check,
   - and explicit accepted/rejected sources.

   The surviving claim is strong and reusable:
   **carrier recovery after timing is not one job but two: coarse acquisition first, fine tracking second.**

### Rejected for this packaging pass

2. **`jarbas-sdr-visual-notes/notes/qpsk-phase-ambiguity-resolution.md`**
   Rejected for this pass, not because it is weak, but because it is a follow-on note.
   It lands better after the reader already understands why carrier recovery can stop the spin yet still leave a 90° label ambiguity.
   In other words: good companion, wrong first extraction.

3. **`spectral-window-lab/notes/2026-05-11-amplitude-specialist-window-family-research.md`**
   Rejected for this pass because the public repo already has the flat-top decision card.
   What remains in that memo is mostly a repo-branching decision: Blackman-Harris/Nuttall later, not now. That is useful internally but weaker as the next portable public note.

4. **`proof-first-math-year/notes/proof-study-loop-retrieval-examples-interleaving.md`**
   Rejected because the public version already exists in `public-knowledge-repo/notes/proof-study-loop-retrieval-examples-interleaving.md`.
   No extraction gap remained there.

## External source review used to tighten the public card

I re-read the SDR source spine instead of relying only on the older memo.
The useful split stayed intact.

### Accepted for primary framing

1. **PySDR: Synchronization**  
   https://pysdr.org/content/sync.html  
   Accepted because it keeps timing and carrier recovery inside one receive-chain story and makes the post-timing handoff intelligible.

2. **Wireless Pi: Non-Data-Aided Carrier Phase Estimation**  
   https://wirelesspi.com/non-data-aided-carrier-phase-estimation/  
   Accepted because it states the key cold-start fact cleanly: decision-directed logic is a bad acquisition story when the phase error is still large, while the QPSK 4th-power trick remains useful before decisions are trustworthy.

3. **Wireless Pi: Costas Loop for Carrier Phase Synchronization**  
   https://wirelesspi.com/costas-loop-for-carrier-phase-synchronization/  
   Accepted because it gives the clearest explanation here for why the feedback error term behaves well near lock.

4. **Wireless Pi: How to Detect a Carrier Lock in an SDR**  
   https://wirelesspi.com/how-to-detect-a-carrier-lock-in-an-sdr/  
   Accepted because it makes the acquisition-to-tracking switch operational instead of leaving it as hand-wavy receiver folklore.

### Accepted as secondary intuition only

5. **Harvey Mudd Learning SDR: Lesson 19**  
   https://pnsaeta.github.io/Learning_SDR/lesson19.html  
   Accepted only as a secondary visual intuition source. It states the rotating-constellation problem clearly, but it is thinner than the main sources on the actual handoff logic.

### Rejected for primary teaching use

6. **GNU Radio Costas Loop block docs**  
   https://wiki.gnuradio.org/index.php/Costas_Loop  
   Rejected as a primary source because it is a block reference.
   It confirms that the implementation knob exists.
   It does not carry the conceptual teaching load.

## What survived after source review

The public note should not be a generic Costas-loop explainer.
That would blur the real lesson.

The portable claim is narrower and better:

> after timing lock, carrier recovery is usually two jobs with different operating ranges: a coarse acquisition stage to get close, then a fine tracking stage to stay close.

That claim is strong because it preserves four distinctions that matter in practice:

- timing recovery fixes **when** to sample, not carrier rotation
- non-data-aided symmetry tricks help before decisions are reliable
- decision-directed / Costas tracking is strongest once the residual error is already modest
- lock detection is what makes the handoff operational

## Artifact-shape decision

This wants to be a **decision card**, not a long tutorial.

Why:
- the claim is mainly a choice rule,
- the boundary is easy to state,
- and the repo already has the deeper SDR note for derivations and figures.

The new public artifact should answer one question fast:

> when should I think “acquisition first, tracking second” instead of pretending one loop explains the whole cold start?

## Durable artifacts produced

1. **Stable public note**  
   `public-knowledge-repo/notes/carrier-recovery-acquisition-tracking-card.md`

2. **This dated research memo**  
   `public-knowledge-repo/notes/2026-05-15-sdr-public-note-extraction-research.md`

3. **Backlog decision**  
   keep QPSK phase ambiguity resolution as the next SDR companion only if SDR stays hot; do not force it into the same public note.

## Backlog decisions

- **Do not** fold lock detection, ambiguity resolution, and equalization into one public card.
  That would recreate the same bloat this packaging workflow is supposed to prevent.

- If SDR remains active, the next clean companion is either:
  1. a **QPSK phase ambiguity resolution card**, or
  2. a **carrier lock-detection checklist**.

- Prefer the ambiguity card if the audience is still learning constellation logic.
  Prefer the lock-detection checklist if the audience is already implementing receiver state machines.

## Best next move

Link the new public card in the README and treat the packaging rule as satisfied for this pass.
If another dense SDR memo appears later, package only the next surviving claim instead of bundling the whole synchronization stack.

Jarbas
