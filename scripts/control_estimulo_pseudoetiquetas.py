"""Control negativo: predice las pseudoetiquetas usando solo el nombre del estímulo."""
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "resultados/estudio_pseudoetiquetas_24-10-2026"
TARGETS = ["attention_label_equal", "attention_label_eye_only", "arousal_label_6s",
           "arousal_label_gsr_continuous_6s"]


def main() -> None:
    data = pd.read_csv(OUT / "dataset_sensibilidad.csv")
    rows = []
    for target in TARGETS:
        frame = data.loc[data.eligible_attention & data.split.isin(["train", "validation", "test"])
                         & data[target].notna()]
        model = Pipeline([
            ("encoder", ColumnTransformer([("stimulus", OneHotEncoder(handle_unknown="ignore"), ["stimulus"])])),
            ("classifier", LogisticRegression(max_iter=2000, class_weight="balanced")),
        ])
        train = frame.loc[frame.split.eq("train")]
        model.fit(train[["stimulus"]], train[target])
        for split in ["validation", "test"]:
            part = frame.loc[frame.split.eq(split)]
            rows.append({"target": target, "split": split, "rows": len(part),
                         "balanced_accuracy": float(balanced_accuracy_score(
                             part[target], model.predict(part[["stimulus"]])))})
    result = pd.DataFrame(rows)
    result.to_csv(OUT / "control_estimulo.csv", index=False)
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
