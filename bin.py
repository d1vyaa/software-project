from avl import AVLTree

def comp(node1, node2):
            if node1.obj_id < node2.obj_id:
                return -1
            elif node1.obj_id > node2.obj_id:
                return 1
            else:
                return 0
            
class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id = bin_id
        self.remaining_capacity = capacity
        self.obj_tree = AVLTree(comp)
        self.height = 1

    def remove_object(self, object):
        self.obj_tree.delete(object)

    def add_object(self, object):
        self.obj_tree.insert(object)
        self.remaining_capacity -= object.size

    def objects_list(self):
        def inorder(node, result):
            if not node:
                return
            inorder(node.left, result)
            result.append(node.key.obj_id)
            inorder(node.right, result)
        
        result = []
        inorder(self.obj_tree.root, result)
        return result


#################################GurnoorSingh###################################################
#################################GurnoorSingh###################################################