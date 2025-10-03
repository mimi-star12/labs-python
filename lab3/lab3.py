# Root = 15; height = 6, left_leaf = 2*(root+1), right_leaf = 2*(root-1)
from collections import deque

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
        return {root: []}
    
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


def print_tree_by_levels(tree_dict: dict):
    """
    Prints nodes, dividing them by levels

    Args:
        tree_dict (dict) - tree, that we get from function get_bin_tree
    """
    if not tree_dict:
        print("Дерево пусто.")
        return

    root_value, children = list(tree_dict.items())[0]
    elements = deque([(root_value, children, 0)])
    
    current_level = 0
    line_output = []

    while elements:
        node_value, children_list, level = elements.popleft()

        if level > current_level:
            # go to another level, print previous one 
            print(f"Level {current_level}: {' | '.join(line_output)}")
            current_level = level
            line_output = []
        
        # adds current node to the output
        line_output.append(str(node_value))

        for child_subtree in children_list:
            if child_subtree:
                # get info about child, grandchildren
                child_root, grand_children = list(child_subtree.items())[0]
                elements.append((child_root, grand_children, level + 1))

    # print the last level
    if line_output:
        print(f"Level {current_level}: {' | '.join(line_output)}")

print_tree_by_levels(get_bin_tree(15,6))

print(get_bin_tree(15,6))
#print(help(get_bin_tree))