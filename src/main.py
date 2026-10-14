"""CLI do KernelLab: python -m src.main --help."""
import argparse
import json
from pathlib import Path
from .schedulers import schedule
from .memory import simulate
from .devices import access_matrix, DeviceQueue, concurrent_demo


def table(headers, rows):
    widths = [max(len(str(x)) for x in [h] + [r[i] for r in rows]) for i,h in enumerate(headers)]
    print(' | '.join(str(h).ljust(widths[i]) for i,h in enumerate(headers)))
    print('-+-'.join('-'*w for w in widths))
    for r in rows:
        print(' | '.join(str(x).ljust(widths[i]) for i,x in enumerate(r)))


def main():
    parser = argparse.ArgumentParser(description='KernelLab - simulador de sistemas operacionais')
    parser.add_argument('--input', default=str(Path(__file__).resolve().parents[1] / 'data' / 'processes.json'))
    parser.add_argument('--quantum', type=int, default=None)
    parser.add_argument('--frames', type=int, default=None)
    parser.add_argument('--pages', help='Sequencia separada por virgulas: 1,2,3')
    parser.add_argument('--plots', action='store_true', help='Salva graficos PNG em docs/')
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding='utf-8'))
    quantum = args.quantum if args.quantum is not None else data['quantum']
    frames = args.frames if args.frames is not None else data['frames']
    pages = [int(x.strip()) for x in args.pages.split(',')] if args.pages else data['pages']
    results = [schedule(data['processes'], a, quantum) for a in ('FCFS','SJF','RR','PRIORITY')]
    mem = [simulate(pages, frames, a) for a in ('FIFO','LRU','OPT')]
    for result in results:
        print('\n###', result['algorithm'], '###')
        print('Gantt:', ' | '.join(f'{p}[{s}-{e}]' for p,s,e in result['segments']))
        table(['PID','Espera','Retorno','Resposta','Conclusao'], [(p, *[v[k] for k in ('waiting','turnaround','response','completion')]) for p,v in result['stats'].items()])
        print('Medias:', {k: round(v, 3) for k,v in result['averages'].items()}, 'Trocas:', result['context_switches'])
    print('\n### Comparacao de CPU ###')
    table(['Algoritmo','Espera media','Retorno medio','Resposta media','Trocas'], [(r['algorithm'],*[f'{r["averages"][k]:.2f}' for k in ('waiting','turnaround','response')],r['context_switches']) for r in results])
    for r in mem:
        print('\n### Memoria', r['algorithm'], '###')
        table(['Ref','Frames','Resultado'], [(x['reference'],str(x['frames']),'HIT' if x['hit'] else 'FAULT') for x in r['trace']])
        print('Hits:',r['hits'],'Faults:',r['faults'],'Taxa:',f'{r["fault_rate"]:.2%}')
    print('\n### Matriz de acesso (L=ler, G=gravar, E=executar, U=utilizar, X=exclusivo) ###')
    acl = access_matrix(data['processes'])
    table(['Processo']+list(next(iter(acl.values())).keys()), [(pid, *[''.join(k for k,v in zip('LGEUX',ops.values()) if v) or '-' for ops in devices.values()]) for pid,devices in acl.items()])
    q = DeviceQueue('disco')
    for pid in ('P3','P5','P6'): q.submit(pid)
    print('Fila de disco:',q.run())
    print('Mutex concorrente:',concurrent_demo())
    print('\nAlerta P4 - inicio:',{r['algorithm']:r['stats']['P4']['response'] for r in results})
    if args.plots:
        from .plots import make_plots
        out = Path(__file__).resolve().parents[1] / 'docs'
        make_plots(results,mem,out)
        print('Graficos salvos em',out)

if __name__ == '__main__':
    main()
