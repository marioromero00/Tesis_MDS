import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from scripts.generar_pseudoetiquetas_pca_senales import (
    causal_context, eligible_zscore, fit_teacher_pc, normalized_inputs,
)


class TestPCASenales(unittest.TestCase):
    def test_normalizacion_excluye_ventana_descartada(self):
        values = pd.Series([0., 1., 2., 100.])
        valid = pd.Series([True, True, True, False])
        result = eligible_zscore(values, pd.Series(["P2"] * 4), valid)
        np.testing.assert_allclose(result.iloc[:3], [-1.224744871, 0., 1.224744871], atol=1e-8)
        self.assertTrue(pd.isna(result.iloc[3]))

    def test_contexto_gsr_reinicia_en_hueco(self):
        frame = pd.DataFrame({"participant": ["P2"] * 4, "recording": ["R"] * 4,
                              "segment_id": [1] * 4,
                              "window_start_recording_s": [0., 1., 4., 5.]})
        result, resets = causal_context(frame, pd.Series([1., 3., 10., 14.]),
                                        pd.Series([True] * 4), 5)
        self.assertEqual(resets, 1)
        np.testing.assert_allclose(result, [1., 2., 10., 12.])

    def test_normalizacion_conserva_fila_de_cada_persona(self):
        frame = pd.DataFrame({"participant": ["P2", "P2", "P10", "P10"],
                              "pupil_mean_z": [1.0, 3.0, 100.0, 200.0]})
        result = normalized_inputs(frame, ["pupil_mean_z"])
        np.testing.assert_allclose(result.pupil_mean_z, [-1.0, 1.0, -1.0, 1.0])

    def test_pca_profesor_se_ajusta_solo_con_train(self):
        values = pd.DataFrame({"a": [-2., -1., 1., 2., 1000.],
                               "b": [-2., -1., 1., 2., -1000.]})
        train = pd.Series([True, True, True, True, False])
        reference = values.a + values.b
        model, scores, info = fit_teacher_pc(values, train, reference)
        self.assertEqual(info["train_rows"], 4)
        self.assertGreater(info["train_orientation_correlation"], 0.99)
        self.assertGreater(scores[3], scores[0])
        np.testing.assert_allclose(model.named_steps["imputer"].statistics_, [0., 0.])


if __name__ == "__main__":
    unittest.main()
