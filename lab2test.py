import unittest

import lab2

class testsmth(unittest.TestCase):
    def test_work(self):
        self.assertEqual(lab2.guess(5,[int(k) for k in range(19)]),(5,5))
        self.assertEqual(lab2.guess(40,[int(k)for k in range(30,43)]),(40,5))
        self.assertEqual(lab2.guess(-1,[int(k)for k in range(-3,10)]),(-1,5))
        self.assertEqual(lab2.guess(3,[int(k)for k in range(3,19)]),(3,5))  # проверяем, находит ли число, если оно на левой границе
        self.assertEqual(lab2.guess(15,[int(k) for k in range(1,16)]),(15,5)) # проверяем, находит ли число, если оно на правой границе
        
    def test_forERRORS(self):
        with self.assertRaises(ValueError):  # проверяем рейзит ли ошибку при некорректном списке
            lab2.guess(10,[int(k)for k in range(9)])
            lab2.guess(-4,[int(k)for k in range(9)])
            lab2.guess(100,[int(k)for k in range(25)])
            lab2.guess('3',[int(k)for k in range(9)])
            lab2.guess(3,[])
            lab2.guess(3,['45','56','77'])
            lab2.guess(3,['45','56',2,3,4,5])
            
            
            
if __name__=='__main__':
    unittest.main()