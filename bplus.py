import random
# used only for generating one single random number between 2 values
import math
# used only for ceil function


class Node:
    def __init__(self, order,name='nonleaf'):
        self.order = order
        self.key = [-1]*order
        self.pointer = [None]*(order+1)
        self.name = name
    
    def print_keys(self):
        print(self.key)

    def __str__(self):
        return self.name+ '->' + str(self.key)
    
    def __repr__(self):
        return self.name+ '->' + str(self.key)

class Tree:
    def __init__(self, order):
        self.root = Node(order)
        self.order = order
        self.leaf_min_keys = (order+1)//2
        self.leaf_min_pointers = (order+1)//2 + 1
        self.min_keys = math.ceil((order+1)/2) - 1
        self.min_pointers = math.ceil((order+1)/2)
        self.max_keys = order
        self.max_pointers = order + 1

    def __str__(self):
        return str('\n_______tree details_______\norder:'+str(self.order)+'\nmin_pointers:'+str(self.min_pointers) +'\nleaf min pointers:'+ str(self.leaf_min_pointers)+'\n')

def data_generation(size, low = 100000, high = 200000):
    record = []
    while len(record)<size:
        no = random.randint(low, high)
        if no not in record:
            record.append(no)
    return record

def build_sparse_tree(order, records):
    tree = Tree(order)
    records.sort()
    
    nodes_at_level = []

    leaf_nodes = len(records)//tree.leaf_min_keys
    nodes_at_level.append(leaf_nodes)
    nodes = leaf_nodes//tree.min_pointers
    nodes_at_level.append(nodes)
    
    while nodes>tree.min_pointers:
        nodes = nodes//tree.min_pointers
        nodes_at_level.append(nodes)
    
    if nodes>=2:
        nodes_at_level.append(1)
    
    nodes_at_level.reverse()

    print('nodes at each level:', nodes_at_level, tree)

    leaves = []
    
    i=0
    while i<nodes_at_level[-1]:
        leaf = Node(order)
        leaf.name = 'leaf'
        leaf.key = records[i*tree.leaf_min_keys:(i+1)*tree.leaf_min_keys]
        if i<nodes_at_level[-1]-1:
            leaf.key += [-1]*(order - len(leaf.key))
        if leaves:
            leaves[-1].pointer[-1] = leaf

        leaves.append(leaf)
        i+=1
    leaves[-1].key += records[i*tree.leaf_min_keys:]
    leaves[-1].key += [-1]*(order - len(leaf.key))

    # print('\nleaves')
    # for leaf in leaves:
    #     leaf.print_keys()
    
    level = len(nodes_at_level)-2
    
    # level_nodes = []
    next_level = leaves

    while level>=0:

        i=0
        this_level = []
        j=0
        while len(this_level)<nodes_at_level[level]:
            this_level.append(Node(order))
            this_level[-1].pointer[0] = next_level[i]
            for j in range(1,min(len(next_level)-i, tree.min_keys+1)):
                this_level[-1].pointer[j] = next_level[i+j]
                # this_level[-1].key[j-1] = next_level[i+j].key[0]
                # -----
                min_n = next_level[i+j]
                while min_n.name!='leaf':
                    min_n = min_n.pointer[0]
                this_level[-1].key[j-1] = min_n.key[0]
                # ------
            i+=tree.min_keys+1
        
        j+=1
        for node in next_level[i:]:
            this_level[-1].pointer[j] = node
            this_level[-1].key[j-1] = node.key[0]
            j+=1
        
        level-=1
        next_level = this_level
        # print(next_level,'===========\n')
    tree.root = next_level[0]
    # tree.name = 'root'
    return tree
    
    

