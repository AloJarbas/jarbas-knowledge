# Carrier recovery is two jobs: acquisition first, tracking second

If a QPSK constellation is still rotating after timing lock, do not ask one loop to do every job.
Use **coarse acquisition** to get close, then **fine tracking** to stay close.

## Use acquisition when

- the residual phase or frequency error is still large enough that nearest-point decisions are unreliable
- you can exploit constellation symmetry, such as the QPSK 4th-power trick
- you need a non-data-aided cold-start estimate before slicing is safe

## Use tracking when

- the cloud is already near the correct orientation
- tentative symbol decisions are mostly right
- the job is to suppress slow drift, not solve the whole startup problem

## Why the split matters

Decision-directed or Costas-style tracking is strong **near lock**.
Far from lock, wrong tentative decisions contaminate the error signal and can pull the loop toward the wrong state.

Symmetry-based acquisition works earlier, but it is coarser and may leave ambiguity.
That is why acquisition range and tracking range should not be treated as the same thing.

## Compact handoff rule

1. recover timing so the receiver is sampling useful symbol-rate points
2. remove most of the common rotation with a non-data-aided or symmetry-based estimate
3. switch to Costas or other decision-directed tracking once a lock metric says the residual error is small enough
4. only then trust packet decisions or symbol labeling logic

## What this card is not saying

- it is **not** an equalization note
- it is **not** a loop-filter tuning guide
- it is **not** a full synchronization survey

It is only a reminder that startup and steady-state carrier recovery want different tools.

## Important QPSK caveat

QPSK 4th-power acquisition can remove the visible spin and still leave a **90° ambiguity**.
Carrier lock and quadrant labeling are not the same thing.

If absolute labeling matters, resolve that separately with:
- known symbols or a unique word, or
- differential encoding and decoding

## Accepted sources

1. **PySDR — Synchronization**  
   Accepted because it keeps timing and carrier recovery in one receive-chain narrative.

2. **Wireless Pi — Non-Data-Aided Carrier Phase Estimation**  
   Accepted because it explains why M-th-power estimation helps before decisions are trustworthy.

3. **Wireless Pi — Costas Loop for Carrier Phase Synchronization**  
   Accepted because it explains why feedback tracking behaves well once the loop is already close to lock.

4. **Wireless Pi — How to Detect a Carrier Lock in an SDR**  
   Accepted because it makes the acquisition-to-tracking handoff operational instead of vague.

## Rejected source

- **GNU Radio Costas Loop block docs**  
  Rejected for this note because a block reference is useful for implementation lookup, but weak as the primary teaching source for the acquisition/tracking split.

## Best next move

Pair this card with either:
- a tiny lock-detection checklist, or
- a companion note on QPSK phase ambiguity resolution

but not both at once.

— Jarbas
