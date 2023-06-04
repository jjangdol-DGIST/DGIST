from tree import Tree

class LinkedTree(Tree):
    """Linked representation of a general tree structure."""

    #-------------------------- nested _Node class --------------------------
    class _Node:
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_children' # streamline memory usage

        def __init__(self, element, parent=None, children=None):
            self._element = element # the element of this node
            self._parent = parent # a link towards the parent
            if children == None: 
                self._children = []
            else:
                self._children = children # list of links towards children nodes

    #-------------------------- nested Position class --------------------------
    class Position(Tree.Position):
        """An abstraction representing the location of a single element."""

        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container # '_container' 속성을 'container' 변수의 값으로 설정
            self._node = node # _node의 속성을 node 변수의 값으로 설정

        def element(self):
            """Return the element stored at this Position."""
            return self._node._element

        def __eq__(self, other):
            """Return True if other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node # 객체의 타입이 동일한지, 동일한 노드를 참조하는지 확인, True반환

    #------------------------------- utility methods -------------------------------
    def _validate(self, p):
        """Return associated node, if position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:            # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """Return Position instance for given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None # 노드가 존재한다면 self.Position(self, node)를 반환, 아니면 None을 반환

    #-------------------------- Tree constructor --------------------------
    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    #-------------------------- public accessors --------------------------    
    def root(self):
        """Return the root Position of the tree (or None if tree is empty)."""
        return self._make_position(self._root)

    def parent(self, p):
        """Return the Position of p's parent (or None if p is root)."""
        node = self._validate(p)
        return self._make_position(node._parent) # p의 부모를 반환

    def num_children(self, p):
        """Return the number of children of Position p."""
        node = self._validate(p)
        return len(node._children) 
    
    def children(self, p):
        """특정 노드의 자식 노드들을 제너레이터(generator)를 이용하여 순회하고 반환"""
        node = self._validate(p)
        for child in node._children:
            yield self._make_position(child) # 자식 노드들을 반환

    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size # 길이를 반환
    
    #-------------------------- nonpublic mutators --------------------------
    def _add_root(self, e):
        #  This method places element 'e' at the root of an empty tree and returns the new Position.
        #  If the tree is not empty, it raises a ValueError with the message 'Root exists'.
        if self._root is not None:
            raise ValueError("Root exists")
        self._root = self._Node(e)
        self._size = 1
        return self._make_position(self._root) # (use self._make_position(node) to pack the Node object into a position.)
        # raise NotImplementedError('HOMEWORK 2-1')

    def _add_child(self, p, e):
        # This method creates a new child node for the given Position 'p' and stores the element 'e'.
        node = self._validate(p) #  (use self._validate(position) to unpack the node inside the position.)
        new_child = self._Node(e, parent=node)
        node._children.append(new_child)
        self._size += 1
        return self._make_position(new_child) # It returns the Position of the newly created node (use self._make_position(new_node)).
        # raise NotImplementedError('HOMEWORK 2-1')

    def _replace(self, p, e):
        node = self._validate(p)
        old_element = node._element
        node._element = e # This method replaces the element at the given Position 'p' with the new element 'e'.
        return old_element # It returns the old element that was replaced.
        # raise NotImplementedError('HOMEWORK 2-1')

    def _delete(self, p):
        # This method deletes the node at the given Position 'p', and returns the element that had been stored at Position 'p'.
        # If the position 'p' has any children, a ValueError is raised.
        node = self._validate(p)
        
        # if node._children is not None:
        if self.num_children != 0:
            raise ValueError # If the position 'p' has any children, a ValueError is raised.
        if node._parent is not None:
            node._parent._children.remove(node)
        else:
            self._root = None
        self._size -= 1
        node._parent = node  # Convention for deprecated nodes
        return node._element
        # raise NotImplementedError('HOMEWORK 2-1')