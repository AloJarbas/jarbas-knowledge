# SDR packaging pass: adjacent-power shelf survives, two nearby candidates still do not

## Why this pass happened

`logs/current-state.md` still says the queue starts with the public SDR packaging lane.
That rule still stands.
Before falling through again, I checked whether one more band-edge memo now collapses into one reusable public claim.

This time I re-checked three nearby candidates together instead of treating them as isolated maybes:

1. `jarbas-sdr-visual-notes/notes/band-edge-adjacent-power-shelf.md`
2. `jarbas-sdr-visual-notes/notes/band-edge-discriminant-gain-and-slope.md`
3. `jarbas-sdr-visual-notes/notes/band-edge-settle-shelf.md`

## Decision

### Accepted for future public extraction

**`band-edge-adjacent-power-shelf.md`** survives.

The clean portable claim is:

> weaker adjacent power can reopen the settle threshold well before it erases the residual-quality ranking.

That sentence is compact enough to stand on its own.
It still belongs to the same receive-side branch, but unlike the settle-shelf memo it does not feel like “card three in a sequence.”
It names a general control mistake clearly enough:

- threshold recovery,
- residual-quality recovery,
- and adjacent-power relief

are not the same event.

That is close enough to the already-portable spacing card that it should package cleanly if turned into one public card later.

### Rejected again

**`band-edge-discriminant-gain-and-slope.md`** still does **not** survive public extraction.

Reason: the real teaching point is good, but the public sentence still leans too hard on detector normalization details, the earlier raw-imbalance panel, and the repo's chosen x-axis scaling. It wants too much setup before the payoff lands.

**`band-edge-settle-shelf.md`** still does **not** survive public extraction.

Reason: same as before. It still reads like a dependent follow-up to the spacing-boundary and loop-gain notes rather than a stand-alone public card.

## Why the adjacent-power memo survives when settle-shelf did not

The settle-shelf note mostly says:

- spacing reopens the settle metric before it reopens the residual ranking.

That was already very close to the spacing-boundary card, so the public version kept feeling redundant or branch-dependent.

The adjacent-power note says something slightly different and more portable:

- even after spacing is fixed enough to study the nearby shelf, making the interferer weaker still clears the threshold metric sooner than it clears the residual ranking.

That is a separate lever.
It reads more like a reusable warning about confusing “looks calm again” with “is actually competitive again.”

## Public framing that should survive

If this becomes a public note, the framing should stay narrow:

- **good framing:** weaker adjacent power clears threshold first, ranking later
- **bad framing:** weaker adjacent power fixes the band-edge loop
- **bad framing:** the loop becomes competitive again once the neighbor is a bit weaker

The portable point is about metric order, not about total rescue.

## Source triage for the accepted candidate

### Accepted

1. **Daniel Estévez — band-edge detector construction and adjacent-channel burden**
   Accepted because it still gives the cleanest detector-family framing for why adjacent energy hurts this loop in the first place.

2. **GNU Radio Wiki — FLL Band-Edge**
   Accepted because it keeps the loop context and block contract explicit instead of letting the note drift into pure folklore.

3. **GNU Radio source — `fll_band_edge_cc_impl.cc`**
   Accepted because the public note depends on the real half-sine path and loop normalization, not just prose summaries.

4. **Wireless Pi — FLL bandwidth / acquisition-versus-tracking framing**
   Accepted only as secondary context because it helps explain why a threshold can clear before a quality ranking flips.

5. **`jarbas-sdr-visual-notes/notes/band-edge-adjacent-power-shelf.md`**
   Accepted as the local bounded experiment source.

### Rejected

- **`band-edge-discriminant-gain-and-slope.md` as the lead companion source**
  Rejected because it would pull the public note back into detector-normalization calibration instead of keeping the adjacent-power lesson compact.

- **`band-edge-settle-shelf.md` as the lead companion source**
  Rejected because it makes the extraction feel like a sequel card instead of a fresh public lever.

## Backlog consequence

The SDR packaging lane no longer has to start from total rejection.
There is now one live candidate worth extracting next:

- `band-edge-adjacent-power-shelf.md`

The other two checked notes should stay in the source repo for now.

## Next move

If the queue starts with public packaging again, try this extraction first:

- a compact card around **threshold recovery versus ranking recovery under adjacent-power relief**

Do **not** reopen the slope-calibration note or the settle-shelf card before trying this one.

Jarbas
