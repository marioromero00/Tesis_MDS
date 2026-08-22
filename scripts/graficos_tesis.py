#!/usr/bin/env python3
"""Genera figuras de calidad editorial a partir de las salidas EDA existentes."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as mticker
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parent.parent
EDA = ROOT / "resultados" / "eda"
OUT = ROOT / "resultados" / "figuras_tesis"
OUT.mkdir(parents=True, exist_ok=True)

COLORS = {"blue":"#2463A6", "teal":"#168A8A", "gold":"#D89C27",
          "red":"#C84A43", "green":"#3A8D5D", "gray":"#667085", "light":"#E8EEF5"}

mpl.rcParams.update({
    "font.family":"DejaVu Sans", "font.size":10.5, "axes.titlesize":13,
    "axes.labelsize":11, "figure.titlesize":16, "axes.spines.top":False,
    "axes.spines.right":False, "axes.grid":True, "grid.alpha":.20,
    "grid.linewidth":.7, "axes.axisbelow":True, "savefig.facecolor":"white",
})

def save(fig, name):
    fig.savefig(OUT/f"{name}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

def pct_label(ax, bars, values):
    for bar, value in zip(bars, values):
        ax.text(bar.get_width()+1, bar.get_y()+bar.get_height()/2,
                f"{value:.2f}%".replace(".",","), va="center", weight="bold")

def overall_quality():
    names=["EEG","GSR","Pupilometría","Eye tracking"]
    eeg=pd.read_csv(EDA/"eeg"/"eeg_resumen_sesiones.csv")
    eeg=eeg[eeg.kind.eq("principal")]
    eeg_pct=100*eeg.quality.eq("utilizable").mean()
    vals=[eeg_pct,95.92,90.25,94.98]
    fig,ax=plt.subplots(figsize=(8.2,4.7))
    bars=ax.barh(names[::-1],vals[::-1],color=[COLORS["blue"],COLORS["gold"],COLORS["teal"],COLORS["green"]][::-1],height=.58)
    ax.set_xlim(0,105); ax.set_xlabel("Señal utilizable o válida (%)")
    fig.subplots_adjust(top=.82)
    fig.suptitle("Disponibilidad y calidad de las señales multimodales",x=.125,y=.97,ha="left",weight="bold")
    fig.text(.125,.885,"Criterios específicos por modalidad; EEG considera solo sesiones principales",
             color=COLORS["gray"],fontsize=9)
    pct_label(ax,bars,vals[::-1]); ax.axvline(90,color=COLORS["gray"],ls="--",lw=1)
    ax.text(90.5,-.62,"90%",color=COLORS["gray"],fontsize=8)
    save(fig,"01_resumen_calidad_modalidades")

def eeg_quality():
    df=pd.read_csv(EDA/"eeg"/"eeg_resumen_sesiones.csv")
    df=df[df.kind.eq("principal")].sort_values("rail_pct")
    colors=np.where(df.quality.eq("excluir"),COLORS["red"],COLORS["blue"])
    fig,ax=plt.subplots(figsize=(9.5,10.8))
    y=np.arange(len(df)); ax.barh(y,df.rail_pct,color=colors,height=.72)
    ax.set_yticks(y,df.participant); ax.set_xlabel("Muestras en saturación (rail) [%]")
    fig.subplots_adjust(top=.91)
    fig.suptitle("Calidad EEG por participante",x=.09,y=.98,ha="left",weight="bold")
    fig.text(.09,.945,"Sesiones principales · Línea roja: umbral flexible de exclusión (30%)",
             color=COLORS["gray"],fontsize=9)
    ax.axvline(30,color=COLORS["red"],ls="--",lw=1.5,label="Umbral 30%")
    ax.legend(frameon=False,loc="lower right")
    for yi,v,q in zip(y,df.rail_pct,df.quality):
        if q=="excluir": ax.text(v+.7,yi,f"{v:.1f}%",va="center",fontsize=8,color=COLORS["red"],weight="bold")
    save(fig,"02_eeg_saturacion_participantes")

    fig,axs=plt.subplots(1,2,figsize=(12,4.8),gridspec_kw={"width_ratios":[1.15,1]})
    axs[0].hist(df.effective_hz.dropna(),bins=14,color=COLORS["blue"],edgecolor="white")
    axs[0].axvline(125,color=COLORS["red"],ls="--",label="Nominal: 125 Hz")
    axs[0].set(xlabel="Frecuencia efectiva (Hz)",ylabel="Sesiones",title="Frecuencia de muestreo")
    axs[0].xaxis.set_major_locator(mticker.MaxNLocator(nbins=5))
    axs[0].xaxis.set_major_formatter(mticker.FormatStrFormatter("%.3f"))
    axs[0].tick_params(axis="x",labelsize=9)
    axs[0].legend(frameon=False)
    counts=df.quality.value_counts().reindex(["utilizable","excluir"],fill_value=0)
    wedges,texts,autotexts=axs[1].pie(counts,labels=["Utilizable","Excluir"],autopct=lambda p:f"{p:.1f}%".replace(".",","),
        colors=[COLORS["green"],COLORS["red"]],startangle=90,wedgeprops={"width":.55,"edgecolor":"white"},
        textprops={"fontsize":11},pctdistance=.72,labeldistance=1.08)
    for text in autotexts:
        text.set_color("white"); text.set_weight("bold"); text.set_fontsize(12)
    axs[1].text(0,0,"48\nsesiones",ha="center",va="center",fontsize=13,weight="bold",color=COLORS["gray"])
    axs[1].set_title("Clasificación flexible (n=48)")
    fig.subplots_adjust(top=.80,wspace=.28,bottom=.18)
    fig.suptitle("Resumen exploratorio de EEG",x=.06,y=.97,ha="left",weight="bold")
    save(fig,"03_eeg_resumen_calidad")

def gsr_quality():
    df=pd.read_csv(EDA/"gsr"/"gsr_por_grabacion.csv")
    fig,axs=plt.subplots(1,3,figsize=(13,4.3))
    axs[0].hist(df.sampling_hz_est,bins=12,color=COLORS["teal"],edgecolor="white")
    axs[0].axvline(df.sampling_hz_est.median(),color=COLORS["red"],ls="--")
    axs[0].set(xlabel="Frecuencia efectiva (Hz)",ylabel="Grabaciones",title="Muestreo GSR")
    axs[1].boxplot(df.n_valid,orientation="vertical",patch_artist=True,boxprops={"facecolor":COLORS["light"]},medianprops={"color":COLORS["red"],"linewidth":2})
    axs[1].set(xticks=[1],xticklabels=["GSR"],ylabel="Muestras válidas",title="Disponibilidad por grabación")
    axs[2].scatter(df.median_approx,df.iqr_approx,s=38,c=COLORS["gold"],alpha=.8,edgecolor="white")
    axs[2].set(xlabel="Mediana GSR",ylabel="Rango intercuartílico",title="Nivel y variabilidad")
    fig.subplots_adjust(top=.78,wspace=.32)
    fig.suptitle("EDA de respuesta galvánica de la piel",x=.055,y=.97,ha="left",weight="bold")
    fig.text(.055,.89,"47 grabaciones con señal válida; P7 y P42 sin GSR",color=COLORS["gray"],fontsize=9)
    save(fig,"04_gsr_resumen")

def eye_pupil_quality():
    df=pd.read_csv(EDA/"eye_pupil"/"calidad_por_participante.csv")
    order=df.assign(num=pd.to_numeric(df.participant.str.extract(r"(\d+)")[0],errors="coerce")).sort_values("num")
    cols=["gaze_valid_pct","pupil_left_valid_pct","pupil_right_valid_pct","both_eyes_valid_pct"]
    labels=["Mirada","Pupila izq.","Pupila der.","Ambos ojos"]
    data=order[cols].to_numpy().T
    cmap=LinearSegmentedColormap.from_list("quality",[COLORS["red"],COLORS["gold"],"#F5F7FA",COLORS["green"]])
    fig,ax=plt.subplots(figsize=(13,4.2))
    im=ax.imshow(data,aspect="auto",vmin=60,vmax=100,cmap=cmap)
    ax.set_yticks(range(4),labels); ax.set_xticks(range(len(order)),order.participant,rotation=90,fontsize=7)
    ax.grid(False); ax.set_title("Validez ocular por participante",loc="left",weight="bold")
    cbar=fig.colorbar(im,ax=ax,pad=.015); cbar.set_label("Muestras válidas (%)")
    save(fig,"05_eye_pupil_validez_participantes")

    movements=pd.read_csv(EDA/"eye_pupil"/"movimientos_oculares.csv")
    fix=pd.read_csv(EDA/"eye_pupil"/"fijaciones_unicas.csv")
    fig,axs=plt.subplots(1,2,figsize=(11,4.6))
    palette=[COLORS["blue"],COLORS["gold"],COLORS["red"],COLORS["gray"]]
    total=movements.rows.sum(); vals=100*movements.rows/total
    bars=axs[0].bar(movements.eye_movement_type,vals,color=palette[:len(movements)])
    axs[0].set(ylabel="Proporción de muestras (%)",title="Clasificación de movimiento ocular")
    axs[0].tick_params(axis="x",rotation=20)
    for b,v in zip(bars,vals): axs[0].text(b.get_x()+b.get_width()/2,v+.8,f"{v:.1f}%".replace(".",","),ha="center",fontsize=9)
    d=fix["Gaze event duration"].dropna(); d=d[d<=d.quantile(.99)]
    axs[1].hist(d,bins=35,color=COLORS["teal"],edgecolor="white")
    axs[1].axvline(d.median(),color=COLORS["red"],ls="--",label=f"Mediana: {d.median():.0f} ms")
    axs[1].set(xlabel="Duración de fijación (ms)",ylabel="Fijaciones",title="Distribución de fijaciones (≤p99)")
    axs[1].legend(frameon=False)
    fig.suptitle("EDA de eye tracking",x=.06,ha="left",weight="bold")
    save(fig,"06_eye_tracking_movimientos_fijaciones")

def main():
    overall_quality(); eeg_quality(); gsr_quality(); eye_pupil_quality()
    print(f"Figuras creadas en {OUT}")

if __name__=="__main__": main()
