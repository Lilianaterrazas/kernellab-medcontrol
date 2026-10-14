"""Escalonadores deterministas de CPU unica; custo de troca de contexto = zero."""
from collections import deque


def schedule(processes, algorithm, quantum=3):
    if quantum <= 0:
        raise ValueError('Quantum deve ser positivo')
    ids = [p['id'] for p in processes]
    if len(ids) != len(set(ids)) or any(p['arrival'] < 0 or p['burst'] <= 0 for p in processes):
        raise ValueError('IDs devem ser unicos; chegada >= 0; burst > 0')
    pending = sorted((dict(p) for p in processes), key=lambda p: (p['arrival'], p['id']))
    by_id = {p['id']: p for p in pending}
    remaining = {p['id']: p['burst'] for p in pending}
    segments = []
    time = 0
    first = {}
    finish = {}
    ready = deque()
    index = 0

    def arrivals(now):
        nonlocal index
        while index < len(pending) and pending[index]['arrival'] <= now:
            ready.append(pending[index]['id'])
            index += 1

    while len(finish) < len(pending):
        arrivals(time)
        if not ready:
            nxt = pending[index]['arrival']
            segments.append(('IDLE', time, nxt))
            time = nxt
            arrivals(time)
        if algorithm == 'RR':
            pid = ready.popleft()
            duration = min(quantum, remaining[pid])
        elif algorithm in ('FCFS', 'SJF', 'PRIORITY'):
            if algorithm == 'FCFS':
                pid = ready.popleft()
            else:
                key = (lambda x: (by_id[x]['burst'], by_id[x]['arrival'], x)) if algorithm == 'SJF' else (lambda x: (by_id[x]['priority'], by_id[x]['arrival'], x))
                pid = min(ready, key=key)
                ready.remove(pid)
            duration = remaining[pid]
        else:
            raise ValueError('Algoritmo desconhecido')
        first.setdefault(pid, time)
        start = time
        time += duration
        remaining[pid] -= duration
        segments.append((pid, start, time))
        arrivals(time)  # chegadas durante quantum entram antes do processo preemptado
        if remaining[pid]:
            ready.append(pid)
        else:
            finish[pid] = time
    stats = {}
    for pid, p in by_id.items():
        turnaround = finish[pid] - p['arrival']
        stats[pid] = {'waiting': turnaround - p['burst'], 'turnaround': turnaround,
                      'response': first[pid] - p['arrival'], 'completion': finish[pid]}
    from .metrics import summarize
    return {'algorithm': algorithm, 'segments': segments, 'stats': stats, **summarize(segments, stats)}
