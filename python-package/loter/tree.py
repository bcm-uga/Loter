import numpy as np

class Node(object):

    def __init__(self, depth, value):
        self.depth = depth
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.value)

def all_paths(node):
    if node.left is None and node.right is None:
        return [[node.value]]
    elif node.left is None:
        res = all_paths(node.right)
        for e in res:
            e.insert(0, node.value)
        return res
    elif node.right is None:
        res = all_paths(node.left)
        for e in res:
            e.insert(0, node.value)
        return res
    else:
        res_left = all_paths(node.left)
        res_right = all_paths(node.right)
        for e in res_left:
            e.insert(0, node.value)
        for e in res_right:
            e.insert(0, node.value)
        return res_left + res_right

def npy_tree(tree):
    res = np.array(all_paths(tree))
    return res[:, 1:].astype(np.uint8)

def update_left(l_node, i):
    node_added = list()
    for node in l_node:
        if node is None:
            print("Warning")
        else:
            if node.left is None:
                node.left = Node(i, 0)

            node_added.append(node.left)

    return node_added

def update_right(l_node, i):
    node_added = list()
    for node in l_node:
        if node is None:
            print("Warning")
        else:
            if node.right is None:
                node.right = Node(i, 1)

            node_added.append(node.right)

    return node_added

def update_tree(root, arr):
    curr = root
    to_update = [curr]
    for i, elem in enumerate(arr):
        nextlevel = list()
        if elem == 0:
            new_nodes = update_left(to_update, i)
            nextlevel.extend(new_nodes)
        elif elem == 2:
            new_nodes = update_right(to_update, i)
            nextlevel.extend(new_nodes)
        else:
            new_nodes = update_left(to_update, i)
            nextlevel.extend(new_nodes)
            new_nodes = update_right(to_update, i)
            nextlevel.extend(new_nodes)

        to_update = nextlevel

def build_tree(mat):
    root = Node(0, "root")
    for row in mat:
        update_tree(root, row)

    return root

def count_width(tree):
    if tree is None:
        return 0
    else:
        if tree.left is None and tree.right is None:
            return 1
        else:
            return count_width(tree.left) + count_width(tree.right)

def arr_to_h(k, arr):
    res_h = []
    curr_pos = 1
    last_pos = 0
    n, m = arr.shape
    while curr_pos <= m:
        width = 0
        while width < k and curr_pos <= m:
            t = build_tree(arr[:, last_pos:curr_pos])
            width = count_width(t)
            curr_pos = curr_pos + 1
        h = npy_tree(t)
        if len(h) < k:
            nb_rows = k - len(h)
            h = np.vstack([h, h[np.random.randint(h.shape[0], size=nb_rows), :]])
        h = np.random.shuffle(h)
        res_h.append(h)
        last_pos = curr_pos - 1

    print(res_h)
    return np.hstack(res_h)

def mat_split(k, arr, pos):
    actual_pos = pos
    arr_fp = np.fliplr(arr[:, :pos])
    arr_lp = arr[:, pos:]

    res_fp = np.fliplr(arr_to_h(k, arr_fp))
    res_lp = arr_to_h(k, arr_lp)
    print(res_fp.shape)
    print(res_lp.shape)

    return np.hstack([res_fp, res_lp])

