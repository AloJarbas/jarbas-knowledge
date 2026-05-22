#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import tempfile
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SVG_OUT = REPO / 'assets/qpsk-fourth-power-alias-cliff-card.svg'
PNG_OUT = REPO / 'assets/qpsk-fourth-power-alias-cliff-card.png'

WIDTH = 1600
HEIGHT = 1600
CLIFF = 0.25


def rect(x: float, y: float, w: float, h: float, fill: str, *, stroke: str = '#334155', rx: float = 18.0, stroke_width: float = 2.0, opacity: float = 1.0) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="{rx:.1f}" fill="{fill}" opacity="{opacity}" stroke="{stroke}" stroke-width="{stroke_width:.1f}"/>'
    )


def line(x1: float, y1: float, x2: float, y2: float, stroke: str, *, width: float = 2.0, opacity: float = 1.0, dash: str | None = None) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ''
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{width:.1f}" opacity="{opacity}" stroke-linecap="round"{dash_attr}/>'
    )


def text(x: float, y: float, body: str, cls: str, *, anchor: str = 'start') -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{escape(body)}</text>'


def block(x: float, y: float, lines: list[str], cls: str, *, anchor: str = 'start', line_step: int = 20) -> str:
    tspans = []
    for idx, line_value in enumerate(lines):
        dy = 0 if idx == 0 else line_step
        tspans.append(f'<tspan x="{x:.1f}" dy="{dy}">{escape(line_value)}</tspan>')
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{"".join(tspans)}</text>'


def wrap(body: str, width: int) -> list[str]:
    words = body.split()
    if not words:
        return ['']
    lines = [words[0]]
    for word in words[1:]:
        candidate = f'{lines[-1]} {word}'
        if len(candidate) <= width:
            lines[-1] = candidate
        else:
            lines.append(word)
    return lines


def axis_x(value: float, left: float, width: float) -> float:
    return left + width * (value / 0.50)


