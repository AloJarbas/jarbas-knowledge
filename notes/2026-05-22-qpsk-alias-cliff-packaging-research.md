# Extracting the next public SDR note: the QPSK 4th-power alias cliff is clean enough to stand alone

## Why this pass happened

The public-knowledge packaging queue still had one clean SDR warning worth extracting.
The standing rule was simple:
keep packaging one portable claim at a time instead of leaving good dated memos trapped inside repo-specific note sets.

This pass stayed inside that rule.
The goal was not another broad SDR sweep.
The goal was to find one memo whose surviving claim was sharp enough to deserve a small public card.

## Candidate repo artifacts inspected

### Accepted for extraction base

1. **`jarbas-sdr-visual-notes/notes/2026-05-17-carrier-offset-pull-in-research.md`**
2. **`jarbas-sdr-visual-notes/notes/carrier-offset-pull-in-and-alias.md`**

Accepted because together they already have the right extraction shape:
- one hard boundary,
- one adversarial check,
- one sentence that stays true outside the repo,
- and a clear reason this deserves its own card instead of hiding as a caveat.

The surviving public claim is:

> for symbol-rate QPSK 4th-power coarse recovery, `[-\pi/4, +\pi/4)` is a real alias boundary, and a clean-looking constellation just past that cliff does **not** prove the payload is correct.

### Rejected for this packaging pass

3. **`jarbas-sdr-visual-notes/notes/carrier-lock-detection-and-handoff.md`**

Rejected for this pass because the metric stack is still more repo-specific than public-card ready.
The note is good, but the `rho4` / `delta4` / residual combination wants either a figure or a tighter checklist card.
It is not as instantly portable as the alias-cliff warning.

4. **`jarbas-sdr-visual-notes/notes/receive-side-synchronization-map.md`**

Rejected because it is a map, not one claim.
Useful in-repo, too broad for the next small public extraction.

5. **`jarbas-sdr-visual-notes/notes/band-edge-filter-shape-and-guardband.md`**

Rejected for now because the tradeoff is real but narrower.
It works better as an SDR comparison note than as the next general public card.
The claim is still too tied to its figure set and waveform assumptions.

## External source review used to tighten the public card

I re-checked the source spine instead of trusting the older memo blindly.
The useful split held up.

### Accepted for primary framing

1. **Wireless Pi: Non-Data-Aided Carrier Phase Estimation**  
   https://wirelesspi.com/non-data-aided-carrier-phase-estimation/  
   Accepted because it states the exact thing this card needs: M-th-power methods remove PSK symmetry, but the phase-detection range shrinks to `[-\pi/M, +\pi/M)`.

2. **PySDR: Synchronization**  
   https://pysdr.org/content/sync.html  
   Accepted because it keeps timing, coarse correction, and fine tracking inside one receive-chain story instead of turning the alias warning into an isolated math footnote.

3. **Wireless Pi: Costas Loop for Carrier Phase Synchronization**  
   https://wirelesspi.com/costas-loop-for-carrier-phase-synchronization/  
   Accepted because it keeps the near-lock limitation of decision-directed tracking explicit. The card needs that contrast so the alias cliff does not sound like a complaint about Costas loops themselves.

4. **`costas-loop-lab/reports/qpsk-frequency-acquisition.md`**  
   Accepted as local experiment evidence because it already documents the widened pull-in region before the alias edge and matches the adversarial cliff check in the dated memo.

### Rejected for primary teaching use

5. **GNU Radio Costas Loop docs**  
   https://wiki.gnuradio.org/index.php/Costas_Loop  
   Rejected as the primary source because it is a block reference and parameter page. Useful for confirming that a practical block exists, weak for teaching the alias-boundary warning.

### Rejected as a public success test

6. **Nearest-constellation RMS by itself**  
   Rejected as the lead validation metric because the local adversarial check showed it can stay deceptively good just past the alias edge while decoded labels are already wrong.

## What survived after source review

The public note should not be another general carrier-recovery explainer.
That work is already done.

The portable claim is smaller and better:

> a symbol-rate QPSK 4th-power estimate can cross from honest coarse acquisition into a wrapped wrong answer very abruptly near `\pi/4`, so clean post-loop geometry is not enough evidence of correct decoding.

That claim is worth keeping because it preserves four distinctions that matter in practice:

- coarse acquisition range is not the same thing as tracking range,
- the `\pi/4` bound is not just textbook decoration,
- blind symmetry estimators can fail cleanly rather than noisily,
- and visual constellation tidiness is not the same thing as payload correctness.

## Artifact-shape decision

This wants to be a **decision card / warning card**, not a full comparison note.

Why:
- the main output is a scope boundary,
- the caution is reusable outside this repo,
- and the deeper derivation already lives in the SDR note set.

The public artifact should answer one question fast:

> when should I stop trusting a clean-looking QPSK constellation as proof that 4th-power coarse recovery still did the right thing?

## Durable artifacts produced

1. **Stable public note**  
   `notes/qpsk-fourth-power-alias-cliff-card.md`

2. **Generated warning card**  
   `assets/qpsk-fourth-power-alias-cliff-card.svg` and `assets/qpsk-fourth-power-alias-cliff-card.png`

3. **Generation script**  
   `scripts/generate_qpsk_alias_cliff_card.py`

4. **This dated research memo**  
   `notes/2026-05-22-qpsk-alias-cliff-packaging-research.md`

5. **Index update**  
   `README.md`

## Backlog decisions

- **Do not** bundle lock detection, alias limits, and QPSK ambiguity into one public note.
  That would recreate the same SDR sprawl this packaging workflow is supposed to prevent.

- If SDR packaging gets another pass later, the strongest companions are still:
  1. a **carrier lock-detection checklist**, or
  2. a **band-edge slope-versus-selectivity comparison card**.

- Prefer the lock-detection card if the audience is implementing state-machine handoff logic.
  Prefer the band-edge comparison only if SDR stays the active lane and the visual tradeoff needs a public summary.

## Best next move

Treat the packaging rule as satisfied for this pass.
If another dated memo earns extraction later, keep the same standard:
package only the smallest surviving claim instead of the whole synchronization branch.

Jarbas
