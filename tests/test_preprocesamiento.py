import importlib.util
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


SCRIPT = Path(__file__).parents[1] / "scripts" / "preprocesamiento_secuencial.py"
SPEC = importlib.util.spec_from_file_location("preprocesamiento", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TestPreprocesamiento(unittest.TestCase):
    def test_normaliza_solo_participantes_experimentales(self):
        self.assertEqual(MODULE.normalize_participant("P01"), "P1")
        self.assertEqual(MODULE.normalize_participant("p48"), "P48")
        self.assertIsNone(MODULE.normalize_participant("Test_Participant"))
        self.assertIsNone(MODULE.normalize_participant("P49"))

    def test_segmentos_no_cruzan_cambio_de_estimulo(self):
        frame = pd.DataFrame({
            "Recording timestamp": [0, 1, 2, 3],
            "Presented Stimulus name": ["Texto", None, "Video", None],
        })
        result = MODULE.stimulus_segments(frame)
        self.assertEqual(result["stimulus"].tolist(), ["Texto", "Texto", "Video", "Video"])
        self.assertEqual(result["segment_id"].nunique(), 2)

    def test_caracteristicas_eeg_son_deterministas(self):
        hz = 125.0
        t = np.arange(250) / hz
        signal = np.tile(np.sin(2 * np.pi * 10 * t)[:, None], (1, 16))
        bands = {"alpha": [8, 13], "beta": [13, 30]}
        first = MODULE.eeg_features(signal, hz, bands)
        second = MODULE.eeg_features(signal, hz, bands)
        self.assertEqual(first, second)
        self.assertGreater(first["eeg_alpha_relative"], 0.95)
        self.assertLess(first["eeg_beta_relative"], 0.01)

    def test_configuracion_excluye_calibracion(self):
        import json
        config_path = Path(__file__).parents[1] / "config" / "preprocesamiento.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertIn("Eyetracker Calibration", config["excluded_stimuli"])
        self.assertEqual(
            config["eeg"]["excluded_quality_participants"],
            ["P1", "P14", "P17", "P25"],
        )


if __name__ == "__main__":
    unittest.main()