def export_png(svg_path: Path, png_path: Path) -> bool:
    qlmanage = shutil.which('qlmanage')
    if qlmanage is None:
        return False
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(
            [qlmanage, '-t', '-s', '2200', '-o', tmpdir, str(svg_path.resolve())],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        generated = Path(tmpdir) / f'{svg_path.name}.png'
        if not generated.exists():
            raise FileNotFoundError(f'Quick Look did not generate {generated}')
        png_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(generated, png_path)
    sips = shutil.which('sips')
    if sips is not None:
        subprocess.run(
            [sips, '--setProperty', 'dpiWidth', '300', '--setProperty', 'dpiHeight', '300', str(png_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    return True


def main() -> None:
    axis_left = 120.0
    axis_top = 338.0
    axis_width = 1360.0
    axis_height = 220.0
    cliff_x = axis_x(CLIFF, axis_left, axis_width)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">',
        '<defs>',
        '  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        '    <stop offset="0%" stop-color="#08111b"/>',
        '    <stop offset="100%" stop-color="#0f1c2b"/>',
        '  </linearGradient>',
        '  <style>',
        '    .title { font: 700 36px Helvetica, Arial, sans-serif; fill: #e2e8f0; }',
        '    .subtitle { font: 500 18px Helvetica, Arial, sans-serif; fill: #b9cadb; }',
        '    .label { font: 700 20px Helvetica, Arial, sans-serif; fill: #e2e8f0; }',
        '    .body { font: 500 16px Helvetica, Arial, sans-serif; fill: #cbd5e1; }',
        '    .small { font: 500 14px Helvetica, Arial, sans-serif; fill: #cbd5e1; }',
        '    .tiny { font: 500 13px Helvetica, Arial, sans-serif; fill: #94a3b8; }',
        '  </style>',
        '</defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>',
        rect(26, 26, WIDTH - 52, HEIGHT - 52, '#0d1826', stroke='#223246', stroke_width=2.0, rx=28.0),
        text(64, 66, 'QPSK 4th-power coarse recovery has a hard alias cliff at π/4', 'title'),
        block(64, 102, [
            'For symbol-rate QPSK, treat ±π/4 as a real trust boundary for the blind 4th-power estimate.',
            'Past that cliff, a tidy-looking post-loop constellation is not strong evidence that the payload labels survived.',
        ], 'subtitle', line_step=24),
        rect(64, 154, WIDTH - 128, 486, '#122030', stroke='#324861', rx=24),
        rect(64, 678, 470, 360, '#122030', stroke='#324861', rx=22),
        rect(564, 678, 470, 360, '#122030', stroke='#324861', rx=22),
        rect(1064, 678, 472, 360, '#122030', stroke='#324861', rx=22),
        rect(64, 1072, 718, 422, '#122030', stroke='#324861', rx=22),
        rect(818, 1072, 718, 422, '#122030', stroke='#324861', rx=22),
    ]

    svg.extend([
        text(90, 194, 'Trust boundary', 'label'),
        block(90, 226, wrap('The only hard number on this card is the alias boundary itself. Everything else below π/4 still depends on loop quality, handoff logic, and what the receiver already knows.', 92), 'body', line_step=22),
        rect(axis_left, axis_top, axis_width, axis_height, '#0f1724', stroke='#334155', rx=24),
        rect(axis_left + 30, axis_top + 82, cliff_x - axis_left - 30, 64, '#14532d', stroke='#14532d', stroke_width=0.0, rx=18),
        rect(cliff_x, axis_top + 82, axis_left + axis_width - cliff_x - 30, 64, '#7f1d1d', stroke='#7f1d1d', stroke_width=0.0, rx=18),
        text(axis_left + 50, axis_top + 122, 'honest 4th-power coarse range', 'label'),
        text(cliff_x + 28, axis_top + 122, 'wrapped-estimate alias risk', 'label'),
        line(axis_left + 30, axis_top + 170, axis_left + axis_width - 30, axis_top + 170, '#64748b', width=3.0),
        line(cliff_x, axis_top + 60, cliff_x, axis_top + 190, '#facc15', width=4.0),
        text(cliff_x, axis_top + 42, 'alias cliff  |Δf| / Rₛ = 0.25', 'label', anchor='middle'),
    ])

    for tick_value in [0.00, 0.10, 0.20, 0.25, 0.30, 0.40, 0.50]:
        x = axis_x(tick_value, axis_left + 30, axis_width - 60)
        svg.append(line(x, axis_top + 162, x, axis_top + 178, '#94a3b8', width=2.0))
        svg.append(text(x, axis_top + 204, f'{tick_value:.2f}', 'small', anchor='middle'))

    svg.append(text(axis_left + axis_width / 2.0, axis_top + 248, 'residual carrier offset magnitude  |Δf| / Rₛ', 'body', anchor='middle'))
    svg.append(text(90, axis_top + 286, 'If you are already near lock, the loop may not need blind coarse help at all.', 'small'))
    svg.append(text(90, axis_top + 312, 'If you still need coarse help but stay inside the green lane, 4th-power acquisition can widen handoff honestly.', 'small'))
    svg.append(text(90, axis_top + 338, 'The red lane is the warning: beyond π/4, a clean cloud can still carry the wrong labels.', 'small'))

    cards = [
        (
            64,
            'Loop-alone region',
            '#0f766e',
            [
                'Residual is already near enough to center that fine tracking may finish the job.',
                'This cutoff is receiver-specific. Do not fake a universal number here.',
            ],
        ),
        (
            564,
            'Coarse-help region',
            '#1d4ed8',
            [
                'Inside the honest 4th-power range, blind coarse correction can pull the residual back toward the near-lock lane.',
                'This is where symbol-rate QPSK symmetry actually buys something useful.',
            ],
        ),
        (
            1064,
            'Alias region',
            '#dc2626',
            [
                'Past π/4, the same estimator can wrap very abruptly to the wrong answer.',
                'The failure mode can look clean instead of noisy. That is why this card exists.',
            ],
        ),
    ]
    for left, title_text, tone, bullets in cards:
        svg.append(text(left + 24, 714, title_text, 'label'))
        svg.append(line(left + 24, 730, left + 160, 730, tone, width=4.0))
        for idx, bullet in enumerate(bullets):
            svg.append(block(left + 24, 770 + idx * 84, wrap(f'• {bullet}', 44), 'body', line_step=22))

    svg.append(text(90, 1108, 'Do not trust as proof', 'label'))
    for idx, bullet in enumerate([
        'A tidy-looking post-loop constellation by itself.',
        'Nearest-point geometry or RMS alone.',
        'The vague feeling that the loop “looks locked.”',
    ]):
        svg.append(block(90, 1150 + idx * 88, wrap(f'• {bullet}', 48), 'body', line_step=22))
    svg.append(text(844, 1108, 'Better evidence', 'label'))
    for idx, bullet in enumerate([
        'The coarse estimate stays inside the hard blind range.',
        'Handoff logic and lock evidence agree with the coarse estimate.',
        'Decoded labels still make sense after ambiguity handling, not just after plotting.',
    ]):
        svg.append(block(844, 1150 + idx * 88, wrap(f'• {bullet}', 48), 'body', line_step=22))

    svg.append(text(64, 1528, 'Source basis: Wireless Pi on M-th-power range limits + Costas near-lock scope, PySDR synchronization framing, and local evidence from costas-loop-lab.', 'small'))
    svg.append(text(64, 1552, 'This is a warning card about blind coarse acquisition scope, not a full loop-tuning guide or a phase-ambiguity tutorial.', 'small'))
    svg.append('</svg>')

    SVG_OUT.parent.mkdir(parents=True, exist_ok=True)
    SVG_OUT.write_text('\n'.join(svg) + '\n')
    exported = export_png(SVG_OUT, PNG_OUT)
    if exported:
        print(f'WROTE {SVG_OUT} and {PNG_OUT}')
    else:
        print(f'WROTE {SVG_OUT}')


if __name__ == '__main__':
    main()
