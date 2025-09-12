import lab1
import unittest

class TestTwoSum(unittest.TestCase):
    def test_basic(self):   # тесты из условия
        self.assertEqual(lab1.two_sum([1,2,7,15],9),[1,2])
        self.assertEqual(lab1.two_sum([3,2,4],6),[1,2])
        self.assertEqual(lab1.two_sum([3,3],6),[0,1])
    def test_additional(self): # доп тесты ---> добавила работу с str
        self.assertEqual(lab1.two_sum(['ss',3,3,87],6),[1,2])
        self.assertEqual(lab1.two_sum(['re',3, 'g',4],7),[1,3])
        self.assertEqual(lab1.two_sum([0,0,0,2,6,1],3),[3,5])
        self.assertEqual(lab1.two_sum(['3','45','7','1'],8),None)
        self.assertEqual(lab1.two_sum([0,0,0,0,0],0),[0,1])
        self.assertEqual(lab1.two_sum([-1,0,-5,-1],-6),[0,2])
        self.assertEqual(lab1.two_sum([-1,6,-1,4],5),[0,1])
    def test_notenough(self): # недостаточное кол-во аргументов тест
        with self.assertRaises(ValueError):
            lab1.two_sum([1],1)
            lab1.two_sum([],0)
if __name__=='__main__':
    unittest.main()