def build_dense_tree(order, records):
    tree = Tree(order)
    records.sort()
    
    nodes_at_level = []

    leaf_nodes = math.ceil(len(records)/tree.max_keys)
    nodes_at_level.append(leaf_nodes)
    nodes = math.ceil(leaf_nodes/tree.max_pointers)
    nodes_at_level.append(nodes)
    
    while nodes>1:
        nodes = math.ceil(nodes/tree.max_pointers)
        nodes_at_level.append(nodes)
    
    # if nodes>=2:
    #     nodes_at_level.append(1)
    
    nodes_at_level.reverse()

    print('nodes at each level:', nodes_at_level, tree)

    leaves = []
    
    i=0
    while i<nodes_at_level[-1]:
        leaf = Node(order, 'leaf')
        leaf.key = records[i*tree.max_keys:(i+1)*tree.max_keys]
        if order - len(leaf.key)>0:
            leaf.key += [-1]*(order - len(leaf.key))

        if leaves:
            leaves[-1].pointer[-1] = leaf

        leaves.append(leaf)
        i+=1
    leaves[-1].key += records[i*tree.max_keys:]

    # print('\nleaves')
    # for leaf in leaves:
    #     leaf.print_keys()
    
    level = len(nodes_at_level)-2
    
    # level_nodes = []
    next_level = leaves

    while level>=0:

        i=0
        this_level = []
        j=0
        while len(this_level)<nodes_at_level[level]:
            this_level.append(Node(order))
            min_n = next_level[i]
            while min_n.name!='leaf':
                min_n = min_n.pointer[0]
            this_level[-1].pointer[0] = next_level[i]
            this_level[-1].key[0] = min_n.key
            for j in range(1,min(len(next_level)-i, tree.max_keys+1)):
                this_level[-1].pointer[j] = next_level[i+j]
                # this_level[-1].key[j-1] = next_level[i+j].key[0]
                # ---
                min_n = next_level[i+j]
                while min_n.name!='leaf':
                    min_n = min_n.pointer[0]
                this_level[-1].key[j-1] = min_n.key[0]
                # ----
            i+=tree.max_keys+1
        
        j+=1
        for node in next_level[i:]:
            this_level[-1].pointer[j] = node
            this_level[-1].key[j-1] = node.key[0]
            j+=1
        
        level-=1
        next_level = this_level
        # print(next_level,'===========\n')
    # if nodes_at_level[0] == 1:
    tree.root = next_level[0]
    # print('+++++++++++++', next_level)
    # else:

        
    # tree.name = 'root'
    return tree
    

def search(tree, search_key):
    node = tree.root
    # print(node)
    if node == None:
        return None, None
    while node.name == 'nonleaf':
        i=0
        flag = 0
        while i<len(node.key) and node.key[i]!=-1:
            
            if node.key[i] > search_key:
                # print('_________',node.key[i])
                node = node.pointer[i]
                # print(node)
                flag = 1
                break
            i+=1

        if flag == 0:
            node = node.pointer[i]
            # print(node)

    # print(node)
    if node:
        for i in range(len(node.key)):
            if node.key[i] == search_key:
                return node, i
            if node.key[i] > search_key:
                return node, None
    return node, None


def range_search(tree, start, end):
    """Includes both start and end"""
    
    if end<start:
        print('end<start...incorrect input')
        return []

    node, pos = search(tree, start)

    if node==None:
        return []

    found = []
    if pos==None:
        for i in range(len(node.key)):
            if node.key[i] > start:
                pos = i
                break
    if pos == None:
        pos = 0
        node = node.pointer[-1]

    while node.key[pos]<=end:

        found.append(node.key[pos])
        pos+=1

        if pos>=len(node.key) or node.key[pos]==-1:
             node = node.pointer[-1]
             pos = 0

    return found


