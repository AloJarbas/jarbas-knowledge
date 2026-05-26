#!/usr/bin/env python3
from __future__ import annotations

import csv
import shutil
import subprocess
import tempfile
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SOURCE_CSV = REPO.parent / 'jarbas-sdr-visual-notes' / 'assets' / '2026-05-24-band-edge-loop-gain-retuning.csv'
CSV_OUT = REPO / 'assets' / 'band-edge-loop-gain-retuning-card.csv'
SVG_OUT = REPO / 'assets' / 'band-edge-loop-gain-retuning-card.svg'
PNG_OUT = REPO / 'assets' / 'band-edge-loop-gain-retuning-card.png'

WIDTH = 1700
HEIGHT = 1420
SERIES = [
    ('proxy_bandpass', 'current proxy', '#60a5fa'),
    ('gnuradio_half_sine', 'GNU Radio / half-sine', '#f97316'),
]
HIGHLIGHT_GAINS = [0.002, 0.020, 0.022]


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
            if abs(float(row['channel_spacing']) - 1.24) > 1e-9:
                continue
            design = row['design']
            gain = float(row['loop_gain'])
            by_design[design][gain] = {
                'mean_tail_residual_cfo': float(row['tail_mean_abs_residual_cfo']),
                'within_threshold_fraction': float(row['tail_within_threshold_fraction']),
            }
    return by_design


def write_public_csv(by_design: dict[str, dict[float, dict[str, float]]]) -> None:
    gains = sorted(by_design['proxy_bandpass'])
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open('w', newline='') as handle:
        writer = csv.writer(handle, lineterminator='\n')
        writer.writerow([
            'loop_gain',
            'proxy_mean_tail_residual_cfo',
            'proxy_tail_within_threshold_fraction',
            'half_sine_mean_tail_residual_cfo',
            'half_sine_tail_within_threshold_fraction',
            'half_sine_to_proxy_residual_ratio',
        ])
        for gain in gains:
            proxy = by_design['proxy_bandpass'][gain]
            half_sine = by_design['gnuradio_half_sine'][gain]
            writer.writerow([
                f'{gain:.4f}',
                f"{proxy['mean_tail_residual_cfo']:.6f}",
                f"{proxy['within_threshold_fraction']:.6f}",
                f"{half_sine['mean_tail_residual_cfo']:.6f}",
                f"{half_sine['within_threshold_fraction']:.6f}",
                f"{half_sine['mean_tail_residual_cfo'] / proxy['mean_tail_residual_cfo']:.6f}",
            ])


