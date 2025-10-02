import unittest

import lab3

class test_tree(unittest.TestCase):
    """group of tests for different tree functions."""
    def test_left_leaf(self):
        """tests left_leaf, formula: 2*(root+1)."""
        self.assertEqual(lab3.left_leaf(10), 22) 
        self.assertEqual(lab3.left_leaf(13), 28)
        self.assertEqual(lab3.left_leaf(0), 2)
        self.assertEqual(lab3.left_leaf(-3),-4)

    def test_right_leaf(self):
        """tests left_leaf, formula: 2*(root-1)."""
        self.assertEqual(lab3.right_leaf(10), 18) 
        self.assertEqual(lab3.right_leaf(13), 24)
        self.assertEqual(lab3.right_leaf(0), -2)
        self.assertEqual(lab3.right_leaf(-3),-8)

    def test_errors(self):
        """tests every function for errors"""
        with self.assertRaises(TypeError):
            lab3.left_leaf('')
            lab3.left_leaf(1.5)
            lab3.right_leaf('')
            lab3.right_leaf(1.5)
            lab3.get_bin_tree('', 2)
            lab3.get_bin_tree(23, '')

    def test_getbintree(self):
        """tests get_bin_tree function"""
        self.assertEqual(lab3.get_bin_tree(10, -5), {})
        self.assertEqual(lab3.get_bin_tree(10, 0), {})
        self.assertEqual(lab3.get_bin_tree(1, 2), {1: [{4: []}, {0: []}]})
            
if __name__ == '__main__':
    unittest.main()