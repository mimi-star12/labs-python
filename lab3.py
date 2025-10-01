# Root = 15; height = 6, left_leaf = 2*(root+1), right_leaf = 2*(root-1)

def get_bin_tree(root: int, height: int) -> dict:
    """Function, constructs a binary tree from root and height.
    
    Arguments:
        root (int) - node value
        height (int) - layer value for binary tree
    Returns:
        (dict) - binary tree in dict type including a list of dicts as value
    """
    

    if height > 1:
        return {root: [get_bin_tree(left_leaf(root), height-1), 
                       get_bin_tree(right_leaf(root), height-1)]}
    
    elif height == 1: 
        return {root}
    
    else: 
        return {}
    
def left_leaf(root: int) -> int:
    """Calculates the value for the left leaf

    Formula for calculation: 2 * (root + 1)

    Arguments:
        root (int) - current parent
    Returns:
        int - value of left leaf
    """
    return 2*(root+1)

def right_leaf(root: int) -> int:
    """Calculates the value for the right leaf

    formula for calculation: 2 * (root - 1)

    Arguments:
        root (int) - current parent
    Returns:
        int - value of right leaf
    """
    return 2*(root-1)

print(help(get_bin_tree))
print(get_bin_tree(15,6))
