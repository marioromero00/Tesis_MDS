# Cargar un modelo del contraste

Desde la raíz del repositorio, con `requirements_temporales.txt` instalado:

```python
import sys, json, joblib, pandas as pd, numpy as np
sys.path.insert(0, 'scripts')
from control_historial import OUT, FEATURES, TARGETS, current_control
from temporales_core import prepare_frame, history_indices, sequence_array, load_net, raw_predict, decode
catalog = json.loads((OUT/'catalogo_modelos.json').read_text(encoding='utf-8'))
meta = next(m for m in catalog if m['fold']==1 and m['kind']=='classification'
            and m['architecture']=='BiLSTM' and m['mode']=='history' and m['seed']==20260907)
data = pd.read_csv('resultados/modelado/dataset_modelado.csv')
frame = prepare_frame(data.loc[data.participant.isin(meta['evaluation_participants'])],
                      'arousal_primary_6s', TARGETS, 'train')
indices, lengths = history_indices(frame, 8)
prep = joblib.load(OUT/meta['preprocessor'])
x = current_control(sequence_array(prep.transform(frame[FEATURES]), indices), lengths, meta['mode'])
prediction = decode(raw_predict(load_net(meta, OUT), x, lengths), meta['kind'])
```

`mode` debe aplicarse también a los controles repetidos. El MLP lee solo la ventana actual.
Los `.joblib` estáticos ya incluyen su preprocesador y aceptan las cinco columnas en orden.
Los modelos corresponden a folds de evaluación, no a un ajuste final sobre los 25 participantes.
