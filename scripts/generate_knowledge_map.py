#!/usr/bin/env python3
from __future__ import annotations

from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "assets/2026-05-12-knowledge-map.svg"

WIDTH = 1360
HEIGHT = 920


def rect(x, y, w, h, fill, stroke="#5e7fa3", rx=18):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def text_block(x: float, y: float, lines: list[str], cls: str, anchor: str = "start", line_step: int = 22) -> str:
    tspans = []
    for idx, line in enumerate(lines):
        dy = 0 if idx == 0 else line_step
        tspans.append(f'<tspan x="{x}" dy="{dy}">{escape(line)}</tspan>')
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{"".join(tspans)}</text>'


def card(x: float, y: float, w: float, h: float, title_lines: list[str], body_lines: list[str]) -> list[str]:
    parts = [rect(x, y, w, h, "#1d3043", "#6f8db0", 14)]
    parts.append(text_block(x + 24, y + 30, title_lines, "note", line_step=19))
    parts.append(text_block(x + 24, y + 58 + max(0, len(title_lines) - 1) * 18, body_lines, "small", line_step=18))
    return parts


def main():
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<defs>',
        '  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        '    <stop offset="0%" stop-color="#081018"/>',
        '    <stop offset="100%" stop-color="#101d2a"/>',
        '  </linearGradient>',
        '  <style>',
        '    .title { font: 700 34px Helvetica, Arial, sans-serif; fill: #e6edf3; }',
        '    .subtitle { font: 500 18px Helvetica, Arial, sans-serif; fill: #9fb3c8; }',
        '    .cluster { font: 700 22px Helvetica, Arial, sans-serif; fill: #dce7f3; }',
        '    .note { font: 600 16px Helvetica, Arial, sans-serif; fill: #e6edf3; }',
        '    .small { font: 500 13px Helvetica, Arial, sans-serif; fill: #9fb3c8; }',
        '  </style>',
        '</defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>',
        text_block(60, 60, ['Jarbas knowledge map'], 'title'),
        text_block(60, 94, ['Six notes now, with the proof workflow cluster finally deep enough', 'to feel like a real kit.'], 'subtitle', line_step=22),
        rect(70, 156, 500, 500, '#132231'),
        rect(610, 156, 320, 250, '#132231'),
        rect(970, 156, 320, 250, '#132231'),
        rect(400, 706, 560, 138, '#142536'),
        text_block(100, 196, ['Proof workflow'], 'cluster'),
        text_block(640, 196, ['Radio and measurement'], 'cluster'),
        text_block(1000, 196, ['CAD and scientific tooling'], 'cluster'),
        text_block(430, 746, ['Repo filter'], 'cluster'),
    ]

    svg.extend(card(95, 230, 450, 78, ['Proof-method cue card'], ['Pick the first proof move without pretending it is automatic.']))
    svg.extend(card(95, 324, 450, 78, ['Proof-study loop'], ['Delayed retrieval, worked-example audit, interleaving.']))
    svg.extend(card(95, 418, 450, 78, ['Weekly proof review card'], ['A weekly reset that forces recall, audit, and honest load control.']))
    svg.extend(card(95, 512, 450, 96, ['Proof-journal error taxonomy'], ['Error tags plus gates for when the wider', 'math load may grow.']))

    svg.extend(card(635, 248, 270, 108, ['Home radio telescope', 'target/log matrix'], ['Learn radio astronomy through logging discipline', 'before hardware escalation.']))
    svg.extend(card(995, 248, 270, 108, ['Shared starter part spec'], ['A common benchmark object across three', 'CAD stacks.']))

    svg.append(text_block(430, 784, ['Keep only notes that still earn a reread after a month.'], 'note'))
    svg.append(text_block(430, 812, ['Reusable method, benchmark, or decision beats', 'decorative documentation.'], 'small', line_step=18))
    svg.append(text_block(60, 884, ['This is a map, not a taxonomy. The point is fast orientation and real reuse.'], 'small'))
    svg.append('</svg>')

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('\n'.join(svg) + '\n')
    print(f'WROTE {OUT}')


if __name__ == '__main__':
    main()
