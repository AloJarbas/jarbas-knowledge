#!/usr/bin/env python3
from __future__ import annotations

from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SVG_OUT = REPO / "assets/home-radio-telescope-target-log-matrix.svg"

WIDTH = 1560
HEIGHT = 1140

ROWS = [
    {
        "lane": "Lane 0",
        "stage": "Remote literacy before ownership",
        "target": "Live or archived solar / Jovian examples",
        "learn": "Event morphology and routine interference discrimination before hardware shopping",
        "software": "Radio JOVE client mode, archived spectrograms, other observers' captures",
        "keep": "3-5 labeled examples and one short pattern glossary",
        "tone": "#1d4ed8",
    },
    {
        "lane": "Lane 1",
        "stage": "Compact receive-and-log habit",
        "target": "Modest receive-only sessions",
        "learn": "Repeatable session logging beats heroic aperture on day one",
        "software": "Use one stack consistently: spectrograph if shape matters, strip-chart if narrow monitoring matters",
        "keep": "One session template with UTC, target, span, gain, conditions, verdict",
        "tone": "#0f766e",
    },
    {
        "lane": "Lane 2A",
        "stage": "Solar activity / ionospheric disturbance",
        "target": "The easiest " + "alive-check" + " target class",
        "learn": "Can the system show obvious bursts and changing background without fooling you?",
        "software": "Radio-Sky Spectrograph when the shape matters most",
        "keep": "Save one clear event and one false alarm with notes",
        "tone": "#ca8a04",
    },
    {
        "lane": "Lane 2B",
        "stage": "Jupiter decametric listening",
        "target": "Timing-dependent canonical target",
        "learn": "Scheduling discipline and cross-checking candidate events against other observers",
        "software": "Same receive/log stack, but with stricter timing and comparison habits",
        "keep": "Candidate clip plus comparison verdict against other observers' data",
        "tone": "#9333ea",
    },
    {
        "lane": "Lane 2C",
        "stage": "Galactic background comparisons",
        "target": "Baseline drift and directional changes",
        "learn": "How much of the curve is the sky, and how much is local baseline behavior?",
        "software": "Simple logging is fine if the session record stays disciplined",
        "keep": "Paired comparisons with local conditions and antenna context recorded",
        "tone": "#dc2626",
    },
    {
        "lane": "Lane 3",
        "stage": "Hydrogen line later",
        "target": "Only after the receive/log habit is already stable",
        "learn": "Calibration discipline and slower interpretation without skipping the logging lane",
        "software": "Treat this as a later branch, not the first proof of life",
        "keep": "Approval-gated branch after the earlier lanes are boringly reproducible",
        "tone": "#475569",
    },
]

SESSION_FIELDS = [
    "UTC start / end",
    "target class",
    "receiver + software stack",
    "frequency span or observing mode",
    "gain / key settings",
    "antenna context",
    "weather or local interference note",
    "verdict: noise only / candidate / clear event",
    "follow-up: save, compare, or discard",
]

BOUNDARY_LINES = [
    "Not in scope here:",
    "transmission, mast work, outdoor installation,",
    "grounding work, or calibration hardware build.",
    "Those stay later and approval-gated.",
]


def rect(x: float, y: float, w: float, h: float, fill: str, *, stroke: str = "#334155", rx: float = 18.0, stroke_width: float = 2.0) -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.1f}"/>'


def text(x: float, y: float, body: str, cls: str, *, anchor: str = "start") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{escape(body)}</text>'


def block(x: float, y: float, lines: list[str], cls: str, *, anchor: str = "start", line_step: int = 20) -> str:
    tspans = []
    for idx, line in enumerate(lines):
        dy = 0 if idx == 0 else line_step
        tspans.append(f'<tspan x="{x:.1f}" dy="{dy}">{escape(line)}</tspan>')
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{"".join(tspans)}</text>'


