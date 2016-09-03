from heap import Heap

def tup_key(tup):
	return tup[1]

h = Heap(tup_key)
h.insert((0,1))
h.insert((0,3))
h.insert((0,2))
h.insert((0,4))
h.insert((0,8))
print(h)