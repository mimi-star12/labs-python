# Root = 15; height = 6, left_leaf = 2*(root+1), right_leaf = 2*(root-1)


def get_bin_tree(root: int, height: int) -> dict:
    if height > 1:
        return {root: [get_bin_tree(left_leaf(root), height-1), get_bin_tree(right_leaf(root), height-1)]}
    elif height == 1: 
        return {root}
    else: 
        return {}
    
def left_leaf(root: int) -> int:
    return 2*(root+1)

def right_leaf(root: int) -> int:
    return 2*(root-1)

print(get_bin_tree(15,6))