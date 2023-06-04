class RedBlackTree():
    # Node class - DO NOT MODIFY
    class _Node:
        RED = object()
        BLACK = object()
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_left', '_right', '_color' # streamline memory usage

        def __init__(self, element, parent=None, left=None, right=None, color=RED):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right
            self._color = color

    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    # Search for the element in the red-black tree.
    # return: _Node object, or None if it's non-existing
    def search(self, element):
        print("Do search...")
        """
        Search for the element in the red-black tree.
        return: _Node object, or None if it's non-existing
        """
        node = self._root
        while node is not None:
            if element < node._element:
                node = node._left
            elif element > node._element:
                node = node._right
            else:  # element is equal to node._element
                return node  # found the node, return it
        return None  # not found
    
    def insert(self, element):
        print("Do insert")
        """Insert an element into the red-black tree."""
        new_node = self._Node(element)
        if self._root is None:
            self._root = new_node
            self._root._color = self._Node.BLACK
            self._size += 1
        else:
            parent = None
            curr = self._root
            while curr is not None:
                parent = curr
                if new_node._element < curr._element:
                    curr = curr._left
                else:
                    curr = curr._right
            new_node._parent = parent
            if new_node._element < parent._element:
                parent._left = new_node
            else:
                parent._right = new_node
            self._size += 1
            self._fix_insert(new_node)
            
    def delete(self, element):
        print("Do delete")
        """Delete an element from the red-black tree."""
        # TODO: Perform BST deletion and fix the tree
        
        node = self.search(element)
        deleted_node_element = node._element

        if node is None:
            return None
        if node._left and node._right:
            successor = self._successor(node)
            node._element = successor._element
            node = successor

        # node to be deleted now has at most one child
        child = node._right if node._left is None else node._left

        # case where node to be deleted is red
        if self._is_black(node) == False:
            self._replace_node(node, child)
            self._size -= 1
        # case where node to be deleted is black
        else:
            if self._is_black(child):
                self._dbl_black(node)
            else:
                if node._parent is not None:
                    if node == node._parent._left:
                        node._parent._left = child
                    else:
                        node._parent._right = child
                else:
                    self._root = child
                child._parent = node._parent
                child._color = self._Node.BLACK
            self._size -= 1
            
        return deleted_node_element

    # BONUS FUNCTIONS -- use them freely if you want
    def _is_black(self, node):
        return node == None or node._color == self._Node.BLACK

    def _successor(self, node):
        successor = node._right
        while successor._left != None:
            successor = successor._left
        return successor

    # def _sibiling(self, node):
    #     parent = node._parent

    #     if parent._left == node:
    #         return parent._right
    #     else:
    #         return parent._left
        
    def _sibling(self, node):
        """
        Return the sibling of the node.
        """
        if node._parent is None:  # Node is root
            return None
        if node is node._parent._left:  # Node is a left child
            return node._parent._right
        return node._parent._left  # Node is a right child
        
    def _fix_insert(self, node):
        """Fix red-black tree properties after insertion."""
        while node != self._root and node._parent._color == self._Node.RED:
            if node._parent == node._parent._parent._left:
                uncle = node._parent._parent._right
                if uncle is not None and uncle._color == self._Node.RED:
                    node._parent._color = uncle._color = self._Node.BLACK
                    node._parent._parent._color = self._Node.RED
                    node = node._parent._parent
                else:
                    if node == node._parent._right:
                        node = node._parent
                        self._rotate_left(node)
                    node._parent._color = self._Node.BLACK
                    node._parent._parent._color = self._Node.RED
                    self._rotate_right(node._parent._parent)
            else:
                uncle = node._parent._parent._left
                if uncle is not None and uncle._color == self._Node.RED:
                    node._parent._color = uncle._color = self._Node.BLACK
                    node._parent._parent._color = self._Node.RED
                    node = node._parent._parent
                else:
                    if node == node._parent._left:
                        node = node._parent
                        self._rotate_right(node)
                    node._parent._color = self._Node.BLACK
                    node._parent._parent._color = self._Node.RED
                    self._rotate_left(node._parent._parent)
        self._root._color = self._Node.BLACK

    def _rotate_left(self, node):
        """Left rotate the subtree rooted with the node."""
        pivot = node._right
        node._right = pivot._left
        if node._right is not None:
            node._right._parent = node
        pivot._parent = node._parent
        if node._parent is None:
            self._root = pivot
        else:
            if node == node._parent._left:
                node._parent._left = pivot
            else:
                node._parent._right = pivot
        pivot._left = node
        node._parent = pivot

    def _rotate_right(self, node):
        """Right rotate the subtree rooted with the node."""
        pivot = node._left
        node._left = pivot._right
        if node._left is not None:
            node._left._parent = node
        pivot._parent = node._parent
        if node._parent is None:
            self._root = pivot
        else:
            if node == node._parent._right:
                node._parent._right = pivot
            else:
                node._parent._left = pivot
        pivot._right = node
        node._parent = pivot
    
    def _replace_node(self, node, child):
        """
        Replace a node with its child.
        """
        # Check if 'node' is the root
        if node._parent is None:
            self._root = child
        else:
            # 'node' is not the root, check if it's the left or right child and replace it
            if node is node._parent._left:
                node._parent._left = child
            else:
                node._parent._right = child

        # If child is not None, update its parent
        if child is not None:
            child._parent = node._parent



    def _dbl_black(self, node):
        if node is self._root:
            # Case 1: node is root. Do nothing and return.
            return
        else:
            sibling = self._sibling(node)
            parent = node._parent
            
            if sibling is None:
                # Case 2: Sibling is None, double black pushed up
                self._dbl_black(parent)
            else:
                if not self._is_black(sibling):
                    # Case 3: Sibling is red
                    parent._color = self._Node.RED
                    sibling._color = self._Node.BLACK
                    if sibling is sibling._parent._left:
                        self._rotate_right(parent)
                    else:
                        self._rotate_left(parent)
                    self._dbl_black(node)
                else:
                    # Case 4: Sibling is black
                    if self._is_black(sibling._left) and self._is_black(sibling._right):
                        # Case 4.1: Sibling's children are both black
                        if self._is_black(parent):
                            sibling._color = self._Node.RED
                            self._dbl_black(parent)
                        else:
                            sibling._color = self._Node.RED
                            parent._color = self._Node.BLACK
                    else:
                        # Case 4.2: Sibling's children are not both black
                        if sibling._right and not self._is_black(sibling._right):
                            # Case 4.2.1: Right child of sibling is red
                            if sibling is sibling._parent._left:
                                sibling._right._color = sibling._color
                                sibling._color = parent._color
                                self._rotate_left(parent)
                            else:
                                sibling._color = parent._color
                                parent._color = self._Node.BLACK
                                self._rotate_left(sibling)
                                self._rotate_right(parent)
                        else:
                            # Case 4.2.2: Left child of sibling is red
                            if sibling is sibling._parent._left:
                                sibling._left._color = sibling._parent._color
                                sibling._color = self._Node.BLACK
                                self._rotate_right(sibling)
                                self._rotate_left(parent)
                            else:
                                sibling._left._color = sibling._color
                                sibling._color = parent._color
                                self._rotate_right(parent)
                        parent._color = self._Node.BLACK


    # Supporting functions -- DO NOT MODIFY BELOW
    def display(self):
        print('--------------')
        self._display(self._root, 0)
        print('--------------')

    def _display(self, node, depth):
        if node == None:
            return

        if node._right != None:
            if node._right._parent != node:
                print("parent-child error - ", node._element, node._right._element)
            self._display(node._right, depth+1)

        if node == self._root:
            symbol = '>'
        else:
            symbol = '*'

        if node._color == self._Node.RED:
            colorstr = 'R'
        else:
            colorstr = 'B'
        print(f'{"    "*depth}{symbol} {node._element}({colorstr})')
        if node._left != None:
            if node._left._parent != node:
                print("parent error - ", node._element, node._left._element)
            self._display(node._left, depth+1)

    def inorder_traverse(self):
        return self._inorder_traverse(self._root)

    def _inorder_traverse(self, node):
        if node == None:
            return []
        else:
            return self._inorder_traverse(node._left) + [node._element] + self._inorder_traverse(node._right)

    def check_tree_property_silent(self):
        if self._root == None:
            return True

        if not self._check_parent_child_link(self._root):
            print('Parent-child link is violated')
            return False
        if not self._check_binary_search_tree_property(self._root):
            print('Binary search tree property is violated')
            return False
        if not self._root._color == self._Node.BLACK:
            print('Root black property is violated')
            return False
        if not self._check_double_red_property(self._root):
            print('Internal property is violated')
            return False
        if self._check_black_height_property(self._root) == 0:
            print('Black height property is violated')
            return False
        return True

    def check_tree_property(self):
        if self._root == None:
            print('Empty tree')
            return

        print('Checking binary search tree property...')
        self._check_parent_child_link(self._root)
        self._check_binary_search_tree_property(self._root)
        print('Done')

        print('Checking root black property...')
        print(self._root._color == self._Node.BLACK)
        print('Done')

        print('Checking internal property (=no double red)...')
        self._check_double_red_property(self._root)
        print('Done')

        print('Checking black height property...')
        self._check_black_height_property(self._root)
        print('Done')

    def _check_parent_child_link(self, node):
        if node == None:
            return True

        test_pass = True

        if node._right != None:
            if node._right._parent != node:
                print("parent-child error - ", node._element, node._right._element)
            test_pass = test_pass and self._check_parent_child_link(node._right)
        if node._left != None:
            if node._left._parent != node:
                print("parent error - ", node._element, node._left._element)
            test_pass = test_pass and self._check_parent_child_link(node._left)

        return test_pass

    def _check_binary_search_tree_property(self, node):
        if node == None:
            return True

        test_pass = True

        if node._left != None:
            if node._left._element > node._element:
                print("Binary search tree property error - ", node._element, node._left._element)
                return False
            test_pass = test_pass and self._check_binary_search_tree_property(node._left)

        if node._right != None:
            if node._right._element < node._element:
                print("Binary search tree property error - ", node._element, node._right._element)
                return False
            test_pass = test_pass and self._check_binary_search_tree_property(node._right)

        return test_pass

    def _check_double_red_property(self, node):
        if node == None:
            return True

        test_pass = True

        if node._color == self._Node.RED:
            if node._left != None:
                if node._left._color == self._Node.RED:
                    print("Double red property error - ", node._element, node._left._element)
                    return False
            if node._right != None:
                if node._right._color == self._Node.RED:
                    print("Double red property error - ", node._element, node._right._element)
                    return False

        if node._left != None:
            test_pass = test_pass and self._check_double_red_property(node._left)
        if node._right != None:
            test_pass = test_pass and self._check_double_red_property(node._right)

        return test_pass

    def _check_black_height_property(self, node):
        if node == None:
            return 1

        left_height = self._check_black_height_property(node._left)
        right_height = self._check_black_height_property(node._right)

        if left_height != right_height:
            print("Black height property error - ", node._element, left_height, right_height)
            return 0

        if node._color == self._Node.BLACK:
            return left_height + 1
        else:
            return left_height