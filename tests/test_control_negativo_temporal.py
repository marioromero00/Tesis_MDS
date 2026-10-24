import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from control_negativo_temporal_24_10_2026 import shifted_labels


class TestControlNegativoTemporal(unittest.TestCase):
    def test_shift_preserves_labels_and_breaks_local_alignment(self):
        labels = np.asarray(["bajo"] * 100 + ["medio"] * 100 + ["alto"] * 100)
        frame = pd.DataFrame({"participant": ["P1"] * len(labels),
                              "recording": ["R1"] * len(labels),
                              "window_start_utc": pd.date_range("2026-01-01", periods=len(labels), freq="s", tz="UTC").astype(str),
                              "arousal_label_6s": labels})
        changed, shifts = shifted_labels(frame, np.random.default_rng(20261024))
        self.assertEqual(len(shifts), 1)
        self.assertGreaterEqual(shifts[0]["shift_rows"], 120)
        self.assertLessEqual(shifts[0]["shift_rows"], len(labels) - 120)
        np.testing.assert_array_equal(changed, np.roll(labels, shifts[0]["shift_rows"]))
        np.testing.assert_array_equal(np.sort(changed), np.sort(labels))

    def test_rejects_short_recording(self):
        frame = pd.DataFrame({"participant": ["P1"] * 240, "recording": ["R1"] * 240,
                              "window_start_utc": pd.date_range("2026-01-01", periods=240, freq="s", tz="UTC").astype(str),
                              "arousal_label_6s": ["bajo"] * 240})
        with self.assertRaisesRegex(ValueError, "demasiado corto"):
            shifted_labels(frame, np.random.default_rng(0))


if __name__ == "__main__":
    unittest.main()
