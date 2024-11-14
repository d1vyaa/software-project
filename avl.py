from node import Node

class AVLTree:
    def __init__(self, compare_function):
        self.root = None
        self.size = 0
        self.comparator = compare_function  # Comparator function to determine node ordering

    def get_height(self, node):
        if node is None:
            return 0
        
        return node.height
        
    def balance_factor(self, node):
        if node is None:
            return 0
        
        return self.get_height(node.right) - self.get_height(node.left)

    def left_rotation(self, x):
        if x.right is None:
            return x  

        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y
    
    def right_rotation(self, y):
        # e
        if y.left is None:
            return y  

        x = y.left
        T2 = x.right

        # change
        x.right = y
        y.left = T2

        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return x

    def insert(self, val):
        self.root = self.inl(self.root, val)

    def inl(self, root, val):
            if root is None:
                return Node(val)

            if self.comparator(val, root.key) < 0:
                root.left = self.inl(root.left, val)
            elif self.comparator(val, root.key) > 0:
                root.right = self.inl(root.right, val)

            # Update the height of the ancestor node
            root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

            # Balance the node
            bf = self.balance_factor(root)

            # Left-left case
            if bf < -1 and self.comparator(val, root.left.key) < 0:
                return self.right_rotation(root)

            # Right-right case
            if bf > 1 and self.comparator(val, root.right.key) > 0:
                return self.left_rotation(root)

            # Left-right case
            if bf < -1 and self.comparator(val, root.left.key) > 0:
                root.left = self.left_rotation(root.left)
                return self.right_rotation(root)

            # Right-left case
            if bf > 1 and self.comparator(val, root.right.key) < 0:
                root.right = self.right_rotation(root.right)
                return self.left_rotation(root)

            return root


    def delete(self, data):
        def delete_util(root, data):
            if root is None:
                return None

            if self.comparator(data, root.key) > 0:
                root.right = delete_util(root.right, data)
            elif self.comparator(data, root.key) < 0:
                root.left = delete_util(root.left, data)
            else:
                # Node with only one child or no child
                if root.left is None:
                    return root.right
                elif root.right is None:
                    return root.left

                # Node with two children: Get the inorder successor
                temp = self.get_min_value_node(root.right)
                root.key = temp.key
                root.right = delete_util(root.right, temp.key)

            # Update the height of the ancestor node
            root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

            # Balance the node
            bf = self.balance_factor(root)

            # Left-left case
            if bf < -1 and self.balance_factor(root.left) <= 0:
                return self.right_rotation(root)

            # Left-right case
            if bf < -1 and self.balance_factor(root.left) > 0:
                root.left = self.left_rotation(root.left)
                return self.right_rotation(root)

            # Right-right case
            if bf > 1 and self.balance_factor(root.right) >= 0:
                return self.left_rotation(root)

            # Right-left case
            if bf > 1 and self.balance_factor(root.right) < 0:
                root.right = self.right_rotation(root.right)
                return self.left_rotation(root)

            return root

        self.root = delete_util(self.root, data)


    def get_min_value_node(self, root):
        while root.left is not None:
            root = root.left
        return root

    
#################################GurnoorSingh###################################################
#################################GurnoorSingh###################################################