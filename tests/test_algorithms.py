import unittest
from src.schedulers import schedule
from src.memory import simulate
from src.devices import access_matrix, concurrent_demo

P = [{'id':'P1','arrival':0,'burst':5,'priority':2,'devices':['rede']},
     {'id':'P2','arrival':1,'burst':2,'priority':0,'devices':['disco']}]

class TestKernelLab(unittest.TestCase):
    def test_fcfs(self):
        r = schedule(P,'FCFS')
        self.assertEqual(r['execution_order'], ['P1','P2'])
        self.assertEqual(r['stats']['P2']['waiting'],4)
    def test_sjf(self):
        self.assertEqual(schedule(P,'SJF')['execution_order'], ['P1','P2'])
    def test_priority(self):
        self.assertEqual(schedule(P,'PRIORITY')['execution_order'], ['P1','P2'])
    def test_rr(self):
        self.assertEqual(schedule(P,'RR',3)['execution_order'], ['P1','P2','P1'])
    def test_memory(self):
        self.assertEqual(simulate([1,2,1,3],2,'FIFO')['faults'],3)
        self.assertEqual(simulate([1,2,1,3],2,'LRU')['hits'],1)
        self.assertEqual(simulate([1,2,1,3],2,'OPT')['faults'],3)
    def test_acl(self):
        self.assertTrue(access_matrix(P)['P2']['disco']['exclusivo'])
        self.assertFalse(access_matrix(P)['P1']['disco']['utilizar'])
    def test_mutex(self):
        events = concurrent_demo()
        self.assertEqual([e[1] for e in events], ['inicio','fim']*3)
    def test_invalid(self):
        with self.assertRaises(ValueError): schedule(P,'RR',0)
        with self.assertRaises(ValueError): simulate([1],0,'FIFO')

if __name__ == '__main__': unittest.main()
