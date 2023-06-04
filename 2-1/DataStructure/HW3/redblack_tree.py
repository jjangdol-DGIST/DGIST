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
        ## IMPLEMENT
        print("Do search...")
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
        print("Do insert...")
        ## IMPLEMENT
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
            self._fix_after_insert(new_node)

    def delete(self, element):
        print("Do delete...")
        ## IMPLEMENT
        node = self.search(element)
        if node is None:
            return  # Node doesn't exist, nothing to delete

        self._delete_node(node)
        self._size -= 1

    # BONUS FUNCTIONS -- use them freely if you want
    def _delete_node(self, node):
        print("Do delete node...")
        if node._left is not None and node._right is not None:
            successor = self._successor(node)
            node._element = successor._element
            node = successor

        if self._is_red(node):
            if node._parent is not None:
                if node == node._parent._left:
                    node._parent._left = None
                else:
                    node._parent._right = None
            return

        self._delete_one_child(node)

    def _delete_one_child(self, node):
        print("Do delete one child...")
        child = node._right if node._right is not None else node._left

        if node._parent is None:
            self._root = child
        else:
            if node == node._parent._left:
                node._parent._left = child
            else:
                node._parent._right = child

        if child is not None:
            child._parent = node._parent

        if not self._is_red(node):
            self._fix_after_delete(child)
            
    def _fix_after_insert(self, node):
        print("Do fix...")
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
    
    def _fix_after_delete(self, node):
        print("Do fix...")
        while node != self._root and self._is_black(node):
            if node == node._parent._left:
                sibling = node._parent._right
                if self._is_red(sibling):
                    sibling._color = self._Node.BLACK
                    node._parent._color = self._Node.RED
                    self._rotate_left(node._parent)
                    sibling = node._parent._right

                if self._is_black(sibling._left) and self._is_black(sibling._right):
                    sibling._color = self._Node.RED
                    node = node._parent
                else:
                    if self._is_black(sibling._right):
                        sibling._left._color = self._Node.BLACK
                        sibling._color = self._Node.RED
                        self._rotate_right(sibling)
                        sibling = node._parent._right

                    sibling._color = node._parent._color
                    node._parent._color = self._Node.BLACK
                    sibling._right._color = self._Node.BLACK
                    self._rotate_left(node._parent)
                    node = self._root
            else:
                sibling = node._parent._left
                if self._is_red(sibling):
                    sibling._color = self._Node.BLACK
                    node._parent._color = self._Node.RED
                    self._rotate_right(node._parent)
                    sibling = node._parent._left

                if self._is_black(sibling._right) and self._is_black(sibling._left):
                    sibling._color = self._Node.RED
                    node = node._parent
                else:
                    if self._is_black(sibling._left):
                        sibling._right._color = self._Node.BLACK
                        sibling._color = self._Node.RED
                        self._rotate_left(sibling)
                        sibling = node._parent._left

                    sibling._color = node._parent._color
                    node._parent._color = self._Node.BLACK
                    sibling._left._color = self._Node.BLACK
                    self._rotate_right(node._parent)
                    node = self._root

        if node is not None:
            node._color = self._Node.BLACK
    
    def _rotate_left(self, node):
        print("Do rotate to left...")
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
        print("Do rotate to right...")
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
    
    def _is_black(self, node):
        return node == None or node._color == self._Node.BLACK
    
    def _is_red(self, node):
        return node is not None and node._color == self._Node.RED

    def _successor(self, node):
        successor = node._right
        while successor._left != None:
            successor = successor._left
        return successor

    def _sibiling(self, node):
        parent = node._parent

        if parent._left == node:
            return parent._right
        else:
            return parent._left

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