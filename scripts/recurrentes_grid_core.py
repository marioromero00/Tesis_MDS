"""Grillas BiLSTM, LSTM y TCN sobre historia disponible hasta el endpoint."""
from itertools import product
import numpy as np
import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence
from temporales_core import CausalBlock
import os

FAMILIES = ['BiLSTM', 'LSTM', 'TCN']
FAMILY = os.environ.get('MDS_GRID_FAMILY', 'BiLSTM')
if FAMILY not in FAMILIES: raise ValueError(FAMILY)
from temporales_core import preprocessor, seed_all, raw_predict
from redes_secuencia_13 import sequences
from hiperparametros_core import FULL, TARGET
from avanzados_core import sample_weights
from optimizar_historial import smooth


def grid(family=None):
    family = family or FAMILY
    if family not in FAMILIES: raise ValueError(family)
    return [dict(id=f'g{i:02d}',context=c,hidden=h,layers=l,lr=lr,dropout=d,
                 family=family,decay=.01,batch=256)
            for i,(c,h,l,lr,d) in enumerate(product([8,32],[16,32],[1,2],[.0003,.001],[.1,.4]))]


class GridSequenceNet(nn.Module):
    def __init__(self, inputs, config):
        super().__init__()
        self.family=config['family']; h=config['hidden']; d=config['dropout']
        if self.family in ['BiLSTM','LSTM']:
            self.body=nn.LSTM(inputs,h,num_layers=config['layers'],batch_first=True,
                bidirectional=self.family=='BiLSTM',dropout=d if config['layers']>1 else 0.)
            width=h*(2 if self.family=='BiLSTM' else 1)
        elif self.family=='TCN':
            dilations=[1,2] if config['layers']==1 else [1,2,4,8]
            self.body=nn.Sequential(*[CausalBlock(inputs if i==0 else h,h,dilation,d)
                                      for i,dilation in enumerate(dilations)])
            width=h
        else: raise ValueError(self.family)
        self.head=nn.Sequential(nn.Dropout(d),nn.Linear(width,3))

    def forward(self,x,lengths):
        if self.family in ['BiLSTM','LSTM']:
            packed=pack_padded_sequence(x,lengths.cpu(),batch_first=True,enforce_sorted=False)
            _,(h,_)=self.body(packed)
            z=torch.cat([h[-2],h[-1]],dim=1) if self.family=='BiLSTM' else h[-1]
        else:
            z=self.body(x.transpose(1,2)).transpose(1,2)[torch.arange(len(x)),lengths-1]
        return self.head(z)


def predict(b,frame):
    # Evaluation/checkpoint serialization must not alter subsequent optimization RNG.
    with torch.random.fork_rng(devices=[]):
        net=GridSequenceNet(b['input_features'],b['config']); net.load_state_dict(b['state']); net.eval()
        x,lengths=sequences(b['prep'],frame,b['config'],b['repeat'])
        raw=raw_predict(net,x,lengths,batch=256)
        return smooth(frame,torch.softmax(torch.from_numpy(raw),dim=1).numpy(),b['smoothing'])


def train(frame,config,seed,epochs,callback=None,repeat=False):
    seed_all(seed); torch.set_num_threads(2)
    prep=preprocessor().fit(frame[FULL]); x,lengths=sequences(prep,frame,config,repeat)
    net=GridSequenceNet(x.shape[2],config)
    xx=torch.from_numpy(x); ll=torch.from_numpy(lengths)
    yy=torch.tensor(frame[TARGET].map({'bajo':0,'medio':1,'alto':2}).to_numpy(),dtype=torch.long)
    weights=torch.tensor(sample_weights(frame,'participant'),dtype=torch.float32)
    optimizer=torch.optim.AdamW(net.parameters(),lr=config['lr'],weight_decay=config['decay'])
    curve=[]
    def bundle(epoch):
        return dict(state={k:v.detach().clone() for k,v in net.state_dict().items()},prep=prep,
                    config=config,seed=seed,epoch=epoch,repeat=repeat,smoothing=1,
                    input_features=x.shape[2],features=FULL)
    for epoch in range(1,epochs+1):
        net.train(); order=torch.randperm(len(frame)); total=0.
        for start in range(0,len(frame),config['batch']):
            ix=order[start:start+config['batch']]; optimizer.zero_grad(set_to_none=True)
            loss=(nn.functional.cross_entropy(net(xx[ix],ll[ix]),yy[ix],reduction='none')*weights[ix]).mean()
            if not torch.isfinite(loss): raise ValueError('Nonfinite loss')
            loss.backward(); nn.utils.clip_grad_norm_(net.parameters(),1.); optimizer.step()
            total+=loss.item()*len(ix)
        curve.append(dict(epoch=epoch,loss=total/len(frame)))
        if callback is not None:
            with torch.random.fork_rng(devices=[]): callback(epoch,bundle(epoch),curve)
    return bundle(epochs),curve
