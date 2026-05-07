# Target-and-log matrix for a receive-first home radio telescope

Topic: `home-radio-telescope`  
Date: 2026-05-07  
Question: How should a first receive-first observing lane tie targets, software, and logs together before any approval-gated outdoor installation?

## Bottom line

The safest and most cumulative first lane is not “buy hardware, then see what happens.” It is a target-and-log progression:

1. learn event morphology from other observers' live or archived data,
2. use one logging stack consistently,
3. move from easy natural signals to harder ones,
4. treat calibration hardware and outdoor installation as later, approval-gated branches.

## Target ladder

### Lane 0 — remote literacy before ownership
- Use Radio JOVE client-mode viewing and live/archived spectrograph material to learn what solar bursts, Jovian activity, and background variation actually look and sound like.
- Goal: become able to distinguish event classes and routine interference before designing a personal receive chain.
- Durable output to keep: a one-page pattern glossary with 3-5 example captures later.

### Lane 1 — compact receive-and-log habit
- Stay with modest receive-only systems that emphasize repeatable logging.
- Radio JOVE and SARA both point beginners toward modest systems whose value comes from regular recording rather than heroic aperture.
- Goal: establish a repeatable observing session template: date/time, target, frequency range, gain settings, local conditions, interference notes, and whether anything worth review appeared.

### Lane 2 — target classes in increasing difficulty
1. **Solar activity / ionospheric disturbance class**: fastest route to seeing that the system is alive.
2. **Jupiter decametric listening**: still canonical, but more timing-dependent.
3. **Galactic background comparisons**: useful for learning baseline drift and directional effects.
4. **Hydrogen line**: explicitly later, after the logging habit and receive-chain literacy are stable.

## Minimal logging schema

For every session, record:
- UTC start and end
- target class
- receiver/software stack
- frequency span or observing mode
- gain / key settings
- antenna context (remote/client/bench/simple receive setup)
- weather or local interference note when relevant
- short verdict: noise only / candidate event / clear event
- follow-up: save clip, compare with other observers, or discard

## Software implication

The current evidence keeps the topic software-centered:
- **Radio-Sky Spectrograph** is the right tool when spectrographic viewing/storage matters.
- **Radio-SkyPipe** is the right mental model for simple time-series logging and sharing.
- The first software choice should be driven by the target class: spectrograph-style viewing for SDR-style observing; simpler strip-chart logging for narrow monitoring tasks.

## Practical recommendation for the next approved-research step

Before any hardware-specific plan, make a private template note for one observing session and one comparison session using other observers' data. If the template feels thin or confused, the topic is not yet ready for a bench-chain bill of materials.

## Source basis

- NASA Radio JOVE — Getting Started: https://radiojove.gsfc.nasa.gov/gettingstarted/
- NASA Radio JOVE — Software: https://radiojove.gsfc.nasa.gov/radio_telescope/SW.php
- SARA — Getting Started in Radio Astronomy: https://www.radio-astronomy.org/getting-started

## Safety / approval status

No practical RF transmission, outdoor antenna installation, mast work, grounding work, or calibration-hardware build is proposed here. Those remain approval-gated.
