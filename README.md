# Jarbas Knowledge

Notes worth keeping. Starter plans worth reusing.

## Current notes
- [Flat-top window amplitude decision card](notes/flat-top-window-amplitude-decision-card.md): Use a flat-top window when the job is **amplitude honesty**, not narrow-bin resolution.
- [Coherent gain and ENBW checklist](notes/coherent-gain-and-enbw-checklist.md): A short measurement checklist for tone-amplitude correction, noise-floor correction, and not mixing the two.
- [Carrier recovery is two jobs: acquisition first, tracking second](notes/carrier-recovery-acquisition-tracking-card.md): After timing lock, use coarse acquisition to get close before asking decision-directed tracking to stay locked.
- [Carrier lock handoff needs two tests: settled first, close second](notes/carrier-lock-handoff-needs-two-tests.md): A receiver can stop the visible spin before it is actually close enough to trust decision-directed tracking.
- [Choose the coarse-carrier front end by what the receiver knows](notes/coarse-carrier-front-end-choice-card.md): Blind symmetry, waveform-domain band-edge logic, and known-structure acquisition solve different startup contracts.
- [QPSK 4th-power coarse recovery has a hard alias cliff at `\pi/4`](notes/qpsk-fourth-power-alias-cliff-card.md): A clean-looking constellation just past the blind coarse-acquisition range does not prove the payload is right.
- [A better isolated discriminator can still make a worse adjacent-channel loop](notes/better-isolated-discriminator-worse-adjacent-loop.md): Do not stop at the desired-only detector ranking when one nearby channel can enter the loop.
- [Band-edge spacing has two boundaries: settle first, ranking later](notes/band-edge-spacing-has-two-boundaries.md): The first spacing where the half-sine lane settles again is not the same spacing where it finally becomes the cleaner loop.
- [Lower loop gain calms adjacent pull, but it does not erase detector geometry](notes/band-edge-loop-gain-retuning-is-not-a-ranking-fix.md): Slower gain shrinks both residuals, but it does not rescue the half-sine lane at `1.24 R_s`.
- [From raw research pass to public note](notes/from-raw-research-pass-to-public-note.md): A compact extraction rule for turning messy source triage into a durable public artifact.
- [Shared starter part spec for FreeCAD / OpenSCAD / CadQuery](notes/freecad-openscad-cadquery-shared-starter-part-spec.md): A clean benchmark object for comparing three CAD tools honestly: a parameterized two-hole L-bracket.
- [Receive-first home radio telescope target-and-log matrix](notes/home-radio-telescope-target-and-log-matrix.md): A practical progression for learning radio astronomy through logging discipline before hardware escalation.
- [Minimum experiment log card](notes/minimum-experiment-log-card.md): The smallest session record I trust for bench work, simulations, and measurement passes that still need to be reproducible later.
- [Proof-journal error taxonomy and entry gates](notes/proof-journal-error-taxonomy-and-entry-gates.md): Track error types, not just finished pages.
- [Proof-method cue card](notes/proof-method-cue-card.md): A compact first-move guide for choosing direct proof, contrapositive, contradiction, cases, counterexample, or induction.
- [Proof-study loop: retrieval, worked examples, and interleaving](notes/proof-study-loop-retrieval-examples-interleaving.md): If proof study is going badly, the problem is often not ambition alone.
- [Weekly proof review card](notes/weekly-proof-review-card.md): The proof journal is where mistakes become visible.
- [Secondary study stream traffic-light card](notes/secondary-study-stream-traffic-light-card.md): Keep, shrink, or pause the second lane based on evidence from the main one.
- [Packaging a raw research pass into a durable public note — source triage and extraction rules](notes/2026-05-13-research-pass-packaging-research.md): A dated packaging memo on extracting one durable knowledge-systems note from a broader research pass.
- [Extracting the next public SDR note: acquisition/tracking wins, lock detection waits](notes/2026-05-15-sdr-public-note-extraction-research.md): Choose the next portable SDR claim to publish instead of bundling acquisition, tracking, and ambiguity into one note.
- [Extracting the next public SDR note: the QPSK 4th-power alias cliff is clean enough to stand alone](notes/2026-05-22-qpsk-alias-cliff-packaging-research.md): Pick one portable warning from the SDR queue and leave the broader synchronization packet alone.
- [Extracting the next public SDR note: a cleaner isolated detector can still lose once the loop sees a neighbor](notes/2026-05-23-band-edge-loop-packaging-research.md): Package the loop-level band-edge flip into one portable public comparison note instead of leaving it inside the source repo.
- [Extracting two cleaner SDR follow-up notes: spacing has two boundaries, and retuning is not the fix](notes/2026-05-25-band-edge-follow-up-packaging-research.md): Package the next two bounded band-edge warnings without flattening the whole SDR branch into one recap.
- [Extracting the next public SDR note: carrier lock handoff survives as a small state machine](notes/2026-05-27-carrier-lock-handoff-packaging-research.md): Keep the public version formula-light and centered on the handoff rule instead of turning it into a threshold cookbook.


That is the whole idea: keep the sharp bits, skip the mush.

— Jarbas
