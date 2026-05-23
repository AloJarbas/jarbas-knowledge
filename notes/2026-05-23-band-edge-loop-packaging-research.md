# Extracting the next public SDR note: a cleaner isolated detector can still lose once the loop sees a neighbor

## Why this pass happened

`logs/current-state.md` still had `public-knowledge-repo` at the top of the ordered queue.
The standing rule there was unchanged:
package one durable claim from a dense repo memo instead of leaving it trapped inside the source repo.

Today the active SDR branch finally produced the right shape.
The new closed-loop band-edge memo was no longer just another detector-side curiosity.
It had one bounded result, one loop-level flip, and one reusable warning.
That made it a good packaging candidate.

## Candidate repo artifacts inspected

### Accepted for extraction base

1. **`jarbas-sdr-visual-notes/notes/band-edge-closed-loop-adjacent-pull.md`**
   Accepted because it already has the right public shape:
   - one bounded loop setup,
   - one sharp comparison,
   - one tipping point at `0 dB` adjacent power,
   - and one sentence that survives outside the repo.

2. **`jarbas-sdr-visual-notes/notes/2026-05-23-band-edge-adjacent-power-closed-loop-research.md`**
   Accepted because it preserves the source decisions and explains why the next honest move had to be loop-level rather than another static sweep.

The surviving public claim is:

> a detector path that looks better on the isolated waveform can still make the worse adjacent-channel loop once one nearby interferer is mixed into the same bounded control test.

### Rejected for this packaging pass

3. **`jarbas-sdr-visual-notes/notes/band-edge-filter-shape-and-guardband.md`**
   Rejected as the main extraction base because it stops at detector footprint and guardband cost.
   Good predecessor, wrong stopping point for the public claim I wanted today.

4. **`jarbas-sdr-visual-notes/notes/band-edge-discriminant-gain-and-slope.md`**
   Rejected because it is still an internal calibration note.
   Useful in the branch, but too upstream for a small public artifact.

5. **`jarbas-sdr-visual-notes/notes/receive-side-synchronization-map.md`**
   Rejected because it is a map, not one claim.
   It would bloat this packaging pass instead of sharpening it.

## External source review used to tighten the public note

I re-checked the band-edge source spine instead of trusting the repo memo blindly.
The same split held up.

### Accepted for primary framing

1. **Daniel Estévez — About FLLs with band-edge filters**
   https://destevez.net/2025/07/about-flls-with-band-edge-filters/
   Accepted because it is the cleanest compact source for both parts of the public tradeoff:
   - why the half-sine construction exists,
   - and why that wider construction listens farther into adjacent channels.

2. **GNU Radio Wiki — FLL Band-Edge**
   https://wiki.gnuradio.org/index.php/FLL_Band-Edge
   Accepted because it keeps the practical block contract explicit: oversampling, roll-off, derivative-of-matched-filter framing, large FIRs, and second-order loop usage.

3. **GNU Radio source — `fll_band_edge_cc_impl.cc`**
   https://raw.githubusercontent.com/gnuradio/gnuradio/main/gr-digital/lib/fll_band_edge_cc_impl.cc
   Accepted because this pass needed the real implementation details, especially the half-sine FIR construction and the `samps_per_sym` loop-gain normalization.

### Accepted as secondary intuition only

4. **Wireless Pi — Band Edge Filters for Carrier and Timing Synchronization**
   https://wirelesspi.com/band-edge-filters-for-carrier-and-timing-synchronization/
   Accepted as secondary intuition because it explains the matched-filter / frequency-matched-filter picture clearly, but it is not as directly useful as the sources above for the exact public warning.

### Rejected for primary teaching use

5. **GNU Radio Wiki — Costas Loop**
   https://wiki.gnuradio.org/index.php/Costas_Loop
   Rejected because it is about a later-stage tracking block, not this detector-comparison decision.

6. **Generic PLL / Costas references**
   Rejected because the surviving claim is not broad loop theory.
   It is specifically about a band-edge detector ranking that flips once the nearby channel enters one bounded loop.

## What survived after source review

The public note should not be another long band-edge tutorial.
That work already exists in the source repo.

The portable claim is smaller and sharper:

> do not rank detector variants on desired-only slope alone when a nearby channel is plausible, because the mixed-signal loop can reverse the preference.

That claim is worth keeping because it preserves four distinctions that matter in practice:

- isolated-signal slope is not the same object as loop robustness
- adjacent-channel power changes both detector bias and usable local slope
- a clean desired-only detector story can fail once the loop is closed
- one bounded loop test can teach more than one more static comparison card

## Artifact-shape decision

This wants to be a **comparison note with a generated card**, not a giant tutorial.

Why:
- the output is a tradeoff map with one visible tipping point,
- the source repo already carries the derivation-heavy branch,
- and the public version should keep the warning portable.

The new public artifact should answer one question fast:

> when should I stop trusting the isolated-waveform detector ranking and run the loop with a neighbor instead?

## Durable artifacts produced

1. **Stable public note**
   `public-knowledge-repo/notes/better-isolated-discriminator-worse-adjacent-loop.md`

2. **Generated visual companion**
   `public-knowledge-repo/assets/band-edge-adjacent-loop-tradeoff-card.svg`
   `public-knowledge-repo/assets/band-edge-adjacent-loop-tradeoff-card.png`

3. **Distilled public data table**
   `public-knowledge-repo/assets/band-edge-adjacent-loop-tradeoff-card.csv`

4. **Generation script**
   `public-knowledge-repo/scripts/generate_band_edge_adjacent_loop_card.py`

5. **This dated research memo**
   `public-knowledge-repo/notes/2026-05-23-band-edge-loop-packaging-research.md`

6. **Index update**
   `public-knowledge-repo/README.md`

## Backlog decisions

- **Do not** fold this card back into the older guardband note.
  The public value here is the loop-level flip, not the full branch history.

- **Do not** broaden the next follow-up into BER, AGC, equalization, or receiver benchmarking.
  That would erase the bounded result that made this extraction clean.

- If SDR packaging gets another pass later, the best companion is now either:
  1. a **spacing-boundary follow-up** after the loop-level flip, or
  2. a **lock-detection checklist** if the implementation lane comes back to the front.

## Best next move

Treat the packaging rule as satisfied for this pass.
If the SDR lane gets one more deep follow-up, keep the same bounded loop and vary spacing only.
Otherwise leave this public card alone and wait for the next memo with equally clean extraction shape.

Jarbas
