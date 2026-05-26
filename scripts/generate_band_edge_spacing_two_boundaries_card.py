#!/usr/bin/env python3
from __future__ import annotations

import csv
import shutil
import subprocess
import tempfile
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SOURCE_CSV = REPO.parent / 'jarbas-sdr-visual-notes' / 'assets' / '2026-05-24-band-edge-spacing-boundary.csv'
CSV_OUT = REPO / 'assets' / 'band-edge-spacing-two-boundaries-card.csv'
SVG_OUT = REPO / 'assets' / 'band-edge-spacing-two-boundaries-card.svg'
PNG_OUT = REPO / 'assets' / 'band-edge-spacing-two-boundaries-card.png'

WIDTH = 1700
HEIGHT = 1420
SETTLE_THRESHOLD = 0.05
SERIES = [
    ('proxy_bandpass', 'current proxy', '#60a5fa'),
    ('gnuradio_half_sine', 'GNU Radio / half-sine', '#f97316'),
]
HIGHLIGHT_SPACINGS = [1.00, 1.24, 1.57]


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


def polyline(points: list[tuple[float, float]], stroke: str, *, width: float = 5.0, opacity: float = 1.0) -> str:
    encoded = ' '.join(f'{x:.1f},{y:.1f}' for x, y in points)
    return (
        f'<polyline fill="none" stroke="{stroke}" stroke-width="{width:.1f}" '
        f'opacity="{opacity}" stroke-linecap="round" stroke-linejoin="round" points="{encoded}"/>'
    )


def circle(x: float, y: float, r: float, fill: str, *, stroke: str = '#e2e8f0', stroke_width: float = 2.0) -> str:
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.1f}"/>'


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


