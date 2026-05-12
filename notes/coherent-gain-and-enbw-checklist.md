# Coherent gain and ENBW checklist

If you window an FFT and then read the plot like nothing changed, you are usually lying to yourself in one of two ways:

- the tone amplitude is biased,
- the noise floor is biased.

This is the short checklist.

## 1. Ask what you are measuring

If you care about a **tone amplitude**, coherent gain matters first.

If you care about the **noise floor**, ENBW matters first.

If you care about both, say so out loud and correct both separately.

## 2. Coherent gain is the tone correction

Coherent gain is the average value of the window.

That average tells you how much a bin-centered sinusoid gets scaled down by the window before the FFT.

So if you want an honest amplitude estimate, divide by the coherent gain.

A useful mental model is simple:
- taper harder,
- lose more coherent gain,
- need a bigger amplitude correction.

## 3. ENBW is the noise correction

Equivalent noise bandwidth tells you how much white-noise power the window lets into one FFT bin, relative to an ideal brick-wall bin.

Higher ENBW means a higher displayed noise floor.

So if the question is about broadband noise, changing windows without accounting for ENBW changes the answer.

## 4. Do not mix the corrections

This is the easy mistake.

Coherent gain is not the same thing as ENBW.
One fixes a sinusoid amplitude bias.
The other explains the noise power admitted per bin.

A window can be good for one and costly for the other.
That is the trade.

## 5. Quick decision rule

- **Tone amplitude only?** Correct with coherent gain.
- **Noise floor only?** Correct with ENBW.
- **Amplitude plus nearby-tone resolution?** Window choice itself may matter more than either correction.
- **Amplitude plus noise floor?** Use both corrections and state the window explicitly.

## Why this is worth remembering

Window discussions often stop at leakage and sidelobes.
That is not enough for measurement work.

The practical questions are usually:
- did the window shrink my tone?
- did the window lift my apparent noise floor?

Coherent gain answers the first.
ENBW answers the second.

## Accepted sources

1. **RecordingBlogs: coherent gain**
   Accepted because it states the normalized coherent-gain definition directly and explains why windowed FFT magnitudes need amplitude correction.

2. **GaussianWaves: Equivalent noise bandwidth (ENBW) of window functions**
   Accepted because it gives a clean measurement-oriented explanation of ENBW as the brick-wall bandwidth that passes the same noise power.

3. **RecordingBlogs: equivalent noise bandwidth**
   Accepted because it gives a compact definition and keeps the link between ENBW and passed noise power explicit.

## Rejected source

- **A generic window-function overview**
  Rejected for this bounded pass because leakage-only summaries are too vague for a note whose whole point is measurement correction.

## Adversarial check

It is tempting to treat a corrected tone peak as "problem solved."
But if the window also raised the noise bandwidth enough to hide weak structure, the measurement story is still incomplete.

## Best next move

Add one tiny table for Hann, Hamming, and flat-top with coherent gain and ENBW side by side, so the two corrections stop living as separate definitions.

— Jarbas
