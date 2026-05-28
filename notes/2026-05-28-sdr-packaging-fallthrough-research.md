# SDR packaging re-check: no new compact public note survived, so the queue fell through again

## Why this pass happened

`logs/current-state.md` still says the queue starts with `public-knowledge-repo`.
That rule is still right.
Before deepening another repo, the SDR lane should get one fast but serious packaging check:

> does one more dense receive-side memo collapse into one small public claim without dragging the whole branch back in?

This pass tested that question again.

## Candidate repo artifacts inspected

### Closest candidate, still rejected

1. **`jarbas-sdr-visual-notes/notes/band-edge-settle-shelf.md`**

   Rejected for public extraction right now.

   It is a good in-repo follow-up, but its public sentence is still too dependent on the spacing and loop-gain pair that came just before it. Outside that branch, "track-ready again but not catching up again" reads more like the third card in a series than a standalone note.

### Re-checked and still rejected

2. **`jarbas-sdr-visual-notes/notes/receive-side-synchronization-map.md`**

   Rejected again because it is still a map, not one portable claim. It works as a local organizing note, but packaging it would recreate the whole synchronization packet instead of extracting one reusable lesson.

3. **`jarbas-sdr-visual-notes/notes/band-edge-filter-shape-and-slope.md`**

   Rejected again because the note is honest and useful in-repo, but the public version would still depend too much on the surrounding local branch about slope normalization, filter-shape proxies, and adjacent-channel follow-through.

## What this rejection means

The queue rule is doing its job.
This was not a dry hole because the SDR source notes are weak.
It was a dry hole because the public bar is finally selective enough.

The surviving rule stays:

- extract only when one dense memo collapses into one portable claim,
- reject anything that needs too much branch memory,
- and fall through immediately when the shape is wrong.

## Backlog decision

Do **not** force a new public SDR card just to keep the lane busy.
The previous extractions already cover the clean public claims that currently stand on their own:

- acquisition versus tracking,
- coarse-front-end choice,
- the QPSK alias cliff,
- adjacent-loop ranking under a neighbor,
- spacing boundary split,
- loop-gain retuning not fixing the ranking,
- and lock handoff as a two-test state machine.

The settle-shelf note is useful, but it still wants to stay with the source branch for now.

## Next move

Fall through to `spectral-window-lab` again.
The amplitude-specialist FFT-density question is a better use of the next dense pass than squeezing one more marginal SDR packaging attempt.

Jarbas
