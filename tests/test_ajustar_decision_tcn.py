import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ajustar_decision_tcn import adjust


class TestAjustarDecisionTCN(unittest.TestCase):
    def test_smoothing_is_causal_and_resets_at_stimulus(self):
        frame = pd.DataFrame({
            "split": ["train"] * 4, "participant": ["P"] * 4,
            "recording": ["R"] * 4, "segment_id": [1] * 4,
            "stimulus": ["a", "a", "b", "b"],
            "window_start_utc": pd.date_range("2020-01-01", periods=4, freq="s", tz="UTC"),
        })
        p = np.array([[.8, .1, .1], [.1, .8, .1], [.2, .2, .6], [.1, .7, .2]])
        output = adjust(frame, p, 4, 1.)
        np.testing.assert_allclose(output[0], p[0])
        np.testing.assert_allclose(output[1], p[:2].mean(axis=0))
        np.testing.assert_allclose(output[2], p[2])
        changed = p.copy()
        changed[-1] = [1., 0., 0.]
        np.testing.assert_allclose(adjust(frame, changed, 4, 1.)[:3], output[:3])

    def test_medium_bias_changes_decision_without_changing_labels(self):
        frame = pd.DataFrame({"participant": ["P"]})
        p = np.array([[.45, .35, .20]])
        original = adjust(frame, p, 1, 1.)
        shifted = adjust(frame, p, 1, 1.5)
        self.assertEqual(original.argmax(axis=1).item(), 0)
        self.assertEqual(shifted.argmax(axis=1).item(), 1)
        np.testing.assert_allclose(shifted.sum(axis=1), 1.)


if __name__ == "__main__":
    unittest.main()
