import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from scripts.experimentar_mejora_condicional_v2 import add_history
from scripts.verificar_mejora_condicional_v2 import shuffle_within_stimulus


class TestMejoraCondicionalV2(unittest.TestCase):
    def test_historial_es_causal_y_reinicia_tras_hueco(self):
        frame = pd.DataFrame({"participant": ["P1"] * 4, "recording": ["R"] * 4,
                              "segment_id": [1] * 4,
                              "window_start_utc": ["2026-01-01T00:00:00Z", "2026-01-01T00:00:01Z",
                                                   "2026-01-01T00:00:04Z", "2026-01-01T00:00:05Z"]})
        values = pd.DataFrame({"stimulus": ["A"] * 4, "signal_0": [1., 3., 10., 14.]})
        result = add_history(values, frame)
        np.testing.assert_allclose(result.history6_signal_0, [1., 2., 10., 12.])

    def test_permutacion_respeta_participante_y_estimulo(self):
        frame = pd.DataFrame({"participant": ["P1"] * 4 + ["P2"] * 4,
                              "stimulus": ["A", "A", "B", "B"] * 2})
        x = pd.DataFrame({"stimulus": frame.stimulus,
                          "signal_0": np.arange(8), "signal_1": np.arange(8) + 20})
        shuffled = shuffle_within_stimulus(x, frame)
        pd.testing.assert_series_equal(shuffled.stimulus, x.stimulus)
        for _, positions in frame.groupby(["participant", "stimulus"]).indices.items():
            original = sorted(map(tuple, x.loc[positions, ["signal_0", "signal_1"]].to_numpy()))
            changed = sorted(map(tuple, shuffled.loc[positions, ["signal_0", "signal_1"]].to_numpy()))
            self.assertEqual(original, changed)


if __name__ == "__main__":
    unittest.main()
