"""Adaptacion offline de salidas por persona, sin etiquetas de esa persona."""
import numpy as np
from scipy.stats import rankdata
from optimizar_historial import smooth
from ensambles_core import predict as base_predict


def grid():
    candidates=[]
    for window in [1,8,32,64]:
        for lo in [.2,1/3,.4]:
            for hi in [.6,2/3,.8]:
                candidates.append(dict(candidate_id=f'rank_w{window}_l{lo:.3f}_h{hi:.3f}',family='rank',window=window,low=lo,high=hi))
        for strength in [.25,.5,1.]:
            for scale in [False,True]:
                candidates.append(dict(candidate_id=f'center_w{window}_s{strength}_scale{scale}',family='center',window=window,strength=strength,scale=scale))
    return candidates


def adapt(frame,raw,choice):
    probabilities=smooth(frame,raw,choice['window']); result=np.zeros_like(probabilities)
    for indices in frame.groupby('participant',sort=True).indices.values():
        logits=np.log(np.clip(probabilities[indices],1e-12,1))
        if choice['family']=='rank':
            # Mid-ranks preserve ties; no labels determine these participant-specific thresholds.
            rank=(rankdata(logits[:,2]-logits[:,0],method='average')-.5)/len(indices)
            pred=np.where(rank<choice['low'],0,np.where(rank>choice['high'],2,1))
            result[indices]=np.eye(3)[pred]
        else:
            logits-=choice['strength']*logits.mean(axis=0)
            if choice['scale']: logits/=np.maximum(logits.std(axis=0),.05)
            p=np.exp(logits-logits.max(axis=1,keepdims=True)); result[indices]=p/p.sum(axis=1,keepdims=True)
    return result


def predict(bundle,frame):
    return adapt(frame,base_predict(bundle['base'],frame),bundle['choice'])
