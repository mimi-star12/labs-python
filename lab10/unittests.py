import math
import unittest
from integrate import integrate
from threads import integrate_threads 
from processes import integrate_process

class TestIntegrate(unittest.TestCase):
    def test_known_integral(self):
        res = integrate(math.sin, 0, math.pi, n_iter=200_000)
        self.assertAlmostEqual(res, 2.0, places=2)
        res = integrate(lambda x: x * x, 0, 1, n_iter=200_000)
        self.assertAlmostEqual(res, 1.0 / 3.0, places=2)

class TestThreads(unittest.TestCase):
    def test_threads_close_to_base(self):
        base = integrate(math.sin, 0, math.pi, n_iter=200_000)
        thr = integrate_threads(math.sin, 0, math.pi, n_iter=200_000)
        self.assertAlmostEqual(thr, base, places=2)


class TestProcesses(unittest.TestCase):
    def test_processes_close_to_base(self):
        base = integrate(math.sin, 0, math.pi, n_iter=200_000)
        proc = integrate_process(math.sin, 0, math.pi, n_iter=200_000)
        self.assertAlmostEqual(proc, base, places=2)


if __name__ == '__main__':
  unittest.main()
