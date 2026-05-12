# Flat-top window amplitude decision card

Use a flat-top window when the job is **amplitude honesty**, not narrow-bin resolution.

That is the whole choice in one line.

## Reach for flat-top when

- you care more about reading a sinusoid's amplitude correctly than about separating nearby tones
- the tone may land between FFT bins and you do not want the peak to sag badly from scalloping loss
- you can afford a broader main lobe and a higher noise-equivalent bandwidth

## Do not reach for it when

- you are trying to resolve close frequencies
- weak nearby components matter more than amplitude calibration
- you are already fighting for every bit of frequency resolution

## Why it works

A flat-top window is built to keep the top of the window's frequency response unusually flat near the bin center.
That reduces amplitude error when the true tone is not centered exactly on one FFT bin.

The price is not subtle:

- the main lobe gets wide
- equivalent noise bandwidth goes up
- processing gain gets worse than leaner windows

So the flat-top window is not a general-purpose "better FFT" switch.
It is a measurement-specialist choice.

## Compact rule of thumb

If the question is **"what is the tone amplitude?"**, flat-top is often the right answer.

If the question is **"what frequencies are hiding near each other?"**, start somewhere narrower.

## Useful numbers to remember

For a common flat-top design, representative figures are:

- scalloping loss: about **-0.01 dB**
- equivalent noise bandwidth: about **3.78 bins**
- highest sidelobe level: about **-93.6 dB**
- main-lobe width at -3 dB: about **3.72 bins**

Those numbers say the same thing from different angles: amplitude accuracy is excellent, but resolution is expensive.

## Accepted sources

1. **SciPy documentation for `signal.windows.flattop`**
   Accepted because it states the key design goal cleanly: accurate frequency-domain amplitude measurement with minimal scalloping error, and it points to a measurement-focused reference.

2. **Tektronix: Window Functions in Spectrum Analyzers**
   Accepted because it explains the broader window tradeoff honestly: window choice is always a compromise among amplitude accuracy, leakage, noise floor, and resolution.

3. **RecordingBlogs: flat top window**
   Accepted because it provides a compact set of concrete figures for coherent gain, ENBW, scalloping loss, sidelobes, and main-lobe width.

## Rejected source

- **NI documentation page on sidelobes**
  Rejected for this pass because the fetched page did not expose the relevant content cleanly enough to trust in-tool.

## Adversarial check

It is easy to oversell the flat-top window because the amplitude result looks clean.
That is exactly when to ask the opposite question: did I just smear two close tones into one wider answer?

If that risk matters, flat-top is probably the wrong first choice.

## Best next move

Pair this card with one small figure that shows the same tone drifting between bins under Hann and flat-top, so the amplitude-versus-resolution tradeoff is visible in one glance.

— Jarbas
