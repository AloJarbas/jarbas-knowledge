#!/usr/bin/env python3
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "assets/2026-05-12-knowledge-map.svg"


def rect(x, y, w, h, fill, stroke="#5e7fa3", rx=18):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def text(x, y, value, cls, anchor="start"):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{value}</text>'


def main():
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1360 880">',
        '<defs>',
        '  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        '    <stop offset="0%" stop-color="#081018"/>',
        '    <stop offset="100%" stop-color="#101d2a"/>',
        '  </linearGradient>',
        '  <style>',
        '    .title { font: 700 34px Helvetica, Arial, sans-serif; fill: #e6edf3; }',
        '    .subtitle { font: 500 18px Helvetica, Arial, sans-serif; fill: #9fb3c8; }',
        '    .cluster { font: 700 22px Helvetica, Arial, sans-serif; fill: #dce7f3; }',
        '    .note { font: 600 17px Helvetica, Arial, sans-serif; fill: #e6edf3; }',
        '    .small { font: 500 14px Helvetica, Arial, sans-serif; fill: #9fb3c8; }',
        '  </style>',
        '</defs>',
        '<rect width="1360" height="880" fill="url(#bg)"/>',
        text(60, 60, 'Jarbas Knowledge map', 'title'),
        text(60, 94, 'Six notes now, with the proof workflow cluster finally deep enough to feel like a real kit.', 'subtitle'),
        rect(70, 150, 480, 470, '#132231'),
        rect(600, 150, 320, 220, '#132231'),
        rect(970, 150, 320, 220, '#132231'),
        rect(420, 680, 520, 130, '#142536'),
        text(100, 190, 'Proof workflow', 'cluster'),
        text(630, 190, 'Radio and measurement', 'cluster'),
        text(1000, 190, 'CAD and scientific tooling', 'cluster'),
        text(450, 720, 'Repo filter', 'cluster'),
        rect(95, 225, 430, 64, '#1d3043', '#6f8db0', 14),
        rect(95, 305, 430, 64, '#1d3043', '#6f8db0', 14),
        rect(95, 385, 430, 64, '#1d3043', '#6f8db0', 14),
        rect(95, 465, 430, 64, '#1d3043', '#6f8db0', 14),
        rect(625, 245, 270, 64, '#1d3043', '#6f8db0', 14),
        rect(995, 245, 270, 64, '#1d3043', '#6f8db0', 14),
        text(120, 263, 'Proof-method cue card', 'note'),
        text(120, 343, 'Proof-study loop', 'note'),
        text(120, 423, 'Weekly proof review card', 'note'),
        text(120, 503, 'Proof-journal error taxonomy', 'note'),
        text(650, 283, 'Home radio telescope target/log matrix', 'note'),
        text(1020, 283, 'Shared starter part spec', 'note'),
        text(120, 281, 'Pick the first proof move without pretending it is automatic.', 'small'),
        text(120, 361, 'Delayed retrieval, worked-example audit, interleaving.', 'small'),
        text(120, 441, 'A weekly reset that forces recall, audit, and honest load control.', 'small'),
        text(120, 521, 'Error tags plus gates for when the wider math load may grow.', 'small'),
        text(650, 301, 'Learn radio astronomy through logging discipline before hardware escalation.', 'small'),
        text(1020, 301, 'A common benchmark object across three CAD stacks.', 'small'),
        text(450, 758, 'Keep only notes that still earn a reread after a month.', 'note'),
        text(450, 786, 'Reusable method, benchmark, or decision > decorative documentation.', 'small'),
        text(60, 850, 'This is a map, not a taxonomy. The point is fast orientation and real reuse.', 'small'),
        '</svg>',
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('\n'.join(svg) + '\n')
    print(f'WROTE {OUT}')


if __name__ == '__main__':
    main()
