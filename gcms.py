from bin import Bin
from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException

def compare_by_capacity_then_id_asc(node1, node2):
    if node1.remaining_capacity != node2.remaining_capacity:
        return -1 if node1.remaining_capacity < node2.remaining_capacity else 1
    return -1 if node1.bin_id < node2.bin_id else (1 if node1.bin_id > node2.bin_id else 0)
      
def compare_by_object_id(node1, node2):
    return -1 if node1.obj_id < node2.obj_id else (1 if node1.obj_id > node2.obj_id else 0)
    
def compare_by_bin_id_asc(node1, node2):
    return -1 if node1.bin_id < node2.bin_id else (1 if node1.bin_id > node2.bin_id else 0)

def compare_by_capacity_then_id_desc(node1, node2):
    if node1.remaining_capacity != node2.remaining_capacity:
        return -1 if node1.remaining_capacity < node2.remaining_capacity else 1
    return 1 if node1.bin_id < node2.bin_id else (-1 if node1.bin_id > node2.bin_id else 0)
                
class GCMS:
    def __init__(self):
        self.bin_tree_leastId=AVLTree(compare_by_capacity_then_id_asc)
        self.object_tree=AVLTree(compare_by_object_id)
        self.id_bin=AVLTree(compare_by_bin_id_asc)
        self.bin_tree_greatestId=AVLTree(compare_by_capacity_then_id_desc)
        pass 

    def add_bin(self, bin_id, capacity):
        self.bin_tree_leastId.insert(Bin(bin_id, capacity))
        self.bin_tree_greatestId.insert(Bin(bin_id, capacity))
        self.id_bin.insert(Bin(bin_id, capacity))
        pass
    
    def find_object(self, obj_id):
        current = self.object_tree.root

        while current is not None:
            if current.key.obj_id == obj_id:
                return current
            elif obj_id < current.key.obj_id:
                current = current.left
            else:
                current = current.right
        
        return None  # Return None if the object is not found
    
    def find_bin_to_add_obj(self, root, bin_id):
            if root == None:
                return None
            if root.key.bin_id == bin_id:
                return root
            elif root.key.bin_id < bin_id:
                return self.find_bin_to_add_obj(root.right, bin_id)
            else:
                return self.find_bin_to_add_obj(root.left, bin_id)

    def add_object(self, object_id, size, color):
        suitable_bin=self.binfind(color, size)
        if suitable_bin is None:
            raise NoBinFoundException
        else:
            id=suitable_bin.key.bin_id
            my_obj=Object(object_id, size , color, id)
            new_cap=suitable_bin.key.remaining_capacity - size
            self.object_tree.insert(my_obj)
            new_bin=Bin(id, new_cap)

            myNode=self.find_bin_to_add_obj(self.id_bin.root, id)
            myNode.key.obj_tree.insert(my_obj)
            myNode.key.remaining_capacity-=size
               
            self.bin_tree_greatestId.delete(Bin(id, new_cap+size))
            self.bin_tree_leastId.delete(Bin(id, new_cap+size))

            self.bin_tree_greatestId.insert(new_bin)
            self.bin_tree_leastId.insert(new_bin)

    def compactFitWithLeastId(self, root, size):
        current = root
        ans = None

        while current is not None:
            if current.key.remaining_capacity < size:
                current = current.right
            else:
                ans = current
                current = current.left

        return ans
    
    def compactFitWithGreatestId(self, root, size):
        current = root
        last_valid = None

        while current is not None:
            if current.key.remaining_capacity >= size:
                last_valid = current
                current = current.left
            else:
                current = current.right

        return last_valid

    def largestFitWithLeastId(self, root, size):
        if root is None:
            return None
        else:
            right_ans =  self.largestFitWithLeastId(root.right, size)
            if right_ans:
                return right_ans
            else:
                if root.key.remaining_capacity >= size:
                    return root
                else:
                    return None

    def largestFitWithGreatestId(self, root, size):
        if root is None:
            return None       
        else: 
            right_ans= self.largestFitWithGreatestId(root.right, size)
            if right_ans is None and root.key.remaining_capacity>=size:
                return root
            else:
                return right_ans

    def binfind(self, color, size):
        if color == Color.BLUE:
            return self.compactFitWithLeastId(self.bin_tree_leastId.root, size)
        elif color == Color.YELLOW:
            return self.compactFitWithGreatestId(self.bin_tree_greatestId.root, size)
        elif color == Color.RED:
            return self.largestFitWithLeastId(self.bin_tree_greatestId.root, size)
        else:
            return self.largestFitWithGreatestId(self.bin_tree_leastId.root, size)
           
    def delete_object(self, object_id):
        myObject = self.object_tree.root
        while myObject is not None:
            if myObject.key.obj_id == object_id:
                break
            elif object_id < myObject.key.obj_id:
                myObject = myObject.left
            else:
                myObject = myObject.right
        
        if(myObject is None):
            return None
        temp=myObject.key
        size=myObject.key.size
        parent_id=myObject.key.parent_id
        self.object_tree.delete(myObject.key)

        bin_id = parent_id
        current = self.id_bin.root

        while current is not None:
            if current.key.bin_id == bin_id:
                bin = current
                break
            elif bin_id < current.key.bin_id:
                current = current.left
            else:
                current = current.right
        else:
            bin = None  #None if the bin is not found

        cap=bin.key.remaining_capacity
        
        #now we find the obj in the bin insie tree and delete it using the above algo only 
        bin.key.obj_tree.delete(temp)
        bin.key.remaining_capacity+=size

        self.bin_tree_greatestId.delete(Bin(parent_id , cap))
        self.bin_tree_leastId.delete(Bin(parent_id , cap))

        self.bin_tree_greatestId.insert(Bin(parent_id , cap+size))
        self.bin_tree_leastId.insert(Bin(parent_id , cap+size))

        
    def bin_info(self, bin_id):
        current_node = self.id_bin.root
        while current_node:
            if current_node.key.bin_id == bin_id:
                return (current_node.key.remaining_capacity, current_node.key.objects_list())
            current_node = current_node.left if bin_id < current_node.key.bin_id else current_node.right
        return None

    def object_info(self, object_id):
        # Search for the object in the AVL tree
        object_node = self.find_object(object_id)
        # If the object is found, return its parent bin ID; otherwise, return None
        return object_node.key.parent_id if object_node else None
        
#################################GurnoorSingh###################################################
#################################GurnoorSingh###################################################