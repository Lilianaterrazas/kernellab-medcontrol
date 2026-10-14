"""ACL e fila FIFO protegida por Lock para dispositivo compartilhado."""
from collections import deque
from threading import Lock, Thread
from time import sleep

DEVICES = ('disco', 'rede', 'audio', 'logs')
OPERATIONS = ('ler', 'gravar', 'executar', 'utilizar', 'exclusivo')

def access_matrix(processes):
    matrix = {}
    for p in processes:
        pid = p['id']
        matrix[pid] = {}
        for device in DEVICES:
            allowed = device in p['devices'] or device == 'logs'
            matrix[pid][device] = {
                'ler': allowed and device in ('disco','rede','logs'),
                'gravar': allowed and device in ('disco','rede','logs'),
                'executar': False,  # dispositivo nao executa codigo do processo
                'utilizar': allowed,
                'exclusivo': allowed and device in ('disco','audio')
            }
    return matrix

class DeviceQueue:
    """Fila FIFO serial: cada solicitacao ocupa dispositivo sob mutex."""
    def __init__(self, name):
        self.name = name
        self.pending = deque()
        self.mutex = Lock()
        self.events = []

    def submit(self, pid):
        self.pending.append(pid)

    def run(self):
        while self.pending:
            pid = self.pending.popleft()
            with self.mutex:
                self.events.append((pid, 'inicio'))
                self.events.append((pid, 'fim'))
        return self.events


def concurrent_demo():
    """Threads competem por um dispositivo; intervalos protegidos nao se sobrepoem."""
    lock = Lock()
    events = []
    def worker(pid):
        with lock:
            events.append((pid, 'inicio'))
            sleep(0.001)
            events.append((pid, 'fim'))
    threads = [Thread(target=worker, args=(p,)) for p in ('P3','P5','P6')]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    return events
