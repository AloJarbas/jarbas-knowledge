#!/usr/bin/env python3
from __future__ import annotations

import csv
import shutil
import subprocess
import tempfile
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SOURCE_CSV = REPO.parent / 'jarbas-sdr-visual-notes' / 'assets' / '2026-05-23-band-edge-closed-loop-adjacent-pull.csv'
CSV_OUT = REPO / 'assets' / 'band-edge-adjacent-loop-tradeoff-card.csv'
SVG_OUT = REPO / 'assets' / 'band-edge-adjacent-loop-tradeoff-card.svg'
PNG_OUT = REPO / 'assets' / 'band-edge-adjacent-loop-tradeoff-card.png'

WIDTH = 1700
HEIGHT = 1520
THRESHOLD = 0.05
X_VALUES = [-12.0, -6.0, 0.0, 6.0]
SERIES = [
    ('proxy_bandpass', 'current proxy', '#60a5fa'),
    ('gnuradio_half_sine', 'GNU Radio / half-sine', '#f97316'),
]


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


def polyline(points: list[tuple[float, float]], stroke: str, *, width: float = 5.0) -> str:
    encoded = ' '.join(f'{x:.1f},{y:.1f}' for x, y in points)
    return (
        f'<polyline fill="none" stroke="{stroke}" stroke-width="{width:.1f}" '
        f'stroke-linecap="round" stroke-linejoin="round" points="{encoded}"/>'
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
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            if not png_path.exists():
                raise
        sips = shutil.which('sips')
        if sips is not None:
            subprocess.run(
                [sips, '--setProperty', 'dpiWidth', '300', '--setProperty', 'dpiHeight', '300', str(png_path)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        return True
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


def load_source() -> tuple[dict[str, dict[float, dict[str, float]]], dict[str, dict[str, float]]]:
    by_design: dict[str, dict[float, dict[str, float]]] = {name: {} for name, _, _ in SERIES}
    desired_only: dict[str, dict[str, float]] = {}
    with SOURCE_CSV.open() as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            design = row['design']
            entry = {
                'mean_tail_residual_cfo': float(row['tail_mean_abs_residual_cfo']),
                'within_threshold_fraction': float(row['tail_within_threshold_fraction']),
                'peak_tail_residual_cfo': float(row['tail_peak_abs_residual_cfo']),
            }
            if row['adjacent_enabled'] == 'False':
                desired_only[design] = entry
            else:
                by_design[design][float(row['adjacent_relative_power_db'])] = entry
    return by_design, desired_only


def write_public_csv(by_design: dict[str, dict[float, dict[str, float]]]) -> None:
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open('w', newline='') as handle:
        writer = csv.writer(handle, lineterminator='\n')
        writer.writerow([
            'adjacent_level_db',
            'proxy_mean_tail_residual_cfo',
            'proxy_tail_within_threshold_fraction',
            'half_sine_mean_tail_residual_cfo',
            'half_sine_tail_within_threshold_fraction',
        ])
        for x_value in X_VALUES:
            proxy = by_design['proxy_bandpass'][x_value]
            half_sine = by_design['gnuradio_half_sine'][x_value]
            writer.writerow([
                f'{x_value:.0f}',
                f"{proxy['mean_tail_residual_cfo']:.6f}",
                f"{proxy['within_threshold_fraction']:.6f}",
                f"{half_sine['mean_tail_residual_cfo']:.6f}",
                f"{half_sine['within_threshold_fraction']:.6f}",
            ])


def main() -> None:
    by_design, desired_only = load_source()
    write_public_csv(by_design)

    chart_left = 112.0
    chart_top = 320.0
    chart_width = 1040.0
    chart_height = 500.0
    x_min = min(X_VALUES)
    x_max = max(X_VALUES)
    y_max = 0.20

    def x_map(value: float) -> float:
        return chart_left + (value - x_min) / (x_max - x_min) * chart_width

    def y_map(value: float) -> float:
        return chart_top + chart_height - value / y_max * chart_height

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
        text(64, 68, 'A better isolated discriminator can still', 'title'),
        text(64, 108, 'make a worse adjacent-channel loop', 'title'),
        block(64, 144, [
            'For the bounded QPSK band-edge test, the GNU Radio / half-sine lane is cleaner on the desired-only waveform,',
            'yet it gets pulled farther once a nearby channel enters the loop. That is why detector ranking cannot stop at isolated-slope plots.',
        ], 'subtitle', line_step=24),
        rect(64, 188, 1210, 654, '#122030', stroke='#324861', rx=24),
        rect(1298, 188, 338, 654, '#122030', stroke='#324861', rx=24),
        rect(64, 874, 500, 566, '#122030', stroke='#324861', rx=22),
        rect(598, 874, 500, 566, '#122030', stroke='#324861', rx=22),
        rect(1132, 874, 504, 566, '#122030', stroke='#324861', rx=22),
    ]

    svg.extend([
        text(92, 226, 'Bounded stress result', 'label'),
        block(92, 256, wrap('Mean tail residual CFO after one blockwise loop, one adjacent interferer at 1.0 R_s spacing, 63 taps, alpha = 0.35, 4 samples/symbol, and one shared settle band at ±0.05 R_s.', 104), 'body', line_step=22),
        rect(chart_left, chart_top, chart_width, chart_height, '#0f1724', stroke='#334155', rx=24),
    ])

    for y_tick in [0.00, 0.05, 0.10, 0.15, 0.20]:
        y = y_map(y_tick)
        svg.append(line(chart_left + 20, y, chart_left + chart_width - 20, y, '#334155', width=1.6, opacity=0.8, dash='8 8' if y_tick == THRESHOLD else None))
        svg.append(text(chart_left - 16, y + 6, f'{y_tick:.2f}', 'small', anchor='end'))
    svg.append(text(chart_left + 12, chart_top + 30, 'mean tail residual CFO', 'small'))

    for x_tick in X_VALUES:
        x = x_map(x_tick)
        svg.append(line(x, chart_top + 18, x, chart_top + chart_height - 18, '#233246', width=1.2, opacity=0.7))
        svg.append(text(x, chart_top + chart_height + 34, f'{int(x_tick):+d} dB', 'small', anchor='middle'))
    svg.append(text(chart_left + chart_width / 2.0, chart_top + chart_height + 68, 'adjacent channel power relative to desired', 'body', anchor='middle'))
    svg.append(text(chart_left + chart_width - 130, y_map(THRESHOLD) - 12, 'settle band  ±0.05 R_s', 'small'))

    legend_y = 286.0
    for idx, (_, label_text, color) in enumerate(SERIES):
        x0 = 760 + idx * 230
        svg.append(line(x0, legend_y, x0 + 46, legend_y, color, width=6.0))
        svg.append(text(x0 + 58, legend_y + 6, label_text, 'small'))

    for design, label_text, color in SERIES:
        points = [(x_map(x_value), y_map(by_design[design][x_value]['mean_tail_residual_cfo'])) for x_value in X_VALUES]
        svg.append(polyline(points, color, width=5.0))
        for x_value, (x, y) in zip(X_VALUES, points):
            svg.append(circle(x, y, 7.0, color))

    x_zero = x_map(0.0)
    svg.append(line(x_zero, chart_top + 10, x_zero, chart_top + chart_height - 10, '#facc15', width=2.5, dash='10 10'))
    svg.append(text(x_zero, chart_top + 28, '0 dB tipping point', 'small', anchor='middle'))

    desired_proxy = desired_only['proxy_bandpass']['mean_tail_residual_cfo']
    desired_half = desired_only['gnuradio_half_sine']['mean_tail_residual_cfo']
    svg.append(text(1326, 230, 'Desired only', 'label'))
    svg.append(block(1326, 264, [
        f'proxy: {desired_proxy:.4f} R_s tail pull',
        f'half-sine: {desired_half:.4f} R_s tail pull',
        'both stay inside the settle band',
    ], 'body', line_step=24))
    svg.append(text(1326, 374, 'At 0 dB adjacent', 'label'))
    svg.append(block(1326, 408, [
        f'proxy: {by_design["proxy_bandpass"][0.0]["mean_tail_residual_cfo"]:.4f} R_s, 100% inside',
        f'half-sine: {by_design["gnuradio_half_sine"][0.0]["mean_tail_residual_cfo"]:.4f} R_s, 0% inside',
    ], 'body', line_step=24))
    svg.append(text(1326, 522, 'Interpretation', 'label'))
    svg.append(block(1326, 556, wrap('The half-sine lane fixes isolated near-lock slope, but this bounded mixed-signal loop shows that the same wider detector pays more adjacent-channel pull.', 32), 'body', line_step=22))
    svg.append(block(1326, 720, [
        'Tail band fractions:',
        '-12 dB and -6 dB: both lanes stay inside.',
        '0 dB: proxy stays inside, half-sine does not.',
        '+6 dB: both lanes fail the same settle band.',
    ], 'tiny', line_step=18))

    svg.append(text(90, 910, 'What this note is protecting against', 'label'))
    for idx, bullet in enumerate([
        'Ranking detector variants on isolated-signal slope alone.',
        'Treating a static adjacent-power sweep as if it were already a loop result.',
        'Calling the wider half-sine lane simply better or simply worse without stating the channel context.',
    ]):
        svg.append(block(90, 954 + idx * 124, wrap(f'• {bullet}', 44), 'body', line_step=22))

    svg.append(text(624, 910, 'Use it for', 'label'))
    for idx, bullet in enumerate([
        'Choosing between detector variants when one nearby interferer is plausible.',
        'Deciding when the next honest experiment must be loop-level rather than detector-only.',
        'Explaining why “better isolated discriminator” is not the same sentence as “more robust receiver.”',
    ]):
        svg.append(block(624, 954 + idx * 124, wrap(f'• {bullet}', 44), 'body', line_step=22))

    svg.append(text(1158, 910, 'Best next move', 'label'))
    for idx, bullet in enumerate([
        'Vary one knob only after this: spacing first is the cleanest follow-up.',
        'Keep the same bounded loop and ask where the preference flips back.',
        'Do not broaden this into BER, AGC, or a full modem benchmark.',
    ]):
        svg.append(block(1158, 954 + idx * 124, wrap(f'• {bullet}', 44), 'body', line_step=22))

    svg.append(text(64, 1468, 'Source basis: Daniel Estévez on band-edge construction and adjacent-channel cost, GNU Radio FLL docs + source for the actual half-sine loop contract, Wireless Pi for matched-filter intuition, and local evidence from jarbas-sdr-visual-notes.', 'small'))
    svg.append(text(64, 1492, 'This is a bounded receive-side comparison card, not a full synchronization survey or a generic statement about all FLLs.', 'small'))
    svg.append('</svg>')

    SVG_OUT.parent.mkdir(parents=True, exist_ok=True)
    SVG_OUT.write_text('\n'.join(svg) + '\n')
    exported = export_png(SVG_OUT, PNG_OUT)
    if exported:
        print(f'WROTE {CSV_OUT}, {SVG_OUT}, and {PNG_OUT}')
    else:
        print(f'WROTE {CSV_OUT} and {SVG_OUT}')


if __name__ == '__main__':
    main()
