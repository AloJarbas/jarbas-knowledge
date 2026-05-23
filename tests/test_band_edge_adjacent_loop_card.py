from __future__ import annotations

import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO / 'scripts' / 'generate_band_edge_adjacent_loop_card.py'
SPEC = importlib.util.spec_from_file_location('band_edge_card', SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class BandEdgeAdjacentLoopCardTests(unittest.TestCase):
    def test_load_source_contains_expected_tipping_point(self) -> None:
        by_design, desired_only = MODULE.load_source()
        self.assertLess(desired_only['proxy_bandpass']['mean_tail_residual_cfo'], 0.001)
        self.assertLess(desired_only['gnuradio_half_sine']['mean_tail_residual_cfo'], 0.001)
        self.assertLess(abs(by_design['proxy_bandpass'][0.0]['mean_tail_residual_cfo'] - 0.0387), 0.001)
        self.assertLess(abs(by_design['gnuradio_half_sine'][0.0]['mean_tail_residual_cfo'] - 0.0995), 0.001)
        self.assertAlmostEqual(by_design['proxy_bandpass'][0.0]['within_threshold_fraction'], 1.0, places=6)
        self.assertAlmostEqual(by_design['gnuradio_half_sine'][0.0]['within_threshold_fraction'], 0.0, places=6)

    def test_write_public_csv_emits_four_adjacent_levels(self) -> None:
        by_design, _ = MODULE.load_source()
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'card.csv'
            original = MODULE.CSV_OUT
            MODULE.CSV_OUT = target
            try:
                MODULE.write_public_csv(by_design)
            finally:
                MODULE.CSV_OUT = original
            with target.open() as handle:
                rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 4)
        self.assertEqual([row['adjacent_level_db'] for row in rows], ['-12', '-6', '0', '6'])

    def test_svg_contains_portable_claim(self) -> None:
        svg = (REPO / 'assets' / 'band-edge-adjacent-loop-tradeoff-card.svg').read_text()
        self.assertIn('make a worse adjacent-channel loop', svg)
        self.assertIn('0 dB tipping point', svg)


if __name__ == '__main__':
    unittest.main()