def insert(tree, pt, p, k, p1, k1):

    # case 1
    if pt == None:
        return None, -1
    print('inserting', k, 'looking at', pt)
    if pt.name == 'leaf':
        if len(pt.key)<pt.order or pt.key[-1]==-1:
            # print('hehe', k)
            pos = -1
            for i in range(len(pt.key)):
                if pt.key[i]>k or pt.key[i]==-1:
                    # print(pt.key[i], k)
                    pos = i
                    break
            pt.key.insert(pos, k)
            pt.key = pt.key[:-1]
            pt.pointer.insert(pos+1,p)
            pt.pointer[-2] = pt.pointer[-1]
            pt.pointer = pt.pointer[:-1]
            print('inserted at', pt, 'at', pos)
            return None, -1
        else:
            pos = len(pt.key)
            for i in range(len(pt.key)):
                if pt.key[i]>k or pt.key[i]==-1:
                    pos = i
                    break
            all_keys = pt.key[:pos] + [k] + pt.key[pos:]
            all_pointers = pt.pointer[:pos] + [p] + pt.pointer[pos:]
            r = (pt.order+1)//2

            k_part2 = all_keys[r+1:] 
            p_part2 = all_pointers[r+1:-1] + [None]*(pt.order-len(k_part2)) + [all_pointers[-1]]
            k_part2 += [-1]*(pt.order-len(k_part2))
            new_leaf = Node(pt.order, 'leaf')
            new_leaf.key = k_part2
            new_leaf.pointer = p_part2
            print('made new leaf:', new_leaf)
            # new_leaf.flag = 'newleaf'
            # pt.flag = 'pt========'
            pt.key = all_keys[:r+1]
            pt.pointer = all_pointers[:r] + [None]*(pt.order-len(pt.key)) + [all_pointers[-1]]
            pt.key += [-1]*(pt.order-len(pt.key))
            pt.pointer[-1] = new_leaf

            if tree.root == pt:
                new_root = Node(pt.order)
                # new_root.flag = 'new root------'
                new_root.pointer[0] = pt
                new_root.pointer[1] = new_leaf
                new_root.key[0] = all_keys[r+1]
                print('root changed to', new_root)
                tree.root = new_root
            else:
                return new_leaf, all_keys[r+1]

    # case 2
    else:
        for i in range(len(pt.key)):
            if pt.key[i]>k or pt.key[i]==-1:
                p1, k1 = insert(tree, pt.pointer[i], p, k, p1, k1)
                break
        if p1 == None:
            return None, -1
        
        elif pt.key[-1] == -1:

            pos = len(pt.key)
            for i in range(len(pt.key)):
                if pt.key[i]>k1 or pt.key[i]==-1:
                    pos = i
                    break
            pt.key.insert(pos, k1)
            pt.key = pt.key[:-1]
            pt.pointer.insert(pos+1,p1)
            # pt.flag3 = 'ckecking insertion p'
            pt.pointer[-2] = pt.pointer[-1]
            pt.pointer = pt.pointer[:-1]
            print('inserted at', pt, 'at', pos)
            return None, -1
        
        else:

            pos = -1
            for i in range(len(pt.key)):
                if pt.key[i]>k1:
                    pos = i
                    break
            all_keys = pt.key[:pos] + [k1] + pt.key[pos:]
            all_pointers = pt.pointer[:pos] + [p1] + pt.pointer[pos:]
            r = math.ceil((pt.order+1)/2)

            k_part2 = all_keys[r+1:] 
            p_part2 = all_pointers[r+1:-1] + [None]*(pt.order-len(k_part2)) + [all_pointers[-1]]
            k_part2 += [-1]*(pt.order-len(k_part2))
            new_node = Node(pt.order)
            new_node.key = k_part2
            new_node.pointer = p_part2
            print('made new node:', new_node)

            pt.key = all_keys[:r+1]
            pt.pointer = all_pointers[:r] + [None]*(pt.order-len(pt.key)) + [all_pointers[-1]]
            pt.key += [-1]*(pt.order-len(pt.key))
            pt.pointer[-1] = new_node
            print('new pt:', pt)

            if tree.root == pt:

                new_root = Node(pt.order)
                new_root.flag2 = 'new root2___'
                new_root.pointer[0] = pt
                new_root.pointer[1] = new_node
                new_root.key[0] = all_keys[r]
                tree.root = new_root
                print('root changed to', new_root)
            else:
                return new_node, all_keys[r]
        

