import sys

class Template():

    def __init__(self, value, key = None):
      self.value = value
      self.key = key

    def get_value(self):
      if self.key == None:
      	return self.value
      else:
        return self.key(self.value)

    def __lt__(self, other):
      if self.key == None:
        return self.value < other.value
      else:
        return self.key(self.value) < self.key(other.value)

    def ___le__(self, other):
      if self.key == None:
        return self.value <= other.value
      else:
        return self.key(self.value) <= self.key(other.value)
    
    def __eq__(self, other):
      if self.key == None:
        return self.value == other.value
      else:
        return self.key(self.value) == self.key(other.value)
 
    def __ne__(self, other):
      if self.key == None:
        return self.value != other.value
      else:
        return self.key(self.value) != self.key(other.value)
    
    def __gt__(self, other):
      if self.key == None:
        return self.value > other.value
      else:
        return self.key(self.value) > self.key(other.value)

    def __ge__(self, other):
      if self.key == None:
      	#print(other)
        return self.value >= other.value
      else:
        return self.key(self.value) >= self.key(other.value)

class Heap():

	# Fast, efficient, binary heap, built on top of list
	# minimum heap by default

	#@staticmethod
	#def maxheap(a,b):
	#	return a > b

	#def minheap(a,b):
	#	return a < b

	#TODO - add support for maxheap


	'''
	We build the heap as a complete binary tree, with list as internal representation.
	The representation is as follows:
	If a node is at index k:
	the left child is at index 2*k
	the right child is at index 2*k+1
	the parent is at k//2,
	assuming: 0 < 2*k < 2*k+1 <= size and k//2 > 0
	No node will have a right child before it has a left child. In complete binary tree,
	levels are always filled from left to right and tree is always well-balanced.
	Of course, we could have built this as a binary tree with every node having a link
	to its parent. That seems a bit more intuitive and we don't have to worry about indexing
	through the list.
	'''

	def __init__(self, key_func = None):
		# the entire implementation is OBO if not for this dummy element
		# We can choose not to use zero as dummy element to make 1-based array, otherwise,
		# without this dummy element, left child is @ 2i+1, right child @ 2i+2
		self.heap = [0] 
		self.size = 0
		self.key_func = key_func

	''' Get top element, but doesn't remove it '''
	def peek(self):
		if self.isEmpty():
			return None
		return self.heap[1]

	def __contains__(self, elem):
		return elem in self.heap

	'''
	Whenever we insert a element at the end of the heap, we have to rearrange the heap in bottom-up fashion
	by doing a swap at each node if and only if the current child is less or equal to than its parent
	We stop by arriving at root, or when child is greater than parent.
	'''
	def heapifyUp(self, child):
		while child // 2 > 0:
			# if key is less than its parent, do basic swap
			# if not, we are done
			if self.heap[child] <= self.heap[child // 2]:
				self.swap(child//2, child)
			else:
				break
			# this is how we get parent of current node
			child //= 2

	'''
	Same as above method, except in top-down fashion, so comparing with children instead of parents
	Used whenever we delete the min
	'''
	def heapifyDown(self, parent):
		while (parent*2) <= len(self):
		
			minChild = self.getChildForSwap(parent)
			# if no need to swap, we are done rearranging heap
			if self.heap[parent] > self.heap[minChild]:
				self.swap(parent, minChild)
			else:
				break

			parent = minChild

	'''
	As we are rearranging the heap in a top-down fashion, we swap with the node that is minimum
	of its left and right child, in order to preserve the heap ordering property.
	'''
	def getChildForSwap(self, i):
		left = 2*i
		right = 2*i+1
		if right > self.size:
			return left # we return left child if right is None

		#otherwise, we do comparison as normal and get min child
		if self.heap[left] < self.heap[right]:
			return left
		return right

	''' Save then delete the minimum, swap first and last element, then rearrange the heap '''
	def pop(self):
		if self.isEmpty():
			return
		minimum = self.peek()
		self.swap(1,-1) # swap first and last element
		self.heap.pop()
		self.size -= 1
		self.heapifyDown(1)
		return minimum

	def isEmpty(self):
		return self.size == 0 # 1 for our dummy element

	def __len__(self):
		return self.size

	''' 
	Builds a heap from a list of keys. We initialize the list, then starting at the halfway point of the array. 
	Every node after this one will have no children, so we want to heapify down for every node BEFORE this node
	We rearrange the heap in a bottom-up fashion, rearranging the parents,so as to place the maximally valued
	elements towards the bottom. 
	'''
	def buildHeap(self, a):
		self.heap = [0] + a[:]
		self.size = len(a)
		for node in a:
			node = Template(node, self.key_func)

		for parent in range(len(a)//2, 0, -1):
			self.heapifyDown(parent)



	''' 
	To Insert a key, we append it to the list, increment size, and then rearrange the heap
	to put the element in the proper place, thus maintaining the heap order property
	'''
	def insert(self, key):
		self.heap.append(Template(key, self.key_func))
		self.size += 1
		self.heapifyUp(self.size)



	''' Basic swap algorithm of two nodes in the heap '''
	def swap(self, i, j):
		self.heap[i],self.heap[j] = self.heap[j],self.heap[i]




	'''	
	How we print the heap, print each key with its children ('' for null children)
	Useful for visual representation of the heap, on paper or whiteboard, etc
	Note: no key after index=(size/2) has children, so we simply print remaining keys
	'''
	def __str__(self):
		size = len(self)
		tree = ''
		for k in xrange(1,size/2+1):
			node = self.heap[k]
			left = self.heap[2*k] if 2*k <= size else ''
			right = self.heap[2*k+1] if 2*k+1 <= size else ''
			tree += "node: " + str(node.get_value()) + ", left: " + str(left.get_value()) + ", right: " + str(right.get_value()) + '\n'
		return tree

	'''
	Exhaustively traverse entire heap to ensure every subtree is ordered properly
	quits upon first error. We can use index=startIndex and size= heapsize/2.
	'''
	def isHeapRec(self, index, size):
		if index >= size:
			return True
		node = self.heap[index]
		# if either left or right are None, we have sys.maxint as the default value
		# so our statement is true if either or both children are None
		left = self.heap[2*index] if 2*index < size else sys.maxint
		right = self.heap[2*index+1] if 2*index+1 < size else sys.maxint
		return left >= node and right >= node and self.isHeapRec(2*index, size) and self.isHeapRec(2*index+1, size)

	def isHeap(self):
		return self.isHeapRec(1, len(self)/2+1)