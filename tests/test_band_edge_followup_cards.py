from __future__ import annotations

import csv
import importlib.util
from pathlib import Path
import re
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    script_path = REPO / relative_path
    spec = importlib.util.spec_from_file_location(name, script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


SPACING = load_module('band_edge_spacing_card', 'scripts/generate_band_edge_spacing_two_boundaries_card.py')
RETUNING = load_module('band_edge_retuning_card', 'scripts/generate_band_edge_loop_gain_retuning_card.py')


class BandEdgeSpacingTwoBoundariesCardTests(unittest.TestCase):
    def test_load_rows_contains_split_boundaries(self) -> None:
        by_design = SPACING.load_rows()
        self.assertAlmostEqual(by_design['proxy_bandpass'][1.24]['mean_tail_residual_cfo'], 0.002826, places=4)
        self.assertAlmostEqual(by_design['gnuradio_half_sine'][1.24]['within_threshold_fraction'], 1.0, places=6)
        self.assertGreater(by_design['gnuradio_half_sine'][1.24]['mean_tail_residual_cfo'], by_design['proxy_bandpass'][1.24]['mean_tail_residual_cfo'])
        self.assertLess(by_design['gnuradio_half_sine'][1.57]['mean_tail_residual_cfo'], by_design['proxy_bandpass'][1.57]['mean_tail_residual_cfo'])

    def test_write_public_csv_emits_spacing_sweep(self) -> None:
        by_design = SPACING.load_rows()
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'spacing.csv'
            original = SPACING.CSV_OUT
            SPACING.CSV_OUT = target
            try:
                SPACING.write_public_csv(by_design)
            finally:
                SPACING.CSV_OUT = original
            with target.open() as handle:
                rows = list(csv.DictReader(handle))
        self.assertEqual(rows[0]['channel_spacing'], '0.80')
        self.assertEqual(rows[-1]['channel_spacing'], '1.65')
        self.assertEqual(len(rows), len(by_design['proxy_bandpass']))

    def test_svg_contains_two_boundary_claim(self) -> None:
        svg = (REPO / 'assets' / 'band-edge-spacing-two-boundaries-card.svg').read_text()
        self.assertIn('settle first, ranking later', svg)
        self.assertIn('1.24 R_s', svg)
        self.assertIn('1.57 R_s', svg)


class PublicNoteAssetLinkTests(unittest.TestCase):
    def test_note_asset_links_resolve(self) -> None:
        image_pattern = re.compile(r'!\[[^\]]*\]\((\.\./assets/[^)]+)\)')
        missing: list[str] = []
        for note_path in sorted((REPO / 'notes').glob('*.md')):
            text = note_path.read_text()
            for relative_asset in image_pattern.findall(text):
                asset_path = (note_path.parent / relative_asset).resolve()
                if not asset_path.exists():
                    missing.append(f'{note_path.relative_to(REPO)} -> {relative_asset}')
        self.assertFalse(missing, '\n'.join(missing))


class BandEdgeLoopGainRetuningCardTests(unittest.TestCase):
    def test_load_rows_preserves_flat_ratio_story(self) -> None:
        by_design = RETUNING.load_rows()
        ratio_low = by_design['gnuradio_half_sine'][0.002]['mean_tail_residual_cfo'] / by_design['proxy_bandpass'][0.002]['mean_tail_residual_cfo']
        ratio_mid = by_design['gnuradio_half_sine'][0.02]['mean_tail_residual_cfo'] / by_design['proxy_bandpass'][0.02]['mean_tail_residual_cfo']
        self.assertGreater(ratio_low, 15.0)
        self.assertGreater(ratio_mid, 15.0)
        self.assertLess(abs(ratio_low - ratio_mid), 1.0)
        self.assertLess(by_design['gnuradio_half_sine'][0.02]['within_threshold_fraction'], 1.000001)
        self.assertLess(by_design['gnuradio_half_sine'][0.022]['within_threshold_fraction'], 1.0)

    def test_write_public_csv_emits_gain_sweep(self) -> None:
        by_design = RETUNING.load_rows()
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'retuning.csv'
            original = RETUNING.CSV_OUT
            RETUNING.CSV_OUT = target
            try:
                RETUNING.write_public_csv(by_design)
            finally:
                RETUNING.CSV_OUT = original
            with target.open() as handle:
                rows = list(csv.DictReader(handle))
        self.assertEqual(rows[0]['loop_gain'], '0.0005')
        self.assertEqual(rows[-1]['loop_gain'], '0.0240')
        self.assertEqual(len(rows), len(by_design['proxy_bandpass']))

    def test_svg_contains_retuning_warning(self) -> None:
        svg = (REPO / 'assets' / 'band-edge-loop-gain-retuning-card.svg').read_text()
        self.assertIn('does not erase detector geometry', svg)
        self.assertIn('ratio barely moves', svg)
        self.assertIn('first settle loss', svg)


if __name__ == '__main__':
    unittest.main()
