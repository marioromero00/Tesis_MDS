"""Genera figuras exportables a partir del analisis de variables, sin nuevos ajustes."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'resultados/analisis_variables_07-09-2026'


def main():
    data = pd.read_csv(OUTPUT / 'importancia_validacion.csv')
    plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False})
    for task, title in [('attention_primary', 'Atención'), ('arousal_primary_6s', 'Activación')]:
        fig, axes = plt.subplots(2, 2, figsize=(14, 9), layout='constrained')
        for row, kind in enumerate(['classification', 'regression']):
            for col, name in enumerate(['logistic' if row == 0 else 'ridge', 'random_forest']):
                ax = axes[row, col]
                part = data.loc[data.task.eq(task) & data.kind.eq(kind) & data.model.eq(name)
                                & ~data.feature.str.startswith('modalidad:')].nlargest(8, 'importance').sort_values('importance')
                y = np.arange(len(part))
                ax.hlines(y, part.bootstrap_low, part.bootstrap_high, color='#64748b', lw=2)
                ax.scatter(part.importance, y, color='#154d71', zorder=3)
                ax.set_yticks(y, part.feature)
                ax.axvline(0, color='#aa4444', lw=1, linestyle='--')
                ax.set_title(f'{name} · {"clasificación" if row == 0 else "regresión"}')
                ax.set_xlabel('Caída de balanced accuracy (macro participante)' if row == 0 else 'Aumento del MSE (macro participante)')
                ax.grid(axis='x', alpha=.2)
        fig.suptitle(f'{title}: 8 mayores importancias por modelo en validación\n'
                     'Desplazamientos dentro de segmento; intervalos bootstrap exploratorios de 8 participantes', fontsize=13)
        fig.savefig(OUTPUT / f'importancia_{task}.png', dpi=180)
        fig.savefig(OUTPUT / f'importancia_{task}.pdf')
        plt.close(fig)
    comparisons = pd.read_csv(OUTPUT / 'comparacion_subconjuntos.csv')
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), layout='constrained')
    for ax, (task, title) in zip(axes, [('attention_primary', 'Atención'), ('arousal_primary_6s', 'Activación')]):
        part = comparisons.loc[comparisons.task.eq(task) & comparisons.kind.eq('classification')]
        order = part.subset.drop_duplicates().tolist()
        for offset, name, color in [(-.12, 'logistic', '#154d71'), (.12, 'random_forest', '#c36b21')]:
            group = part.loc[part.model.eq(name)].set_index('subset').loc[order]
            ax.scatter(group.balanced_accuracy, np.arange(len(order)) + offset, label=name, color=color)
        ax.axvline(1/3, ls='--', color='#777777', label='Referencia 1/3')
        ax.set_yticks(np.arange(len(order)), order)
        ax.set_xlabel('Balanced accuracy global en validación')
        ax.set_title(title)
        ax.grid(axis='x', alpha=.2)
        ax.legend(fontsize=8)
    fig.suptitle('Comparación exploratoria de subconjuntos · top-k elegido con train')
    fig.savefig(OUTPUT / 'comparacion_subconjuntos.png', dpi=180)
    fig.savefig(OUTPUT / 'comparacion_subconjuntos.pdf')


if __name__ == '__main__':
    main()
