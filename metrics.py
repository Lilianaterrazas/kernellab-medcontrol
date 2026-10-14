"""Metricas classicas de escalonamento."""
def summarize(segments, stats):
    n = len(stats)
    real = [s[0] for s in segments if s[0] != 'IDLE']
    switches = sum(a != b for a, b in zip(real, real[1:]))
    return {'averages': {k: sum(s[k] for s in stats.values()) / n for k in ('waiting','turnaround','response')},
            'context_switches': switches,
            'execution_order': real}
