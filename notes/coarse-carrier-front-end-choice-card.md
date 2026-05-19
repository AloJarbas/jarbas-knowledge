# Choose the coarse-carrier front end by what the receiver knows

When carrier offset is too large for late-stage symbol-rate tracking, do **not** ask one block to solve every regime.
Pick the coarse front end by what information the receiver can actually trust.

## 1. If you already have a trustworthy symbol-rate PSK view

Use a symmetry-based coarse estimate first, then fine tracking.

For QPSK, the 4th-power trick is the clean example:
- it removes the data modulation by exploiting rotational symmetry
- it gives a blind coarse estimate before decisions are safe
- but its honest range is tied to the sample rate seen by the estimator

So if you only look at **1 sample/symbol**, you should expect a narrower honest frequency window than if you run the same idea earlier at several samples per symbol.

## 2. If the useful clue still lives in the oversampled waveform

Use a waveform-domain front end.

A band-edge FLL is the clean example when:
- the signal is pulse-shaped with nonzero excess bandwidth
- the receiver still has an oversampled view
- and frequency error shows up as left/right imbalance across the spectral roll-off edges

This is a different contract from M-th-power estimation.
It uses **pulse-shape asymmetry**, not constellation symmetry.

## 3. If the packet gives you known structure

Use it.

If there is a preamble, pilot field, or other known correlation target, that often becomes the best coarse-acquisition lane.
That is not just an implementation detail.
It is a different information source, and often a better one.

Known-structure estimators usually beat blind methods when the system can afford them, because they are not forced to recover everything from symmetry or spectral shape alone.

## The compact split

| receiver knows | best first coarse lane | why |
|---|---|---|
| PSK symmetry, but no pilots | oversampled M-th-power / symmetry-based estimate | preserves blind acquisition and scales with observation rate |
| pulse shape + excess bandwidth in an oversampled waveform | band-edge FLL / waveform-domain frequency recovery | uses spectral imbalance before symbol decisions are reliable |
| preamble or pilots | correlation / known-sequence coarse estimation | spends known structure for a cleaner startup estimate |

## What this card is protecting against

- pretending the symbol-rate Costas story has unlimited capture range
- pretending every large-CFO problem wants the same front end
- mixing up **blind**, **waveform-domain**, and **known-structure** acquisition as if they were interchangeable

## Accepted sources

1. **Wireless Pi — Non-Data-Aided Carrier Phase Estimation**  
   Accepted because it is the clearest compact explanation of M-th-power symmetry removal.

2. **GNU Radio Wiki — FLL Band-Edge**  
   Accepted because it states the waveform-domain assumptions plainly: oversampling, excess bandwidth, and band-edge power imbalance.

3. **MathWorks — QPSK Transmitter and Receiver**  
   Accepted because it shows a practical receiver split between coarse frequency compensation, timing recovery, and fine carrier tracking.

4. **MathWorks — Coarse Frequency Compensator**  
   Accepted because it keeps FFT-based and correlation-based coarse estimation distinct.

5. **Wireless Pi — How to Estimate the Carrier Phase**  
   Accepted as the reminder that known symbols change the estimation contract.

## Rejected sources

- **Generic Costas-loop docs**  
  Rejected because this card is about what belongs **before** near-lock tracking.

- **OFDM CFO tutorials**  
  Rejected because they solve a different synchronization structure.

- **Broad QPSK walkthrough tutorials**  
  Rejected because they are useful for implementation context, but too diffuse for this decision card.

## Best next move

If you turn this into a visual note, show:
- one pipeline fork, and
- one assumption table

not a giant synchronization taxonomy.

— Jarbas