def wrap(text_value: str, width: int) -> list[str]:
    words = text_value.split()
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if len(candidate) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def main() -> None:
    row_h = 112
    table_x = 56
    table_y = 188
    lane_w = 110
    stage_w = 250
    target_w = 214
    learn_w = 292
    software_w = 322
    keep_w = 240

    col_x = [
        table_x,
        table_x + lane_w,
        table_x + lane_w + stage_w,
        table_x + lane_w + stage_w + target_w,
        table_x + lane_w + stage_w + target_w + learn_w,
        table_x + lane_w + stage_w + target_w + learn_w + software_w,
    ]

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">',
        '<defs>',
        '  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        '    <stop offset="0%" stop-color="#08111b"/>',
        '    <stop offset="100%" stop-color="#0f1c2b"/>',
        '  </linearGradient>',
        '  <style>',
        '    .title { font: 700 34px Helvetica, Arial, sans-serif; fill: #e2e8f0; }',
        '    .subtitle { font: 500 17px Helvetica, Arial, sans-serif; fill: #a8bdd2; }',
        '    .header { font: 700 14px Helvetica, Arial, sans-serif; fill: #dbe7f4; }',
        '    .lane { font: 700 16px Helvetica, Arial, sans-serif; fill: #f8fafc; }',
        '    .stage { font: 700 15px Helvetica, Arial, sans-serif; fill: #eff6ff; }',
        '    .cell { font: 500 13px Helvetica, Arial, sans-serif; fill: #cbd5e1; }',
        '    .side-title { font: 700 20px Helvetica, Arial, sans-serif; fill: #e2e8f0; }',
        '    .side-body { font: 500 13px Helvetica, Arial, sans-serif; fill: #cbd5e1; }',
        '    .small { font: 500 12px Helvetica, Arial, sans-serif; fill: #94a3b8; }',
        '  </style>',
        '</defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>',
        text(56, 58, 'Receive-first home radio telescope target-and-log matrix', 'title'),
        block(56, 88, [
            'Learn event morphology, keep one logging stack steady, and climb from easy natural signals to harder ones.',
            'Treat installation, calibration hardware, and outdoor escalation as later approval-gated branches, not the day-one plan.',
        ], 'subtitle', line_step=22),
        rect(56, 128, 1148, 840, '#122030', stroke='#324861', rx=22),
        rect(1232, 128, 272, 362, '#122030', stroke='#324861', rx=22),
        rect(1232, 520, 272, 196, '#122030', stroke='#324861', rx=22),
        rect(1232, 744, 272, 184, '#122030', stroke='#324861', rx=22),
    ]

    headers = [
        ('Lane', lane_w),
        ('Stage', stage_w),
        ('Target class', target_w),
        ('What you are really learning', learn_w),
        ('Software / observing mode', software_w),
        ('Durable output to keep', keep_w),
    ]

    x = table_x
    for label, width in headers:
        svg.append(rect(x, table_y, width, 48, '#18283b', stroke='#415a74', rx=12))
        svg.append(text(x + 14, table_y + 30, label, 'header'))
        x += width

    for idx, row in enumerate(ROWS):
        y = table_y + 60 + idx * (row_h + 8)
        svg.append(rect(table_x, y, 1148, row_h, '#101b29', stroke='#27374b', rx=16))
        svg.append(rect(table_x + 10, y + 12, 90, row_h - 24, row['tone'], stroke=row['tone'], rx=12, stroke_width=0))
        svg.append(block(table_x + 24, y + 46, wrap(row['lane'], 10), 'lane', line_step=18))
        svg.append(block(col_x[1] + 14, y + 28, wrap(row['stage'], 22), 'stage', line_step=18))
        svg.append(block(col_x[2] + 14, y + 28, wrap(row['target'], 22), 'cell', line_step=18))
        svg.append(block(col_x[3] + 14, y + 28, wrap(row['learn'], 34), 'cell', line_step=18))
        svg.append(block(col_x[4] + 14, y + 28, wrap(row['software'], 34), 'cell', line_step=18))
        svg.append(block(col_x[5] + 14, y + 28, wrap(row['keep'], 24), 'cell', line_step=18))

    svg.append(text(1248, 160, 'Minimal session log', 'side-title'))
    for idx, field in enumerate(SESSION_FIELDS):
        y = 190 + idx * 28
        svg.append(rect(1248, y - 14, 18, 18, '#0f766e', stroke='#0f766e', rx=5, stroke_width=0))
        svg.append(text(1278, y, field, 'side-body'))

    svg.append(text(1248, 552, 'Software implication', 'side-title'))
    svg.append(block(1248, 580, [
        'Spectrograph-style viewing when event shape matters.',
        'Strip-chart logging when the job is narrow monitoring over time.',
        'Pick the mode by target class, not by gadget lust.',
    ], 'side-body', line_step=20))

    svg.append(text(1248, 776, 'Approval boundary', 'side-title'))
    svg.append(block(1248, 806, BOUNDARY_LINES, 'side-body', line_step=20))
    svg.append(text(56, 1088, 'Source basis: NASA Radio JOVE getting-started + software pages, plus SARA getting-started guidance.', 'small'))
    svg.append(text(56, 1112, 'This is a target ladder and logging matrix, not a hardware bill of materials.', 'small'))
    svg.append('</svg>')

    SVG_OUT.parent.mkdir(parents=True, exist_ok=True)
    SVG_OUT.write_text('\n'.join(svg) + '\n')
    print(f'WROTE {SVG_OUT}')


if __name__ == '__main__':
    main()
