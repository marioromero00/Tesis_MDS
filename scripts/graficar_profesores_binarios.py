from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'resultados/profesor_binario_reconstruido_29-10-2026'
COLORS={'Dummy':'#888888','Logistica':'#1874b4','RandomForest':'#dd7c16','MLP_current':'#9270b2','TCN':'#169878','LSTM':'#cf4d70'}
def main():
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(2,2,figsize=(13,11),layout='constrained')
    for row,kind in enumerate(['igualitario','pca']):
        curves=pd.read_csv(OUT/kind/'curvas_roc.csv'); metrics=pd.read_csv(OUT/kind/'metricas.csv')
        for _,m in metrics.iterrows():
            mode=m['mode']; family=m.family; ax=axes[row,1 if mode=='history' else 0]
            name='MLP' if family=='MLP_current' else family
            if mode=='repeat_current':name+=' (control)'
            ax.plot(curves.fpr,curves[f'{family}_{mode}'],label=f'{name}: {m.auc_macro:.3f}',color=COLORS[family],lw=1.8)
        for col,title in enumerate(['Ventana actual','Historial causal (hasta 8 ventanas)']):
            ax=axes[row,col]; ax.plot([0,1],[0,1],'--',color='#999999',lw=1)
            ax.set(title=f"Profesor {kind.upper() if kind=='pca' else kind} · {title}",xlabel='Tasa de falsos positivos',ylabel='Sensibilidad',xlim=(0,1),ylim=(0,1))
            ax.grid(alpha=.15); ax.legend(loc='lower right',fontsize=8)
    fig.suptitle('Atención binaria reconstruida desde mirada y pupila\n1 = score sobre mediana personal · 0 = resto · ROC media por persona / leyenda AUC macro',fontsize=13)
    for ext in ['png','pdf']:fig.savefig(OUT/f'curvas_roc_profesores.{ext}',dpi=180)
    plt.close(fig)
if __name__=='__main__':main()
