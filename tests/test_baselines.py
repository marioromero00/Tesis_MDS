import importlib.util
import contextlib
import io
import json
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

import joblib
import numpy as np
import pandas as pd


SCRIPT = Path(__file__).parents[1] / "scripts" / "baselines_estaticos.py"
SPEC = importlib.util.spec_from_file_location("baselines", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TestBaselines(unittest.TestCase):
    def setUp(self):
        self.partition = pd.DataFrame({"participant": ["P1", "P2", "P3"],
                                       "split": ["train", "validation", "test"]})

    def test_accepts_frozen_partition(self):
        MODULE.validate_partition(self.partition.copy(), self.partition)

    def test_rejects_participant_leakage(self):
        data = pd.concat([self.partition,
                          pd.DataFrame({"participant": ["P1"], "split": ["test"]})])
        with self.assertRaisesRegex(ValueError, "mas de un split"):
            MODULE.validate_partition(data, self.partition)

    def test_rejects_changed_frozen_assignment(self):
        data = self.partition.copy()
        data.loc[1, "split"] = "test"
        with self.assertRaisesRegex(ValueError, "no coincide"):
            MODULE.validate_partition(data, self.partition)

    def test_all_six_pipelines_reload_with_preprocessing(self):
        x = pd.DataFrame({"eeg": np.arange(30, dtype=float),
                          "gsr": [np.nan, 1., 2.] * 10,
                          "all_missing": [np.nan] * 30})
        unseen = pd.DataFrame({"eeg": [np.nan, 31., 42.],
                               "gsr": [5., np.nan, 1.],
                               "all_missing": [np.nan] * 3})
        with tempfile.TemporaryDirectory() as temporary:
            for kind, models, y in [
                ("regression", MODULE.regression_models(7, 3), np.arange(30) / 30),
                ("classification", MODULE.classification_models(7, 3),
                 np.array(["bajo", "medio", "alto"] * 10)),
            ]:
                for name, model in models.items():
                    with self.subTest(kind=kind, model=name):
                        model.fit(x, y)
                        path = Path(temporary) / kind / f"{name}.joblib"
                        result = MODULE.save_pipeline(model, path, unseen)
                        self.assertTrue(result["reload_verified"])
                        restored = joblib.load(path)
                        self.assertEqual(restored.feature_names_in_.tolist(), x.columns.tolist())
                        np.testing.assert_array_equal(model.predict(unseen), restored.predict(unseen))

    def test_complete_run_writes_30_models_and_manifest(self):
        rng = np.random.default_rng(7)
        columns = MODULE.EEG + MODULE.GSR + MODULE.EYE + MODULE.PUPIL
        data = pd.DataFrame(rng.normal(size=(45, len(columns))), columns=columns)
        data["participant"] = np.repeat(["P1", "P2", "P3"], 15)
        data["split"] = np.repeat(["train", "validation", "test"], 15)
        data["window_start_utc"] = np.arange(45)
        for stem in ["attention", "arousal"]:
            variants = ["equal", "pca"] if stem == "attention" else ["6s", "2s", "pca"]
            for variant in variants:
                data[f"{stem}_score_{variant}"] = rng.normal(size=45)
                data[f"{stem}_label_{variant}"] = ["bajo", "medio", "alto"] * 15
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            source.mkdir()
            data.to_csv(source / "dataset_modelado.csv", index=False)
            self.partition.to_csv(source / "particion_participantes.csv", index=False)
            (root / "requirements.txt").write_text("test\n", encoding="utf-8")
            config = {"output_dir": "source", "random_seed": 7,
                      "baselines": {"random_forest_estimators": 2}}
            config_path = root / "config.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")
            args = ["baselines", "--config", str(config_path), "--run-dir", "run"]
            with patch.object(MODULE, "ROOT", root), patch("sys.argv", args), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(MODULE.main(), 0)
            manifest = json.loads((root / "run/manifiesto_baselines.json").read_text(encoding="utf-8"))
            self.assertEqual(len(manifest["artifacts"]), 30)
            self.assertEqual(manifest["metrics_rows"], 60)
            for artifact in manifest["artifacts"]:
                self.assertEqual(artifact["train_participants"], ["P1"])
                self.assertTrue(artifact["reload_verified"])
                self.assertTrue((root / "run" / artifact["path"]).with_suffix(".json").exists())


if __name__ == "__main__":
    unittest.main()
