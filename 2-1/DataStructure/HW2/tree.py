# Copyright 2013, Michael H. Goldwasser
#
# Developed for use with the book:
#
#        Data Structures and Algorithms in Python
#        Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser
#        John Wiley & Sons, 2013
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.    If not, see <http://www.gnu.org/licenses/>.

import collections
class Tree:
    """Abstract base class representing a tree structure."""

    #------------------------------- nested Position class -------------------------------
    class Position:
        """An abstraction representing the location of a single element within a tree.

        Note that two position instaces may represent the same inherent location in a tree.
        Therefore, users should always rely on syntax 'p == q' rather than 'p is q' when testing
        equivalence of positions.
        """

        def element(self):
            """Return the element stored at this Position."""
            raise NotImplementedError('must be implemented by subclass')

        def __eq__(self, other):
            """Return True if other Position represents the same location."""
            raise NotImplementedError('must be implemented by subclass')

        def __ne__(self, other):
            """Return True if other does not represent the same location."""
            return not (self == other)                        # opposite of __eq__

    # ---------- abstract methods that concrete subclass must support ----------
    # 오버라이딩
    def root(self):
        """Return Position representing the tree's root (or None if empty)."""
        raise NotImplementedError('must be implemented by subclass')

    def parent(self, p):
        """Return Position representing p's parent (or None if p is root)."""
        raise NotImplementedError('must be implemented by subclass')

    def num_children(self, p):
        """Return the number of children that Position p has."""
        raise NotImplementedError('must be implemented by subclass')

    def children(self, p):
        """Generate an iteration of Positions representing p's children."""
        raise NotImplementedError('must be implemented by subclass')

    def __len__(self):
        """Return the total number of elements in the tree."""
        raise NotImplementedError('must be implemented by subclass')

    # ---------- concrete methods implemented in this class ----------
    def is_root(self, p):
        """Return True if Position p represents the root of the tree."""
        return self.root() == p # Is the 'p' root?

    def is_leaf(self, p):
        """Return True if Position p does not have any children."""
        return self.num_children(p) == 0 # 자녀가 없는가?

    def is_empty(self):
        """Return True if the tree is empty."""
        return len(self) == 0 # 비었나?

    def depth(self, p):
        """Return the number of levels separating Position p from the root."""
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    def _height(self, p):                                    # time is linear in size of subtree
        """Return the height of the subtree rooted at Position p."""
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self._height(c) for c in self.children(p))

    def height(self, p=None):
        """Return the height of the subtree rooted at Position p.

        If p is None, return the height of the entire tree.
        """
        if p is None:
            p = self.root()
        return self._height(p)                # start _height2 recursion

    def __iter__(self):
        """Generate an iteration of the tree's elements."""
        for p in self.positions():     # use same order as positions()
            yield p.element()          # but yield each element

    def positions(self):
        """Generate an iteration of the tree's positions."""
        return self.preorder()         # return entire preorder iteration

    def preorder(self):
        """Generate a preorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):    # start recursion
                yield p

    def _subtree_preorder(self, p):
        """Generate a preorder iteration of positions in subtree rooted at p."""
        yield p                       # visit p before its subtrees
        for c in self.children(p):                 # for each child c
            for other in self._subtree_preorder(c):              # do preorder of c's subtree
                yield other                                               # yielding each to our caller

    def postorder(self):
        """Generate a postorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):    # start recursion
                yield p

    def _subtree_postorder(self, p):
        """Generate a postorder iteration of positions in subtree rooted at p."""
        for c in self.children(p):       # for each child c
            for other in self._subtree_postorder(c):  # do postorder of c's subtree
                yield other      # yielding each to our caller
        yield p             # visit p after its subtrees
        
    def levelorder(self):
        """Generate a levelorder iteration of positions in the tree."""
        """The running time of this level-order traversal should be O(n) """
        if not self.is_empty(): # 트리가 비어있는가? -> 비어있지 않음
            queue = collections.deque() 
            queue.append(self.root()) # 루트위치를 큐에 추가
            while len(queue) > 0: # 이진 트리의 모든 노드를 레벨 순서에 따라 탐색 할 수 있다; O(n).
                current_position = queue.popleft()
                yield current_position
                for child in self.children(current_position):
                    queue.append(child)
        # HOMEWORK 2-1.
        # raise NotImplementedError('HOMEWORK 2-2')