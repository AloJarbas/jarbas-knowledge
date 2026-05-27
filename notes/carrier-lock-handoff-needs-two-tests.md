# Carrier lock handoff needs two tests: settled first, close second

If a QPSK receiver treats carrier lock as one vague threshold, it hides two different questions:

1. **has the constellation stopped spinning modulo 90°?**
2. **is the remaining phase error small enough that decision-directed tracking is trustworthy?**

That is why acquisition-to-tracking handoff wants a small state machine, not one overconfident `lock=yes` bit.

## Use it for

- coarse-acquisition to fine-tracking handoff logic
- explaining why **candidate lock** is not the same thing as **near lock**
- keeping carrier lock separate from QPSK quadrant labeling

## The compact state machine

1. **Acquire**
   - the symmetry-collapsed view is still drifting or smearing
   - stay in blind or coarse acquisition

2. **Candidate lock**
   - the constellation is stable modulo 90°
   - stop broad searching, but do **not** trust hard decisions yet

3. **Track**
   - the modulo-90 view stays settled
   - a Costas-style residual stays small for several windows
   - now hand off to fine tracking

4. **Resolve ambiguity separately**
   - even this state can still be off by 90° in QPSK labeling

## Why one threshold is not enough

A symmetry-based stability metric can tell you that the visible spin has stopped while the residual phase is still too large for clean decision-directed feedback.

That gap is the whole point.
A receiver can be **stable enough to stop coarse searching** and still **not** be close enough to trust fine tracking or payload decisions.

## What this card is protecting against

- calling a stable modulo-90 constellation “fully locked”
- using raw `|I|-|Q|` arm balance as the main public QPSK lock test
- treating carrier lock as if it already solved the last 90° ambiguity

## What this card is not saying

- it is **not** a universal threshold table
- it is **not** a production PLL tuning guide
- it is **not** the ambiguity-resolution note

It is only a compact reminder that **settled** and **close enough for decision-directed trust** are different states.

## Accepted sources

1. **PySDR — Synchronization**  
   Accepted because it keeps timing recovery, carrier recovery, and receive-chain staging in one story.

2. **Wireless Pi — How to Detect a Carrier Lock in an SDR**  
   Accepted because it makes the acquisition/tracking switch operational instead of mystical.

3. **Wireless Pi — Non-Data-Aided Carrier Phase Estimation**  
   Accepted because it gives the right symmetry-based acquisition framing before symbol decisions are safe.

4. **Wireless Pi — Costas Loop for Carrier Phase Synchronization**  
   Accepted because it explains why decision-directed tracking belongs in the near-lock region.

5. **Learning SDR — Lesson 19**  
   Accepted only as secondary visual intuition for the rotating-constellation problem.

## Rejected source / framing

- **GNU Radio Costas Loop docs**  
  Rejected as the primary teaching source because block docs are implementation lookup, not the cleanest explanation of handoff logic.

- **MathWorks synchronization catalog page**  
  Rejected because it confirms component separation, but it is still a catalog page rather than a crisp teaching note.

- **Raw QPSK `|I|-|Q|` arm balance as the public lead metric**  
  Rejected because it does not cleanly separate spinning, candidate-lock, and ambiguity states in this QPSK teaching lane.

## Best next move

Pair this with the QPSK ambiguity card, not inside it.
If more implementation detail is needed later, keep the formulas and threshold tuning in the source SDR repo instead of bloating the public note.

— Jarbas
