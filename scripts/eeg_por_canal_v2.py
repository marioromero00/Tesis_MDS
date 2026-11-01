"""EEG espacial/espectral por canal sobre las ventanas originales, solo train."""
from __future__ import annotations
import argparse,json,time,zipfile,hashlib
from pathlib import Path
import numpy as np,pandas as pd
from scipy.signal import welch,detrend,butter,sosfiltfilt,iirnotch,filtfilt
from preprocesamiento_secuencial import read_eeg_entry,eeg_features,sha256_file
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'../../datos/locales/v2_2025/eeg_recordings_exp_V2.zip'
OUT=ROOT/'resultados/eeg_por_canal_v2_29-10-2026'
FS=125.; BANDS={'delta':(1,4),'theta':(4,8),'alpha':(8,13),'beta':(13,30),'gamma':(30,45)}
CHANNEL_FIELDS=['finite_fraction','rail_fraction','flat_fraction','usable','log_variance','log_peak_to_peak','hjorth_mobility','hjorth_complexity','spectral_entropy','spectral_mean_hz','spectral_edge95_hz']+[f'logpower_{b}' for b in BANDS]+[f'relative_{b}' for b in BANDS]
FEATURES=[f'eegch{c:02d}_{k}' for c in range(16) for k in CHANNEL_FIELDS]+['eegsp_n_samples','eegsp_coverage','eegsp_max_gap_s','eegsp_usable_channels','eegsp_mean_abs_correlation','eegsp_dominant_covariance_fraction']
SOS=butter(4,[1,45],btype='bandpass',fs=FS,output='sos');NOTCH=iirnotch(50,30,fs=FS)