def delete(tree, pt, k, p, belowmin):
    # case 1
    if pt == None:
        return False

    print('deleting', k, 'looking at', pt)

    if pt.name == 'leaf':
        length = len(pt.key)
        for i in range(len(pt.key)):
            if pt.key[i] == k:
                pt.key.pop(i)
                pt.key.append(-1)
                pt.pointer.pop(i)
                pt.pointer.insert(-1, None)
            
            if pt.key[i] == -1:
                length = i
                break
            
        print('deleted',k,'from pt:', pt)
            
        if pt == tree.root or length>=tree.leaf_min_keys:
            return False
        else:
            return True
        
    # case 2
    else:
        for i in range(len(pt.key)):
            if pt.key[i]>k or pt.key[i]==-1:
                belowmin1 = delete(tree, pt.pointer[i], k, p, belowmin)
                break
        pi = pt.pointer[i]
        ptpos = i
        if not belowmin1:
            return False
        elif pi.pointer[-1]!=None:
            length = len(pi.pointer[-1].key)
            for j in range(len(pi.pointer[-1].key)):
                if pi.pointer[-1].key[j] == -1:
                    length = j
                    break
            if length>tree.min_keys:
                # move one key pointer pair from pi.pointer[-1] to pi
                p1 = pi
                p2 = pi.pointer[-1]
                print('moving one key pointer pair from', p1, 'to', p2)
                # p2 = pt.pointer[ptpos+1]
                
                length1 = len(p1.key)
                for i in range(len(p1.key)):
                    if p1.key[i]==-1:
                        length1 = i
                        break
                if p1.name == 'nonleaf':
                    p1.pointer[length1+1] = p2.pointer[0]
                    p2.pointer = p2.pointer[1:]
                    p2.pointer.insert(-1,None) 
                    p1.key[length1] = pt.key[ptpos]
                    pt.key[ptpos] = p2.key[0]
                    p2.key = p2.key[1:] + [-1]
                else:
                    p1.pointer[length1] = p2.pointer[0]
                    p2.pointer = p2.pointer[1:]
                    p2.pointer.insert(-1,None) 
                    p1.key[length1] = p2.key[0]
                    p2.key = p2.key[1:] + [-1]
                    pt.key[ptpos] = p2.key[0]

                print('after moving:', p1, p2, '\nparent:', pt)
            
            else:
                # combine pi and sibling
                p1 = pi
                p2 = pi.pointer[-1]

                print('combining', p1, 'and', p2)

                length1 = len(p1.key)
                for i in range(len(p1.key)):
                    if p1.key[i]==-1:
                        length1 = i
                        break
                
                length1_key = length1
                
                if p1.name == 'nonleaf':
                    p1.key[length1] = pt.key[ptpos]
                    length1_key = length1 + 1
                pt.key.pop(ptpos)
                pt.key.append(-1)

                for i in range(length):
                    p1.key[length1_key+i] = p2.key[i]
                    # check index for pointer 
                    p1.pointer[length1+1+i] = p2.pointer[i]

                p1.pointer[-1] = p2.pointer[-1]
                
                pt.pointer.pop(ptpos+1)
                pt.pointer.insert(-1,None)

                print('after combining nodes', p1, '\nparent', pt)

                if pt == tree.root and pt.pointer[1]==None:
                    # check if pt chould be replaced by pi in tree
                    # pt = pi
                    tree.root = pi
                    return False
                
                pt_length = len(pt.key)
                for i in range(len(pt.key)):
                    if pt.key[i] == -1:
                        pt_length = i
                        break

                if pt == tree.root or pt_length>tree.min_keys:
                    return False
                
                else:
                    return True

        

def random_ops(tree, rec, n = 5):
    for _ in range(n):
        p = random.random()
        if p > 0.5:
            k = random.randint(100000, 200000)
            print('\n\n========operation: insert',k,'==========')
            while k in rec:
                k = random.randint(100000, 200000)
            rec.append(k)
            insert(tree, tree.root, None, k, None, -1)
        else:
            k = random.randint(0, 9900)
            print('\n\n=========operation: delete',rec[k],'==========')
            delete(tree,tree.root, rec[k], None, True)


