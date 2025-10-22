import unittest

import lab5

class test_tree(unittest.TestCase):

    def test_getbintree(self):
        """tests get_bin_tree function"""
        self.assertEqual(lab5.get_bin_tree_iter(10, 0), {10})
        self.assertEqual(lab5.get_bin_tree_iter(1, 2),{1: [{4: [10, 6]}, {0: [2, -2]}]})
        self.assertEqual(lab5.get_bin_tree_iter(5, 1), {5: [12, 8]})
        
    
    def test_for_value_error(self):
        """tests get_bin_tree for ValueError"""
        with self.assertRaises(ValueError):
            lab5.get_bin_tree_iter(10, -1)
            lab5.get_bin_tree_iter(5, -10)
            lab5.get_bin_tree_iter(0, -5)
            lab5.get_bin_tree_iter(10, -100)
    
    def test_for_type_error(self):
        """tests every function for errors"""
        with self.assertRaises(TypeError):
            lab5.get_bin_tree_iter('', 2)
            lab5.get_bin_tree_iter(23, '')
            lab5.get_bin_tree_iter(1.5, 2)
            lab5.get_bin_tree_iter(23, 2.5)

if __name__ == '__main__':
    unittest.main()                                 
    