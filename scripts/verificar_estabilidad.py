"""Audita entrega de estabilidad: integridad, cobertura OOF y metricas guardadas."""
from pathlib import Path
import json
import hashlib
import numpy as np
import pandas as pd
from analisis_variables import score

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'resultados/estabilidad_variables_07-09-2026'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads((OUTPUT / 'manifiesto.json').read_text(encoding='utf-8'))
    protocol = json.loads((OUTPUT / 'protocolo.json').read_text(encoding='utf-8'))
    frozen = json.loads((OUTPUT / 'conjuntos_congelados.json').read_text(encoding='utf-8'))
    assert manifest['test_evaluated'] is False
    assert protocol['script_sha256'] == digest(ROOT / 'scripts/estabilidad_variables.py')
    assert manifest['protocol_sha256'] == digest(OUTPUT / 'protocolo.json')
    assert frozen['cv_summary_sha256'] == digest(OUTPUT / 'resumen_cv.csv')
    data = pd.read_csv(ROOT / 'resultados/modelado/dataset_modelado.csv')
    train = data.loc[data.split.eq('train')]
    expected = set(train.participant)
    assert expected == set(manifest['cv_participants'])
    assert expected.isdisjoint(manifest['validation_participants'])
    fold_map = {}
    for f in protocol['folds']:
        assert set(f['fit']).isdisjoint(f['evaluation'])
        assert set(f['fit']) | set(f['evaluation']) == expected
        for p in f['evaluation']:
            assert p not in fold_map
            fold_map[p] = f['fold']
    assert set(fold_map) == expected
    predictions = pd.read_csv(OUTPUT / 'predicciones_oof.csv.gz', dtype={'actual': str, 'predicted': str})
    keys = ['task', 'kind', 'model', 'subset']
    scores = pd.read_csv(OUTPUT / 'metricas_participantes_oof.csv').set_index(keys + ['participant'])
    checks = 0
    for identity, group in predictions.groupby(keys):
        task, kind, model, subset = identity
        target = frozen['targets'][task][0 if kind == 'regression' else 1]
        expected_counts = train.loc[train[target].notna()].groupby('participant').size()
        counts = group.groupby('participant').size()
        pd.testing.assert_series_equal(counts.sort_index(), expected_counts.sort_index())
        assert group.fold.eq(group.participant.map(fold_map)).all()
        for person, part in group.groupby('participant'):
            actual = part.actual.to_numpy() if kind == 'classification' else part.actual.to_numpy(float)
            predicted = part.predicted.to_numpy() if kind == 'classification' else part.predicted.to_numpy(float)
            value = score(actual, predicted, kind)
            np.testing.assert_allclose(value, scores.loc[(*identity, person), 'score'], rtol=1e-10, atol=1e-12)
            checks += 1
    assert checks == len(scores)
    assert not scores.index.duplicated().any()
    for artifact in manifest['final_models']:
        assert artifact['reload_verified']
        assert digest(OUTPUT / artifact['path']) == artifact['sha256']
        assert set(artifact['train_participants']) == expected
        assert artifact['features'] == frozen['features'][artifact['task']][artifact['subset']]
    log = (OUTPUT / 'pruebas.txt').read_text(errors='replace')
    assert 'Ran 18 tests' in log and 'OK' in log
    audit = dict(tests_passed=18, fold_models=manifest['fold_models'], final_models=len(manifest['final_models']),
                 oof_predictions=len(predictions), participant_metrics_recomputed=checks,
                 test_evaluated=False, participants_disjoint=True,
                 source_hashes={p.name: digest(p) for p in (ROOT / 'scripts').glob('*.py')},
                 output_hashes={str(p.relative_to(OUTPUT)): digest(p) for p in OUTPUT.rglob('*')
                                if p.is_file() and p.name != 'verificacion_entrega.json'})
    (OUTPUT / 'verificacion_entrega.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in audit.items() if not k.endswith('hashes')}, indent=2))


if __name__ == '__main__':
    main()
