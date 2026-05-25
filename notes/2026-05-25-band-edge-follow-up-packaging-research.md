# Extracting two cleaner SDR follow-up notes: spacing has two boundaries, and retuning is not the fix

## Why this pass happened

`logs/current-state.md` still had `public-knowledge-repo` at the top of the ordered queue.
The standing rule there was unchanged:
extract one durable claim from a dense repo memo instead of leaving it buried in the source branch.

By today, the two 2026-05-24 SDR follow-ups had both crossed the packaging bar.
They were no longer just more branch maintenance.
Each one had one bounded question and one portable answer.

That made this a good paired extraction pass.

## Candidate repo artifacts inspected

### Accepted for extraction base

1. **`jarbas-sdr-visual-notes/notes/band-edge-spacing-boundary.md`**
   Accepted because it now has the right public shape:
   - one controlled spacing sweep,
   - one portable two-boundary lesson,
   - and one sentence that survives outside the source repo.

   The surviving claim is:

   > the half-sine lane becomes track-ready again around `1.24 R_s`, but it does not win the mean-residual ranking until about `1.57 R_s`.

2. **`jarbas-sdr-visual-notes/notes/band-edge-loop-gain-retuning.md`**
   Accepted because it closes the obvious objection to the spacing note instead of wandering into generic loop folklore.

   The surviving claim is:

   > lower gain really does calm both loops, but at `1.24 R_s` it mostly rescales the same geometry penalty instead of fixing the ranking.

3. **The dated research memos behind both notes**
   - `jarbas-sdr-visual-notes/notes/2026-05-24-band-edge-spacing-boundary-research.md`
   - `jarbas-sdr-visual-notes/notes/2026-05-24-band-edge-loop-gain-retuning-research.md`

   Accepted because they keep the source triage honest and make it clear why these two public notes should stay compact instead of turning back into a branch history lesson.

### Rejected for this packaging pass

4. **`jarbas-sdr-visual-notes/notes/2026-05-16-carrier-lock-detection-handoff-research.md`**
   Rejected for this pass because it still wants a small state-machine card, not a quick append onto today’s band-edge pair.
   Strong candidate, wrong shape for this exact extraction run.

5. **`jarbas-sdr-visual-notes/notes/receive-side-synchronization-map.md`**
   Rejected because it is a map, not one portable claim.
   Pulling it in here would bloat both notes.

6. **A broad band-edge branch summary or index card**
   Rejected because the public value today is still the two bounded warnings, not one flattened recap of the whole branch.

## External source review used to tighten the public notes

I re-checked the source spine instead of trusting the repo memos blindly.
The same split held up.

### Accepted for primary framing

1. **Daniel Estévez — About FLLs with band-edge filters**  
   https://destevez.net/2025/07/about-flls-with-band-edge-filters/

   Accepted because it is still the cleanest compact source for both halves of the band-edge story:
   - why the half-sine path exists,
   - and why that wider construction can carry a real adjacent-channel burden.

2. **GNU Radio Wiki — FLL Band-Edge**  
   https://wiki.gnuradio.org/index.php/FLL_Band-Edge

   Accepted because it keeps the practical block contract explicit: oversampling, roll-off dependence, the power-difference discriminator, and loop usage.

3. **GNU Radio source — `fll_band_edge_cc_impl.cc`**  
   https://raw.githubusercontent.com/gnuradio/gnuradio/main/gr-digital/lib/fll_band_edge_cc_impl.cc

   Accepted because the public notes depend on the actual half-sine implementation path and the `samps_per_sym` loop-gain normalization, not just summary prose.

### Accepted as secondary only

4. **Wireless Pi — How a Frequency Locked Loop (FLL) Works**  
   https://wirelesspi.com/how-a-frequency-locked-loop-fll-works/

   Accepted only for the retuning note as a bandwidth / acquisition-versus-tracking reminder.
   Useful, but not specific enough to carry either claim by itself.

### Rejected for primary teaching use

5. **GNU Radio doxygen API page for `fll_band_edge_cc`**  
   https://www.gnuradio.org/doc/doxygen/classgr_1_1digital_1_1fll__band__edge__cc.html

   Rejected because it is mostly API scaffolding and adds little to either portable teaching point.

## What survived after source review

The public repo wanted **two compact comparison notes with generated cards**, not one giant tutorial.

The surviving paired claims are:

1. **Spacing note** — one nearby-channel loop can have an early settle boundary and a later residual-quality boundary.
2. **Retuning note** — lower gain can calm both loops while leaving the ranking essentially intact.

Together they protect against two lazy reactions:

- “spacing fixed it”
- “then the gain must still be wrong”

## Artifact-shape decision

This wanted two lightweight public notes with visual companions, not one prose wall.

Why:
- the source repo already carries the derivation-heavy branch,
- each follow-up has one fast public sentence,
- and the public value here is keeping the warnings portable.

## Durable artifacts produced

1. **Stable public notes**
   - `public-knowledge-repo/notes/band-edge-spacing-has-two-boundaries.md`
   - `public-knowledge-repo/notes/band-edge-loop-gain-retuning-is-not-a-ranking-fix.md`

2. **Generated visual companions**
   - `public-knowledge-repo/assets/band-edge-spacing-two-boundaries-card.{csv,svg,png}`
   - `public-knowledge-repo/assets/band-edge-loop-gain-retuning-card.{csv,svg,png}`

3. **Generation scripts**
   - `public-knowledge-repo/scripts/generate_band_edge_spacing_two_boundaries_card.py`
   - `public-knowledge-repo/scripts/generate_band_edge_loop_gain_retuning_card.py`

4. **This dated research memo**
   - `public-knowledge-repo/notes/2026-05-25-band-edge-follow-up-packaging-research.md`

5. **Index and queue updates**
   - `public-knowledge-repo/README.md`
   - `logs/current-state.md`
   - `GITHUB_PORTFOLIO.md`

## Backlog decisions

- **Do not** flatten the whole band-edge branch into one public summary note yet.
  The current value is still the paired bounded warnings.

- **Do not** keep reopening the retuning branch with more same-shape gain nudges.
  The public read is already good enough.

- **Keep** the lock-detection / acquisition-to-tracking state-machine note as the next SDR packaging candidate only if it can stay as compact as today’s pair.

## Best next move

If SDR packaging stays active, test whether the lock-detection / handoff memo can collapse into one small state-machine card without dragging in ambiguity resolution.
If it cannot, let the queue fall through to the next dormant repo instead of forcing another SDR extraction.

Jarbas
