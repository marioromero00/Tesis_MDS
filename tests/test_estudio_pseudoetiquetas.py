import unittest
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from scripts.comparar_pseudoetiquetas import temporal_features
from scripts.estudio_pseudoetiquetas import label


class TestEstudioPseudoetiquetas(unittest.TestCase):
    def test_quantiles_excluyen_ventanas_no_elegibles(self):
        score = pd.Series([-100.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        valid = pd.Series([False, True, True, True, True, True, True])
        result = label(score, valid, pd.Series(["P1"] * 7))
        self.assertTrue(pd.isna(result.iloc[0]))
        self.assertEqual(result.iloc[2], "bajo")
        self.assertEqual(result.iloc[5], "alto")

    def test_historial_se_reinicia_tras_salto(self):
        frame = pd.DataFrame({
            "participant": ["P1"] * 4,
            "recording": ["R"] * 4,
            "segment_id": [1] * 4,
            "window_start_utc": ["2026-01-01T00:00:00Z", "2026-01-01T00:00:01Z",
                                 "2026-01-01T00:00:04Z", "2026-01-01T00:00:05Z"],
            "x": [1.0, 3.0, 10.0, 14.0],
        })
        self.assertEqual(temporal_features(frame, ["x"])["history6_x"].tolist(),
                         [1.0, 2.0, 10.0, 12.0])


if __name__ == "__main__":
    unittest.main()
