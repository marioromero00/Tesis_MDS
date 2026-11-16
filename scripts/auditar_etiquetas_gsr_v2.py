"""Reproducción del error histórico y verificación independiente de etiquetas V2."""
import json
import numpy as np
import pandas as pd
from preparar_modelado import teacher_components, zscore, transformed_feature
from reconstruir_etiquetas_gsr_calidad_v2 import ROOT, OUT, COLS, KEYS, rebuild
from atencion_binaria import digest, write


def main():
    source = ROOT / 'resultados/preprocesamiento/caracteristicas_multimodales.csv'
    partition = ROOT / 'resultados/modelado/particion_participantes.csv'
    raw = pd.read_csv(source)
    archived = pd.read_csv(ROOT / 'resultados/modelado/dataset_modelado.csv')
    identity = ['participant', 'recording', 'segment_id', 'window_start_utc']
    assert raw[identity].equals(archived[identity])
    legacy, *_ = teacher_components(raw, json.loads((ROOT / 'config/modelado.json').read_text()))
    errors = {}
    for column in ['arousal_score_2s', 'arousal_score_6s']:
        assert np.allclose(legacy[column], archived[column], rtol=1e-7, atol=1e-7, equal_nan=True)
        errors[column] = float(np.nanmax(abs(legacy[column] - archived[column])))
    normalized = raw.groupby('participant', group_keys=False).apply(
        lambda group: zscore(transformed_feature(group, COLS[0])), include_groups=False)
    displaced = int((normalized.index.to_numpy() != np.arange(len(raw))).sum())
    raw['source_row'] = np.arange(len(raw))
    raw['split'] = raw.participant.map(pd.read_csv(partition).set_index('participant').split)
    eligible = raw[raw.split.isin(['train', 'validation', 'test'])]
    rebuilt, _, _ = rebuild(eligible)
    saved = pd.read_csv(OUT / 'etiquetas.csv.gz').set_index('source_row').sort_index()
    actual = rebuilt.set_index('source_row').sort_index()
    for column in ['score2s_quality', 'score6s_quality', 'activation_binary_v2']:
        assert np.allclose(actual[column].to_numpy(dtype=float, na_value=np.nan), saved[column],
                           atol=1e-12, rtol=1e-12, equal_nan=True)
    assert actual[identity].equals(saved[identity])
    # Independent normalization by participant, with explicit source-row alignment.
    for person, group in actual.groupby('participant'):
        valid = group[group.gsr_quality_valid]
        components = valid[COLS].copy()
        components[COLS[2:]] = np.log1p(components[COLS[2:]])
        sd = components.std(ddof=0)
        components = (components - components.mean()) / sd.where(sd > 1e-8, 1.)
        components.loc[:, sd <= 1e-8] = 0.
        score = components.mean(axis=1)
        expected = (score - score.mean()) / score.std(ddof=0)
        assert np.allclose(expected, valid.score2s_quality, atol=1e-12)
    # Every labelled window has exactly five valid contiguous starts in its group.
    for _, group in actual.groupby(KEYS):
        group = group.sort_values('window_start_utc')
        for position in np.flatnonzero(group.activation_binary_v2.notna()):
            assert position >= 4
            support = group.iloc[position-4:position+1]
            assert support.gsr_quality_valid.all()
            assert pd.to_datetime(support.window_start_utc).diff().iloc[1:].eq(pd.Timedelta(seconds=1)).all()
    protocol = json.loads((OUT / 'protocolo.json').read_text())
    assert digest(source) == protocol['source_sha256']
    assert digest(partition) == protocol['partition_sha256']
    result = dict(passed=True, legacy_scores_reproduced=True, legacy_max_absolute_error=errors,
                  legacy_displaced_component_rows=displaced, legacy_total_rows=len(raw),
                  v2_reproduced=True, independent_normalization_verified=True,
                  temporal_support_verified=True, source_and_partition_unchanged=True,
                  labelled=int(actual.activation_binary_v2.notna().sum()),
                  audit_script_sha256=digest(__file__),
                  label_file_sha256=digest(OUT / 'etiquetas.csv.gz'))
    write(OUT / 'auditoria_independiente_02-11-2026.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
