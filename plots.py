"""Graficos comparativos salvos em PNG."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def make_plots(cpu, memory, out):
    out.mkdir(exist_ok=True, parents=True)
    labels = [r['algorithm'] for r in cpu]
    fig, ax = plt.subplots(figsize=(9,5))
    x = range(len(labels))
    for offset, key, title in ((-0.25,'waiting','Espera'),(0,'turnaround','Retorno'),(0.25,'response','Resposta')):
        ax.bar([i+offset for i in x], [r['averages'][key] for r in cpu], width=.24,label=title)
    ax.set_xticks(list(x),labels); ax.set_ylabel('Tempo medio (unidades)');ax.legend();fig.tight_layout();fig.savefig(out/'cpu_medias.png',dpi=160);plt.close(fig)
    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(labels,[r['context_switches'] for r in cpu]);ax.set_ylabel('Trocas de contexto');fig.tight_layout();fig.savefig(out/'trocas_contexto.png',dpi=160);plt.close(fig)
    fig, ax = plt.subplots(figsize=(8,4))
    mlabels = [r['algorithm'] for r in memory]
    ax.bar([i-.2 for i in range(3)],[r['hits'] for r in memory],width=.4,label='Hits')
    ax.bar([i+.2 for i in range(3)],[r['faults'] for r in memory],width=.4,label='Faults')
    ax.set_xticks(range(3),mlabels);ax.legend();fig.tight_layout();fig.savefig(out/'memoria_hits_faults.png',dpi=160);plt.close(fig)
    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(mlabels,[r['fault_rate']*100 for r in memory]);ax.set_ylabel('Taxa de faltas (%)');fig.tight_layout();fig.savefig(out/'taxa_faltas.png',dpi=160);plt.close(fig)
    for r in cpu:
        fig, ax = plt.subplots(figsize=(10,2.5))
        for pid,start,end in r['segments']:
            y = 0
            ax.broken_barh([(start,end-start)],(y,1),facecolors='lightgray',edgecolors='black')
            ax.text((start+end)/2,.5,pid,ha='center',va='center',fontsize=8)
        ax.set_xlim(0,max(e for _,_,e in r['segments']));ax.set_ylim(0,1);ax.set_yticks([]);ax.set_xlabel('Tempo');ax.set_title('Gantt - '+r['algorithm']);fig.tight_layout();fig.savefig(out/('gantt_'+r['algorithm'].lower()+'.png'),dpi=160);plt.close(fig)
