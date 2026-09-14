"""Grilla cartesiana Transformer con checkpoints que preservan el RNG."""
from itertools import product
import numpy as np
import torch
from torch import nn
from temporales_core import preprocessor, seed_all, raw_predict
from redes_secuencia_13 import sequences
from hiperparametros_core import FULL, TARGET
from avanzados_core import sample_weights
from optimizar_historial import smooth


def grid():
    return [dict(id=f'g{i:02d}',context=c,hidden=h,layers=l,lr=lr,dropout=d,
                 heads=4,ff_multiplier=2,decay=.01,batch=256)
            for i,(c,h,l,lr,d) in enumerate(product([8,32],[16,32],[1,2],[.0003,.001],[.1,.4]))]


class GridTransformer(nn.Module):
    def __init__(self, inputs, config):
        super().__init__(); h=config['hidden']
        self.project=nn.Linear(inputs,h)
        self.position=nn.Parameter(torch.randn(1,config['context'],h)*.02)
        # Independent initialization of layers rather than cloned identical weights.
        self.layers=nn.ModuleList([nn.TransformerEncoderLayer(h,config['heads'],h*config['ff_multiplier'],
            config['dropout'],batch_first=True,norm_first=True) for _ in range(config['layers'])])
        self.norm=nn.LayerNorm(h); self.head=nn.Linear(h,3)

    def forward(self,x,lengths):
        padding=torch.arange(x.shape[1])[None,:]>=lengths[:,None]
        mask=torch.ones(x.shape[1],x.shape[1],dtype=torch.bool).triu(1)
        z=self.project(x)+self.position[:,:x.shape[1]]
        for layer in self.layers: z=layer(z,src_mask=mask,src_key_padding_mask=padding)
        return self.head(self.norm(z)[torch.arange(len(x)),lengths-1])


def predict(b,frame):
    # Evaluation/checkpoint serialization must not alter subsequent optimization RNG.
    with torch.random.fork_rng(devices=[]):
        net=GridTransformer(b['input_features'],b['config']); net.load_state_dict(b['state']); net.eval()
        x,lengths=sequences(b['prep'],frame,b['config'],b['repeat'])
        raw=raw_predict(net,x,lengths,batch=256)
        return smooth(frame,torch.softmax(torch.from_numpy(raw),dim=1).numpy(),b['smoothing'])


def train(frame,config,seed,epochs,callback=None,repeat=False):
    seed_all(seed); torch.set_num_threads(2)
    prep=preprocessor().fit(frame[FULL]); x,lengths=sequences(prep,frame,config,repeat)
    net=GridTransformer(x.shape[2],config)
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
