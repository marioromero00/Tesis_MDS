"""Control descriptivo: predice las nuevas pseudoetiquetas solo con el estímulo."""
from pathlib import Path
import argparse
import json

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "resultados/pca_senales_v2_24-10-2026"
TARGETS = {"attention": "attention_label_teacher_pca",
           "arousal": "arousal_label_teacher_pca_6s"}


def main(output: Path = OUT) -> None:
    data = pd.read_csv(output / "dataset_pca_senales.csv")
    rows = []
    for task, target in TARGETS.items():
        frame = data.loc[data.eligible_attention & data.split.isin(["train", "validation", "test"])
                         & data[target].notna()]
        train = frame.loc[frame.split.eq("train")]
        model = Pipeline([
            ("encoder", ColumnTransformer([("stimulus", OneHotEncoder(handle_unknown="ignore"), ["stimulus"])])),
            ("classifier", LogisticRegression(max_iter=2000, class_weight="balanced")),
        ]).fit(train[["stimulus"]], train[target])
        for split in ["validation", "test"]:
            part = frame.loc[frame.split.eq(split)]
            rows.append({"task": task, "split": split,
                         "balanced_accuracy": float(balanced_accuracy_score(
                             part[target], model.predict(part[["stimulus"]])))})
    result = pd.DataFrame(rows)
    result.to_csv(output / "control_estimulo.csv", index=False)
    print(result.to_string(index=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(ROOT / "config/pca_senales_v2.json"))
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    main(ROOT / config["output_dir"])
