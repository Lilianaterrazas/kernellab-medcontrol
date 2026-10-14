"""Substituicao de paginas com frames inicialmente vazios."""
def simulate(pages, frames, algorithm):
    if frames < 1:
        raise ValueError('Frames deve ser >= 1')
    if algorithm not in ('FIFO', 'LRU', 'OPT'):
        raise ValueError('Algoritmo desconhecido')
    slots = [None] * frames
    fifo = []
    last_used = {}
    trace = []
    hits = 0
    for i, page in enumerate(pages):
        hit = page in slots
        if hit:
            hits += 1
        else:
            if None in slots:
                victim = slots.index(None)
            elif algorithm == 'FIFO':
                victim = slots.index(fifo.pop(0))
            elif algorithm == 'LRU':
                victim = min(range(frames), key=lambda j: last_used[slots[j]])
            else:
                def next_use(j):
                    try:
                        return pages.index(slots[j], i + 1)
                    except ValueError:
                        return float('inf')
                victim = max(range(frames), key=next_use)
            slots[victim] = page
            if algorithm == 'FIFO':
                fifo.append(page)
        last_used[page] = i
        trace.append({'reference': page, 'frames': slots.copy(), 'hit': hit})
    faults = len(pages) - hits
    return {'algorithm': algorithm, 'trace': trace, 'hits': hits, 'faults': faults,
            'fault_rate': faults / len(pages) if pages else 0}