def extract_window(signal,max_gap_s=0.):
    out={k:np.nan for k in FEATURES};n=len(signal)
    out.update(eegsp_n_samples=n,eegsp_coverage=min(1,n/250),eegsp_max_gap_s=max_gap_s,eegsp_usable_channels=0)
    if not n:return out
    x=np.asarray(signal,float);finite=np.isfinite(x).mean(axis=0);rail=(np.abs(x)>=180000).mean(axis=0)
    flat=(np.abs(np.diff(x,axis=0))<1e-12).mean(axis=0) if n>1 else np.ones(16)
    usable=(finite>=.95)&(rail<=.01)&(flat<.99)&(n>=200)&(max_gap_s<=.1)
    clean=x.copy()
    for c in range(16):
        for k,v in [('finite_fraction',finite[c]),('rail_fraction',rail[c]),('flat_fraction',flat[c]),('usable',int(usable[c]))]:out[f'eegch{c:02d}_{k}']=float(v)
        if finite[c]<1:
            ok=np.isfinite(clean[:,c])
            clean[:,c]=np.interp(np.arange(n),np.flatnonzero(ok),clean[ok,c]) if ok.any() else 0.
    if not usable.any():return out
    clean=detrend(clean,axis=0,type='linear');clean=filtfilt(*NOTCH,clean,axis=0);clean=sosfiltfilt(SOS,clean,axis=0)
    f,psd=welch(clean,fs=FS,nperseg=125,noverlap=62,nfft=256,detrend='constant',scaling='density',axis=0)
    mask=(f>=1)&(f<45);s=psd[mask];freq=f[mask];total=s.sum(axis=0)
    prob=s/np.maximum(total,1e-30);entropy=-(prob*np.log(np.maximum(prob,1e-30))).sum(axis=0)/np.log(len(freq))
    d1=np.diff(clean,axis=0)*FS;d2=np.diff(d1,axis=0)*FS
    variance=np.var(clean,axis=0);var1=np.var(d1,axis=0);var2=np.var(d2,axis=0)
    mobility=np.sqrt(var1/np.maximum(variance,1e-30));complexity=np.sqrt(var2/np.maximum(var1,1e-30))/np.maximum(mobility,1e-30)
    power={band:psd[(f>=a)&(f<b)].sum(axis=0) for band,(a,b) in BANDS.items()}
    for c in np.flatnonzero(usable):
        values={'log_variance':np.log10(max(variance[c],1e-12)),'log_peak_to_peak':np.log1p(np.ptp(clean[:,c])),
            'hjorth_mobility':mobility[c],'hjorth_complexity':complexity[c],'spectral_entropy':entropy[c],
            'spectral_mean_hz':(prob[:,c]*freq).sum(),'spectral_edge95_hz':freq[min(np.searchsorted(np.cumsum(prob[:,c]),.95),len(freq)-1)]}
        for band in BANDS:
            values[f'logpower_{band}']=np.log10(max(power[band][c]*(f[1]-f[0]),1e-12))
            values[f'relative_{band}']=power[band][c]/max(total[c],1e-30)
        for k,v in values.items():out[f'eegch{c:02d}_{k}']=float(v)
    out['eegsp_usable_channels']=int(usable.sum())
    if usable.sum()>=2:
        corr=np.nan_to_num(np.corrcoef(clean[:,usable],rowvar=False));upper=np.abs(corr[np.triu_indices(len(corr),1)])
        ev=np.linalg.eigvalsh(corr).clip(min=0)
        out['eegsp_mean_abs_correlation']=float(upper.mean());out['eegsp_dominant_covariance_fraction']=float(ev[-1]/max(ev.sum(),1e-30))
    return out

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--raw',default=str(RAW.resolve()));args=parser.parse_args();raw=Path(args.raw)
    expected=json.loads((ROOT/'resultados/preprocesamiento/manifiesto_ejecucion.json').read_text())['inputs']['eeg_zip']
    if raw.stat().st_size!=expected['bytes'] or sha256_file(raw)!=expected['sha256']:raise ValueError('El ZIP crudo no coincide con el manifiesto')
    source=ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv';partition=ROOT/'resultados/modelado/particion_participantes.csv'
    frame=pd.read_csv(source);frame['source_row']=np.arange(len(frame));split=pd.read_csv(partition).set_index('participant').split;frame['split']=frame.participant.map(split)
    train=frame[frame.split.eq('train')].copy();mapping=pd.read_csv(ROOT/'resultados/sincronizacion/coordinacion_sesiones.csv').set_index('participant')
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'participantes').mkdir(exist_ok=True)
    protocol={'raw_zip_sha256':expected['sha256'],'source_sha256':sha256_file(source),'partition_sha256':sha256_file(partition),'code_sha256':sha256_file(Path(__file__)),
        'teacher_labels_changed':False,'train_only':True,'expected_rows':13524,'expected_people':25,'features':FEATURES,'fs':FS,'window_seconds':2,'welch':{'nperseg':125,'noverlap':62,'nfft':256},
        'filter':{'detrend':'linear within current window','notch_hz':50,'notch_Q':30,'bandpass_hz':[1,45],'bandpass_order':4,'phase':'forward-backward within current window only'},
        'quality':{'minimum_samples':200,'minimum_finite_fraction':.95,'maximum_rail_fraction':.01,'rail_microvolts':180000,'maximum_flat_fraction':.99,'maximum_sample_gap_s':.1},
        'missing_channel_handling':'missing features; no windows removed; imputation only inside model training folds','validation_evaluated':False,'test_evaluated':False}
    path=OUT/'protocolo.json'
    if path.exists():assert json.loads(path.read_text())==protocol,'Protocolo cambiado'
    else:path.write_text(json.dumps(protocol,indent=2))
    allrows=[];checks=[];started=time.monotonic()
    with zipfile.ZipFile(raw) as archive:
        for person,windows in train.groupby('participant',sort=True):
            dest=OUT/'participantes'/f'{person}.csv.gz';audit=OUT/'participantes'/f'{person}.json'
            if dest.exists() and audit.exists():
                record=json.loads(audit.read_text());assert sha256_file(dest)==record['features_sha256'];allrows.append(pd.read_csv(dest));checks+=record['legacy_checks'];continue
            info=mapping.loc[person];timestamps,signal=read_eeg_entry(archive,info.eeg_file,16)
            finite=np.isfinite(timestamps);timestamps,signal=timestamps[finite],signal[finite]
            order=np.argsort(timestamps,kind='stable');timestamps,signal=timestamps[order],signal[order]
            rows=[];qa=[];sample_indices=set(np.linspace(0,len(windows)-1,10,dtype=int))
            for i,row in enumerate(windows.itertuples(index=False)):
                start=pd.Timestamp(row.window_start_utc).timestamp();end=pd.Timestamp(row.window_end_utc).timestamp();lo,hi=np.searchsorted(timestamps,[start,end],side='left')
                ts=timestamps[lo:hi];x=signal[lo:hi];gap=float(np.diff(ts).max()) if len(ts)>1 else 2.
                # Preserve exactly the old UTC selection; no synchronization offsets are added.
                assert len(x)==int(row.eeg_n),f'Cobertura EEG distinta {person}, fila {row.source_row}'
                if i in sample_indices:
                    old=eeg_features(x,FS,BANDS)
                    for key in ['eeg_rms_uv','eeg_std_uv','eeg_alpha_relative']:
                        np.testing.assert_allclose(old[key],getattr(row,key),rtol=2e-6,atol=1e-8,equal_nan=True)
                    qa.append({'source_row':int(row.source_row),'legacy_selection_and_features_match':True})
                values=extract_window(x,gap)
                rows.append({'source_row':row.source_row,'participant':person,'window_start_utc':row.window_start_utc,**values})
            table=pd.DataFrame(rows);table.to_csv(dest,index=False)
            record={'participant':person,'raw_member':info.eeg_file,'rows':len(table),'features_sha256':sha256_file(dest),'legacy_checks':qa};audit.write_text(json.dumps(record,indent=2))
            allrows.append(table);checks+=qa
            print(person,len(table),'ventanas',round(time.monotonic()-started,1),'s',flush=True)
    result=pd.concat(allrows,ignore_index=True)
    assert len(result)==13524 and result.participant.nunique()==25 and not result.source_row.duplicated().any()
    result.to_csv(OUT/'caracteristicas_eeg_por_canal.csv.gz',index=False)
    (OUT/'verificacion.json').write_text(json.dumps({'passed':True,'rows':len(result),'participants':25,'features':len(FEATURES),'legacy_checks':len(checks),'feature_file_sha256':sha256_file(OUT/'caracteristicas_eeg_por_canal.csv.gz'),'rows_removed':0},indent=2))
    print('EEG por canal completo',flush=True)
if __name__=='__main__':main()