def random_search(tree, n = 5):
    for _ in range(n):
        k = random.randint(100000, 200000)
        out = search(tree, k)
        if out[1] == None:
            result = 'not found'
        else:
            result = 'found at '+str(out[1])+' in node:'+str(out[0]) 
        print('\nsearching', k, '\nresult:', result)



def experiments():
    # a
    rec = data_generation(10000)

    # b
    # d13 = build_dense_tree(13, rec)
    s13 = build_sparse_tree(13, rec)
    d24 = build_dense_tree(24, rec)
    # s24 = build_sparse_tree(24, rec)

    # # c1
    # added = 0
    # while added<2:
    #     print('\n\n\n=============using dense13================')
    #     no = random.randint(100000, 200000)
    #     if no not in rec:
    #         rec.append(no)
    #         insert(d13, d13.root, None, no, None, -1)
    #         added+=1

    added = 0
    while added<2:
        print('\n\n\n=============using dense24================')
        no = random.randint(100000, 200000)
        if no not in rec:
            insert(d24, d24.root, None, no, None, -1)
            added+=1

    
    # c2
    print('\n\n\n===========================c2====================================')
    for _ in range(2):
        print('\n\n\n=============using sparse13================')
        no = random.randint(0, 9900)
        delete(s13,s13.root, rec[no], None, True)

    # for _ in range(2):
    #     print('\n\n\n=============using sparse24================')
    #     no = random.randint(0, 9900)
    #     delete(s24,s24.root, rec[no], None, True)

    # # c3
    # print('\n\n\n===========================c3====================================')
    # print('\n\n\n=============using dense13================')
    # random_ops(d13, rec)
    # print('\n\n\n=============using dense24================')
    # random_ops(d24, rec)
    # print('\n\n\n=============using sparse13================')
    # random_ops(s13, rec)
    # print('\n\n\n=============using sparse24================')
    # random_ops(s24, rec)

    # # c4
    # print('\n\n\n===========================c4====================================')
    # print('\n\n\n=============using dense13================')
    # random_search(d13)
    # print('\n\n\n=============using dense24================')
    # random_search(d24)
    # print('\n\n\n=============using sparse13================')
    # random_search(s13)
    # print('\n\n\n=============using sparse24================')
    # random_search(s24)



def test():
    # rec = [2, 3, 8, 9, 11, 13, 29, 33, 35, 36, 38, 51, 69, 80, 85, 99, 100, 101, 102, 107, 112, 120, 128, 132, 140, 146, 147, 149, 155, 156, 161, 165, 171, 187, 189, 194, 209, 216, 225, 233, 236, 247, 266, 274, 277, 281, 282, 283, 288, 289, 290, 295, 296, 298, 299, 300, 302, 306, 307, 315, 319, 321, 322, 325, 328, 333, 337, 338, 339, 343, 344, 345, 351, 352, 354, 355, 360, 364, 372, 381, 396, 397, 406, 408, 409, 410, 427, 432, 438, 447, 460, 465, 471, 477, 479, 483, 487, 490, 491, 498]
    rec = list(range(25))
    tree2 = build_sparse_tree(6,rec)
    # # tree2 = build_dense_tree(6,rec)
    # # print('root', tree2.root)
    # # print(rec[-205])
    # # print(search(tree2, 200))
    # # print(rec)
    # # print(range_search(tree2, 250, 275))
    # # pos = search(tree2, 9.5)
    # # print(pos[0], pos[1])
    # # insert(tree2, pos[0], None, 30, None, 0)
    # # print(search(tree2, 30))
    # # insert(tree2, tree2.root, None, 113,None, -1)
    delete(tree2, tree2.root, 12, None, True)
    # delete(tree2, tree2.root, 11, None, True)


experiments()