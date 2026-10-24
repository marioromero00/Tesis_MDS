import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from robustez_sin_cohorte_nueva_24_10_2026 import attach, person_metrics


class TestRobustez(unittest.TestCase):
    def test_alignment_rejects_mismatched_participant(self):
        data = pd.DataFrame({"split": ["test"], "participant": ["P1"],
                             "window_start_utc": ["2026-01-01T00:00:00Z"],
                             "arousal_label_6s": ["bajo"], "arousal_label_2s": ["medio"],
                             "arousal_label_pca": ["bajo"]})
        prediction = pd.DataFrame({"source_row": [0], "participant": ["P2"],
                                   "window_start_utc": ["2026-01-01T00:00:00Z"],
                                   "prediction": ["bajo"]})
        with self.assertRaisesRegex(ValueError, "no alineadas"):
            attach(data, prediction, "test")

    def test_two_class_person_uses_only_present_classes(self):
        frame = pd.DataFrame({"participant": ["P1"] * 4,
                              "arousal_label_6s": ["bajo", "bajo", "alto", "alto"],
                              "prediction": ["bajo", "medio", "alto", "alto"]})
        result = person_metrics(frame, "arousal_label_6s").iloc[0]
        self.assertEqual(result.classes_present, 2)
        self.assertAlmostEqual(result.ba, .75)
        self.assertAlmostEqual(result.constant_ba, .5)


if __name__ == "__main__":
    unittest.main()
