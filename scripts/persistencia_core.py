"""Filtros causales: nunca consumen etiquetas durante la prediccion."""
import numpy as np
from optimizar_historial import histories, smooth
from temporales_core import CLASSES
from hiperparametros_core import TARGET
from ensambles_core import predict as base_predict


def starts(frame):
    return np.asarray([len(ix)==1 for _,ix in histories(frame,2,'recording')])


def transitions(frame):
    reset=starts(frame); y=frame[TARGET].map(dict(zip(CLASSES,range(3)))).to_numpy(int)
    matrices=[]
    for indices in frame.groupby('participant',sort=True).indices.values():
        counts=np.ones((3,3))
        for i in indices:
            if not reset[i]: counts[y[i-1],y[i]]+=1
        matrices.append(counts/counts.sum(axis=1,keepdims=True))
    result=np.mean(matrices,axis=0)
    return result/result.sum(axis=1,keepdims=True)


def grid():
    choices=[dict(candidate_id=f'mean_{w}',family='mean',window=w) for w in [1,4,16,64]]
    choices += [dict(candidate_id=f'ema_{a}',family='ema',alpha=a) for a in [.02,.1,.3]]
    choices += [dict(candidate_id=f'hmm_{s}_{t}',family='hmm',shrink=s,temperature=t)
                for s in [.01,.1,.5] for t in [.25,1.,4.]]
    return choices


def decode(frame,probabilities,matrix,choice):
    if choice['family']=='mean': return smooth(frame,probabilities,choice['window'])
    reset=starts(frame); result=np.empty_like(probabilities)
    trans=(1-choice.get('shrink',0))*matrix+choice.get('shrink',0)/3
    for i,p in enumerate(probabilities):
        if choice['family']=='ema':
            q=p if reset[i] else choice['alpha']*p+(1-choice['alpha'])*result[i-1]
        else:
            prior=np.ones(3)/3 if reset[i] else result[i-1]@trans
            logp=np.log(np.clip(p,1e-12,1))/choice['temperature']+np.log(prior)
            q=np.exp(logp-logp.max())
        result[i]=q/q.sum()
    return result


def predict(bundle,frame):
    return decode(frame,base_predict(bundle['base'],frame),bundle['transition'],bundle['choice'])