def main() -> None:
    by_design = load_rows()
    write_public_csv(by_design)
    gains = sorted(by_design['proxy_bandpass'])
    ratios = {
        gain: by_design['gnuradio_half_sine'][gain]['mean_tail_residual_cfo'] / by_design['proxy_bandpass'][gain]['mean_tail_residual_cfo']
        for gain in gains
    }
    first_settle_loss = next(
        gain
        for gain in gains
        if by_design['gnuradio_half_sine'][gain]['within_threshold_fraction'] < 1.0
    )

    chart_left = 92.0
    chart_top = 318.0
    chart_width = 1030.0
    residual_height = 470.0
    ratio_top = 854.0
    ratio_height = 214.0
    summary_x = 1160.0
    x_min = min(gains)
    x_max = max(gains)
    residual_max = 0.06
    ratio_min = 14.0
    ratio_max = 17.0

    def x_map(value: float) -> float:
        return chart_left + (value - x_min) / (x_max - x_min) * chart_width

    def residual_y(value: float) -> float:
        return chart_top + residual_height - value / residual_max * residual_height

    def ratio_y(value: float) -> float:
        return ratio_top + ratio_height - (value - ratio_min) / (ratio_max - ratio_min) * ratio_height

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
        text(64, 68, 'Lower loop gain calms adjacent pull,', 'title'),
        text(64, 108, 'but it does not erase detector geometry', 'title'),
        block(64, 144, [
            'At the first settle-point spacing of 1.24 R_s, slower gains shrink both residuals,',
            'yet the half-sine lane stays about 15x worse and loses settle margin first as gain rises.',
        ], 'subtitle', line_step=24),
        rect(64, 188, 1086, 920, '#122030', stroke='#324861', rx=24),
        rect(1178, 188, 458, 920, '#122030', stroke='#324861', rx=24),
        rect(64, 1134, 1572, 250, '#122030', stroke='#324861', rx=22),
        text(92, 228, 'Residual pull versus loop gain', 'label'),
        block(92, 258, wrap('Same bounded loop as the spacing note, but spacing held at 1.24 R_s and gain swept from 0.0005 to 0.0240. This asks whether the early settle boundary is mostly a tuning artifact or still a geometry problem.', 108), 'body', line_step=22),
        rect(chart_left, chart_top, chart_width, residual_height, '#0f1724', stroke='#334155', rx=24),
        text(92, 826, 'Residual ratio stays flat', 'label'),
        block(92, 856, wrap('The ratio is the clean test. If retuning truly fixed the ranking, this line would collapse toward 1. It does not.', 96), 'body', line_step=22),
        rect(chart_left, ratio_top, chart_width, ratio_height, '#0f1724', stroke='#334155', rx=24),
    ]

    for y_tick in [0.00, 0.02, 0.04, 0.06]:
        y = residual_y(y_tick)
        svg.append(line(chart_left + 18, y, chart_left + chart_width - 18, y, '#334155', width=1.4, opacity=0.8, dash='8 8'))
        svg.append(text(chart_left - 16, y + 5, f'{y_tick:.2f}', 'small', anchor='end'))
    svg.append(text(chart_left + 12, chart_top + 30, 'mean tail residual CFO', 'small'))

    for y_tick in [14.0, 15.0, 16.0, 17.0]:
        y = ratio_y(y_tick)
        svg.append(line(chart_left + 18, y, chart_left + chart_width - 18, y, '#334155', width=1.4, opacity=0.8, dash='8 8'))
        svg.append(text(chart_left - 16, y + 5, f'{y_tick:.0f}x', 'small', anchor='end'))
    svg.append(text(chart_left + 12, ratio_top + 30, 'half-sine residual  /  proxy residual', 'small'))

    x_ticks = [0.0005, 0.0020, 0.0100, 0.0200, 0.0220, 0.0240]
    for x_tick in x_ticks:
        x = x_map(x_tick)
        svg.append(line(x, chart_top + 18, x, ratio_top + ratio_height - 18, '#233246', width=1.2, opacity=0.7, dash='4 10' if abs(x_tick - first_settle_loss) < 1e-9 else None))
        svg.append(text(x, ratio_top + ratio_height + 32, f'{x_tick:.4f}', 'small', anchor='middle'))
    svg.append(text(chart_left + chart_width / 2.0, ratio_top + ratio_height + 64, 'loop gain', 'body', anchor='middle'))

    for design, label_text, color in SERIES:
        residual_points = [(x_map(gain), residual_y(by_design[design][gain]['mean_tail_residual_cfo'])) for gain in gains]
        svg.append(polyline(residual_points, color, width=5.0))
        legend_x = 774 if design == 'proxy_bandpass' else 936
        legend_y = 286.0
        svg.append(line(legend_x, legend_y, legend_x + 44, legend_y, color, width=6.0))
        svg.append(text(legend_x + 56, legend_y + 5, label_text, 'small'))

    ratio_points = [(x_map(gain), ratio_y(ratios[gain])) for gain in gains]
    svg.append(polyline(ratio_points, '#f8fafc', width=4.5))

    for gain in HIGHLIGHT_GAINS:
        for design, _, color in SERIES:
            svg.append(circle(x_map(gain), residual_y(by_design[design][gain]['mean_tail_residual_cfo']), 7.5, color))
        svg.append(circle(x_map(gain), ratio_y(ratios[gain]), 7.5, '#f8fafc'))

    loss_x = x_map(first_settle_loss)
    svg.append(line(loss_x, chart_top + 18, loss_x, ratio_top + ratio_height - 18, '#f8fafc', width=2.2, opacity=0.9, dash='10 8'))
    svg.append(rect(loss_x - 82, chart_top + 136, 164, 58, '#17283b', stroke='#94a3b8', rx=14, stroke_width=1.6))
    svg.append(block(loss_x, chart_top + 164, ['0.022', 'first settle loss'], 'small', anchor='middle', line_step=18))

    summary_rows = [
        ('gain 0.002', 'proxy 0.00030 / 100%', 'half-sine 0.00461 / 100%', 'ratio 15.2x'),
        ('gain 0.020', 'proxy 0.00283 / 100%', 'half-sine 0.04475 / 100%', 'ratio 15.8x'),
        ('gain 0.022', 'proxy 0.00309 / 100%', 'half-sine 0.04907 / 62.5%', 'ratio 15.9x'),
    ]
    box_y = 316.0
    for label_text, proxy_text, half_text, ratio_text in summary_rows:
        svg.append(rect(summary_x + 24, box_y, 410, 154, '#0f1724', stroke='#334155', rx=18))
        svg.append(text(summary_x + 44, box_y + 34, label_text, 'label'))
        svg.append(text(summary_x + 44, box_y + 68, proxy_text, 'body'))
        svg.append(text(summary_x + 44, box_y + 98, half_text, 'body'))
        svg.append(text(summary_x + 44, box_y + 128, ratio_text, 'body'))
        box_y += 172

    svg.extend([
        text(summary_x + 28, 860, 'Portable readout', 'label'),
        block(summary_x + 28, 890, wrap('Lower gain really does calm both loops. But the ratio barely moves, which means the retuning mostly rescales the same geometry penalty instead of fixing the ranking.', 41), 'body', line_step=22),
        text(summary_x + 28, 1018, 'Decision rule', 'label'),
        block(summary_x + 28, 1048, wrap('If the half-sine lane already lost badly at 1.24 R_s, turning the loop down is not the main cure. Change the spacing or the detector geometry before you expect gain alone to rescue the comparison.', 41), 'body', line_step=22),
        text(92, 1170, 'What this card protects against', 'label'),
        block(92, 1200, wrap('Do not explain the 1.24 R_s result away as a simple loop-tuning artifact. A slower loop helps both designs, but the half-sine lane stays roughly 15x worse and gives up full settle margin first as the gain comes back up.', 118), 'body', line_step=22),
        text(92, 1300, 'Source basis', 'label'),
        block(92, 1330, wrap('External framing comes from Daniel Estévez plus the GNU Radio FLL Band-Edge wiki and source, with Wireless Pi kept only for the acquisition-versus-tracking loop-bandwidth reminder. The public values here are extracted from jarbas-sdr-visual-notes/notes/band-edge-loop-gain-retuning.md and its dated 2026-05-24 research memo.', 96), 'tiny', line_step=20),
    ])

    svg.append('</svg>')

    SVG_OUT.parent.mkdir(parents=True, exist_ok=True)
    SVG_OUT.write_text('\n'.join(svg))
    export_png(SVG_OUT, PNG_OUT)


if __name__ == '__main__':
    main()
