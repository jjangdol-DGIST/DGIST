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
        node = self._root
        while node is not None:
            if element < node._element:
                node = node._left
            elif element > node._element:
                node = node._right
            else:
                return node
        return None

    def insert(self, element):
        ## IMPLEMENT
        node = self._Node(element)
        if self._root is None:
            self._root = node
        else:
            parent_node = None
            current_node = self._root
            while current_node is not None:
                parent_node = current_node
                if node._element < current_node._element:
                    current_node = current_node._left
                else:
                    current_node = current_node._right
            node._parent = parent_node
            if node._element < parent_node._element:
                parent_node._left = node
            else:
                parent_node._right = node
        self._size += 1
        self._fix_insert(node)

    def delete(self, element):
        node = self.search(element)

        if node is None:
            return

        if self.is_leaf(node):
            if node._color == self._Node.RED:
                self._delete_case1(node)
            else:
                self._delete_case2(node)
        else:
            child = node._left if node._left is not None else node._right
            if node._color == self._Node.RED or child._color == self._Node.RED:
                self._replace_node(node, child)
                if child is not None:
                    child._color = self._Node.BLACK
            else:
                self._delete_case1(node)

        self._size -= 1



    # BONUS FUNCTIONS -- use them freely if you want
    def _delete_case1(self, node):
        if node._parent != None:
            self._delete_case2(node)

    def _delete_case2(self, node):
        sibling = self._sibiling(node)

        if sibling._color == self._Node.RED:
            node._parent._color = self._Node.RED
            sibling._color = self._Node.BLACK
            if node == node._parent._left:
                self._rotate_left(node._parent)
            else:
                self._rotate_right(node._parent)

        self._delete_case3(node)

    def _delete_case3(self, node):
        sibling = self._sibiling(node)
        if (node._parent._color == self._Node.BLACK and
            sibling._color == self._Node.BLACK and
            self._is_black(sibling._left) and
            self._is_black(sibling._right)):
            sibling._color = self._Node.RED
            self._delete_case1(node._parent)
        else:
            self._delete_case4(node)

    def _delete_case4(self, node):
        sibling = self._sibiling(node)
        if (node._parent._color == self._Node.RED and
            sibling._color == self._Node.BLACK and
            self._is_black(sibling._left) and
            self._is_black(sibling._right)):
            sibling._color = self._Node.RED
            node._parent._color = self._Node.BLACK
        else:
            self._delete_case5(node)

    def _delete_case5(self, node):
        sibling = self._sibiling(node)
        if sibling._color == self._Node.BLACK:
            if (node == node._parent._left and
                self._is_black(sibling._right) and
                sibling._left is not None and sibling._left._color == self._Node.RED):
                sibling._color = self._Node.RED
                sibling._left._color = self._Node.BLACK
                self._rotate_right(sibling)
            elif (node == node._parent._right and
                self._is_black(sibling._left) and
                sibling._right is not None and sibling._right._color == self._Node.RED):
                sibling._color = self._Node.RED
                sibling._right._color = self._Node.BLACK
                self._rotate_left(sibling)

        self._delete_case6(node)

    def _delete_case6(self, node):
        sibling = self._sibiling(node)
        sibling._color = node._parent._color
        node._parent._color = self._Node.BLACK

        if node == node._parent._left:
            sibling._right._color = self._Node.BLACK
            self._rotate_left(node._parent)
        else:
            sibling._left._color = self._Node.BLACK
            self._rotate_right(node._parent)

    def _replace_node(self, node, child):
        child._parent = node._parent
        if node._parent._left == node:
            node._parent._left = child
        elif node._parent._right == node:
            node._parent._right = child

    def delete_one_child(self, node):
        child = node._left if self.is_leaf(node._right) else node._right

        self._replace_node(node, child)
        if node._color == self._Node.BLACK:
            if child._color == self._Node.RED:
                child._color = self._Node.BLACK
            else:
                self._delete_case1(child)

        # node._left = node._right = node._parent = None

    def _rotate_left(self, node):
        y = node._right
        node._right = y._left
        if y._left is not None:
            y._left._parent = node
        y._parent = node._parent
        if node._parent is None:
            self._root = y
        elif node == node._parent._left:
            node._parent._left = y
        else:
            node._parent._right = y
        y._left = node
        node._parent = y

    def _rotate_right(self, node):
        y = node._left
        node._left = y._right
        if y._right is not None:
            y._right._parent = node
        y._parent = node._parent
        if node._parent is None:
            self._root = y
        elif node == node._parent._right:
            node._parent._right = y
        else:
            node._parent._left = y
        y._right = node
        node._parent = y
        
    def _fix_insert(self, node):
        while node != self._root and node._parent._color == self._Node.RED:
            if node._parent == node._parent._parent._right:
                uncle = node._parent._parent._left
                if uncle and uncle._color == self._Node.RED:
                    node._parent._color = self._Node.BLACK
                    uncle._color = self._Node.BLACK
                    node._parent._parent._color = self._Node.RED
                    node = node._parent._parent
                else:
                    if node == node._parent._left:
                        node = node._parent
                        self._rotate_right(node)
                    node._parent._color = self._Node.BLACK
                    node._parent._parent._color = self._Node.RED
                    self._rotate_left(node._parent._parent)
            else:
                uncle = node._parent._parent._right
                if uncle and uncle._color == self._Node.RED:
                    node._parent._color = self._Node.BLACK
                    uncle._color = self._Node.BLACK
                    node._parent._parent._color = self._Node.RED
                    node = node._parent._parent
                else:
                    if node == node._parent._right:
                        node = node._parent
                        self._rotate_left(node)
                    node._parent._color = self._Node.BLACK
                    node._parent._parent._color = self._Node.RED
                    self._rotate_right(node._parent._parent)
        self._root._color = self._Node.BLACK

    def is_leaf(self, node):
        return node._left is None and node._right is None

    def _is_black(self, node):
        return node == None or node._color == self._Node.BLACK

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