def export_png(svg_path: Path, png_path: Path) -> bool:
    brave_candidates = [
        Path('/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'),
        Path(shutil.which('brave-browser') or ''),
    ]
    browser = next((candidate for candidate in brave_candidates if candidate and candidate.exists()), None)
    if browser is not None:
        command = [
            str(browser),
            '--headless',
            '--disable-gpu',
            '--hide-scrollbars',
            '--run-all-compositor-stages-before-draw',
            '--virtual-time-budget=1000',
            f'--screenshot={png_path.resolve()}',
            f'--window-size={WIDTH},{HEIGHT}',
            svg_path.resolve().as_uri(),
        ]
        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        except subprocess.TimeoutExpired:
            if not png_path.exists():
                raise
        sips = shutil.which('sips')
        if sips is not None:
            subprocess.run([sips, '--setProperty', 'dpiWidth', '300', '--setProperty', 'dpiHeight', '300', str(png_path)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    qlmanage = shutil.which('qlmanage')
    if qlmanage is None:
        return False
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run([qlmanage, '-t', '-s', '2200', '-o', tmpdir, str(svg_path.resolve())], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        generated = Path(tmpdir) / f'{svg_path.name}.png'
        if not generated.exists():
            raise FileNotFoundError(f'Quick Look did not generate {generated}')
        png_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(generated, png_path)
    sips = shutil.which('sips')
    if sips is not None:
        subprocess.run([sips, '--setProperty', 'dpiWidth', '300', '--setProperty', 'dpiHeight', '300', str(png_path)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return True


def load_rows() -> dict[str, dict[float, dict[str, float]]]:
    by_design: dict[str, dict[float, dict[str, float]]] = {name: {} for name, _, _ in SERIES}
    with SOURCE_CSV.open() as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if row['adjacent_enabled'] != 'True' or float(row['adjacent_relative_power_db']) != 0.0:
                continue
            design = row['design']
            spacing = float(row['channel_spacing'])
            by_design[design][spacing] = {
                'mean_tail_residual_cfo': float(row['tail_mean_abs_residual_cfo']),
                'within_threshold_fraction': float(row['tail_within_threshold_fraction']),
            }
    return by_design


def write_public_csv(by_design: dict[str, dict[float, dict[str, float]]]) -> None:
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    spacings = sorted(by_design['proxy_bandpass'])
    with CSV_OUT.open('w', newline='') as handle:
        writer = csv.writer(handle, lineterminator='\n')
        writer.writerow([
            'channel_spacing',
            'proxy_mean_tail_residual_cfo',
            'proxy_tail_within_threshold_fraction',
            'half_sine_mean_tail_residual_cfo',
            'half_sine_tail_within_threshold_fraction',
        ])
        for spacing in spacings:
            proxy = by_design['proxy_bandpass'][spacing]
            half_sine = by_design['gnuradio_half_sine'][spacing]
            writer.writerow([
                f'{spacing:.2f}',
                f"{proxy['mean_tail_residual_cfo']:.6f}",
                f"{proxy['within_threshold_fraction']:.6f}",
                f"{half_sine['mean_tail_residual_cfo']:.6f}",
                f"{half_sine['within_threshold_fraction']:.6f}",
            ])


def main() -> None:
    by_design = load_rows()
    write_public_csv(by_design)
    spacings = sorted(by_design['proxy_bandpass'])

    settle_boundary = next(
        spacing
        for spacing in spacings
        if by_design['gnuradio_half_sine'][spacing]['within_threshold_fraction'] >= 1.0
    )
    crossover = next(
        spacing
        for spacing in spacings
        if by_design['gnuradio_half_sine'][spacing]['mean_tail_residual_cfo'] <= by_design['proxy_bandpass'][spacing]['mean_tail_residual_cfo']
    )

    top_left = 92.0
    chart_top = 318.0
    chart_width = 1030.0
    residual_height = 470.0
    settle_top = 854.0
    settle_height = 214.0
    summary_x = 1160.0
    x_min = min(spacings)
    x_max = max(spacings)
    residual_max = 0.12

    def x_map(value: float) -> float:
        return top_left + (value - x_min) / (x_max - x_min) * chart_width

    def residual_y(value: float) -> float:
        return chart_top + residual_height - value / residual_max * residual_height

    def settle_y(value: float) -> float:
        return settle_top + settle_height - value * settle_height

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">',
        '<defs>',
        '  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        '    <stop offset="0%" stop-color="#08111b"/>',
        '    <stop offset="100%" stop-color="#0f1c2b"/>',
        '  </linearGradient>',
        '  <style>',
        '    .title { font: 700 38px Helvetica, Arial, sans-serif; fill: #e2e8f0; }',
        '    .subtitle { font: 500 19px Helvetica, Arial, sans-serif; fill: #b9cadb; }',
        '    .label { font: 700 20px Helvetica, Arial, sans-serif; fill: #e2e8f0; }',
        '    .body { font: 500 16px Helvetica, Arial, sans-serif; fill: #cbd5e1; }',
        '    .small { font: 500 14px Helvetica, Arial, sans-serif; fill: #cbd5e1; }',
        '    .tiny { font: 500 13px Helvetica, Arial, sans-serif; fill: #94a3b8; }',
        '  </style>',
        '</defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>',
        rect(26, 26, WIDTH - 52, HEIGHT - 52, '#0d1826', stroke='#223246', stroke_width=2.0, rx=28.0),
        text(64, 68, 'Band-edge spacing has two boundaries:', 'title'),
        text(64, 108, 'settle first, ranking later', 'title'),
        block(64, 144, [
            'At 0 dB adjacent power, the GNU Radio / half-sine lane becomes track-ready again near 1.24 R_s,',
            'but it does not beat the proxy on mean tail residual until about 1.57 R_s.',
        ], 'subtitle', line_step=24),
        rect(64, 188, 1086, 920, '#122030', stroke='#324861', rx=24),
        rect(1178, 188, 458, 920, '#122030', stroke='#324861', rx=24),
        rect(64, 1134, 1572, 250, '#122030', stroke='#324861', rx=22),
        text(92, 228, 'Residual ranking versus spacing', 'label'),
        block(92, 258, wrap('Same bounded loop as the adjacent-loop card: one desired QPSK channel, one equal-power neighbor, 4 samples/symbol, 63 taps, alpha = 0.35, loop gain 0.02, and spacing swept from 0.80 R_s to 1.65 R_s.', 108), 'body', line_step=22),
        rect(top_left, chart_top, chart_width, residual_height, '#0f1724', stroke='#334155', rx=24),
        text(92, 826, 'Half-sine settle fraction', 'label'),
        block(92, 856, wrap('The first full-settle point lands earlier than the residual crossover. Proxy stays at 100% across this sweep; the half-sine lane is the moving one.', 96), 'body', line_step=22),
        rect(top_left, settle_top, chart_width, settle_height, '#0f1724', stroke='#334155', rx=24),
    ]

    for y_tick in [0.00, 0.03, 0.06, 0.09, 0.12]:
        y = residual_y(y_tick)
        svg.append(line(top_left + 18, y, top_left + chart_width - 18, y, '#334155', width=1.4, opacity=0.8, dash='8 8' if y_tick == SETTLE_THRESHOLD else None))
        svg.append(text(top_left - 16, y + 5, f'{y_tick:.2f}', 'small', anchor='end'))
    svg.append(text(top_left + 12, chart_top + 30, 'mean tail residual CFO', 'small'))

    for y_tick in [0.0, 0.5, 1.0]:
        y = settle_y(y_tick)
        svg.append(line(top_left + 18, y, top_left + chart_width - 18, y, '#334155', width=1.4, opacity=0.8, dash='8 8' if y_tick in {0.0, 1.0} else None))
        svg.append(text(top_left - 16, y + 5, f'{y_tick:.1f}', 'small', anchor='end'))
    svg.append(text(top_left + 12, settle_top + 30, 'tail fraction inside ±0.05 R_s', 'small'))

    x_ticks = [0.80, 1.00, 1.20, 1.24, 1.40, 1.57, 1.65]
    for x_tick in x_ticks:
        x = x_map(x_tick)
        svg.append(line(x, chart_top + 18, x, settle_top + settle_height - 18, '#233246', width=1.2, opacity=0.7, dash='4 10' if x_tick in {settle_boundary, crossover} else None))
        svg.append(text(x, settle_top + settle_height + 32, f'{x_tick:.2f}', 'small', anchor='middle'))
    svg.append(text(top_left + chart_width / 2.0, settle_top + settle_height + 64, 'channel spacing  /  R_s', 'body', anchor='middle'))

    for design, label_text, color in SERIES:
        residual_points = [(x_map(spacing), residual_y(by_design[design][spacing]['mean_tail_residual_cfo'])) for spacing in spacings]
        settle_points = [(x_map(spacing), settle_y(by_design[design][spacing]['within_threshold_fraction'])) for spacing in spacings]
        svg.append(polyline(residual_points, color, width=5.0))
        svg.append(polyline(settle_points, color, width=5.0, opacity=0.95))
        legend_x = 774 if design == 'proxy_bandpass' else 936
        legend_y = 286.0
        svg.append(line(legend_x, legend_y, legend_x + 44, legend_y, color, width=6.0))
        svg.append(text(legend_x + 56, legend_y + 5, label_text, 'small'))

    for spacing in HIGHLIGHT_SPACINGS:
        for design, _, color in SERIES:
            svg.append(circle(x_map(spacing), residual_y(by_design[design][spacing]['mean_tail_residual_cfo']), 7.5, color))
        svg.append(circle(x_map(spacing), settle_y(by_design['gnuradio_half_sine'][spacing]['within_threshold_fraction']), 7.5, '#f97316'))

    for x_value, label_text, label_y in [
        (settle_boundary, '1.24 R_s\nfirst full settle', chart_top + 112),
        (crossover, '1.57 R_s\nresidual crossover', chart_top + 352),
    ]:
        x = x_map(x_value)
        svg.append(line(x, chart_top + 18, x, settle_top + settle_height - 18, '#f8fafc', width=2.2, opacity=0.9, dash='10 8'))
        svg.append(rect(x - 74, label_y - 40, 148, 58, '#17283b', stroke='#94a3b8', rx=14, stroke_width=1.6))
        lines = label_text.split('\n')
        svg.append(block(x, label_y - 12, lines, 'small', anchor='middle', line_step=18))

    svg.extend([
        text(summary_x + 28, 228, 'Portable readout', 'label'),
        block(summary_x + 28, 258, wrap('This is not one spacing boundary. It is two different questions with two different answers.', 38), 'body', line_step=22),
    ])

    summary_rows = [
        ('1.00 R_s', 'proxy 0.0387 / 100%', 'half-sine 0.0995 / 0%'),
        ('1.24 R_s', 'proxy 0.0028 / 100%', 'half-sine 0.0447 / 100%'),
        ('1.57 R_s', 'proxy 0.00020 / 100%', 'half-sine 0.00017 / 100%'),
    ]
    box_y = 330.0
    for label_text, proxy_text, half_text in summary_rows:
        svg.append(rect(summary_x + 24, box_y, 410, 136, '#0f1724', stroke='#334155', rx=18))
        svg.append(text(summary_x + 44, box_y + 34, label_text, 'label'))
        svg.append(text(summary_x + 44, box_y + 68, proxy_text, 'body'))
        svg.append(text(summary_x + 44, box_y + 98, half_text, 'body'))
        box_y += 154

    svg.extend([
        text(summary_x + 28, 816, 'Why keep this note', 'label'),
        block(summary_x + 28, 846, wrap('It protects against the sloppy sentence that spacing "fixes" the half-sine lane at one magic point. The settle band recovers around 1.24 R_s, but the stricter mean-residual ranking only flips much later.', 41), 'body', line_step=22),
        text(summary_x + 28, 980, 'Decision rule', 'label'),
        block(summary_x + 28, 1010, wrap('If you only need the half-sine lane to stop failing the settle band, 1.24 R_s is enough in this setup. If you care about which loop is actually cleaner, the honest boundary is closer to 1.57 R_s.', 41), 'body', line_step=22),
        text(92, 1170, 'What this card protects against', 'label'),
        block(92, 1200, wrap('Do not collapse "track-ready again" and "residual ranking flipped" into one sentence. One nearby-channel loop can have an early settle boundary and a later quality boundary.', 118), 'body', line_step=22),
        text(92, 1300, 'Source basis', 'label'),
        block(92, 1330, wrap('External framing comes from Daniel Estévez plus the GNU Radio FLL Band-Edge wiki and source. The public values here are a direct extraction from jarbas-sdr-visual-notes/notes/band-edge-spacing-boundary.md and its dated 2026-05-24 research memo.', 118), 'tiny', line_step=20),
    ])

    svg.append('</svg>')

    SVG_OUT.parent.mkdir(parents=True, exist_ok=True)
    SVG_OUT.write_text('\n'.join(svg))
    export_png(SVG_OUT, PNG_OUT)


if __name__ == '__main__':
    main()
