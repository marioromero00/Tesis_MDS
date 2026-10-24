import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from contraste_temporalidad_fusion import SPECS, frame_for, sequences, person_scores
from temporales_core import preprocessor


class TestContrasteTemporalidadFusion(unittest.TestCase):
    def test_modalities_remain_disjoint_from_label_sources(self):
        for spec in SPECS.values():
            self.assertFalse(set(sum(spec["modalities"].values(), [])) & set(spec["forbidden"]))

    def test_histories_reset_at_stimulus_and_repeat_only_current(self):
        frame = pd.DataFrame({
            "split": ["train"] * 4, "participant": ["P"] * 4,
            "recording": ["R"] * 4, "segment_id": [1] * 4,
            "stimulus": ["a", "a", "b", "b"],
            "window_start_utc": pd.date_range("2020-01-01", periods=4, freq="s", tz="UTC"),
            "signal": [1., 2., 10., 20.],
        })
        prep = preprocessor().fit(frame[["signal"]])
        real, lengths = sequences(prep, frame, ["signal"], False)
        control, control_lengths = sequences(prep, frame, ["signal"], True)
        np.testing.assert_array_equal(lengths, [1, 2, 1, 2])
        np.testing.assert_array_equal(control_lengths, lengths)
        self.assertAlmostEqual(real[1, 0, 0], prep.transform(frame[["signal"]])[0, 0])
        self.assertAlmostEqual(control[1, 0, 0], prep.transform(frame[["signal"]])[1, 0])
        self.assertAlmostEqual(real[2, 0, 0], prep.transform(frame[["signal"]])[2, 0])
        self.assertTrue(np.all(real[:, 2:] == 0))
        self.assertTrue(np.all(control[:, 2:] == 0))

    def test_participant_score_uses_only_present_classes(self):
        table = pd.DataFrame({"participant": ["P", "P", "Q", "Q"],
                              "true": ["bajo", "alto", "bajo", "bajo"],
                              "prediction": ["bajo", "bajo", "bajo", "alto"]})
        scores = {row["participant"]: row["ba"] for row in person_scores(table)}
        self.assertEqual(scores, {"P": .5, "Q": .5})


if __name__ == "__main__":
    unittest.main()
