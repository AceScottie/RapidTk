from random import randint

class int(int):
	def pm(self, x:int, y:int)->bool:
		"""
		self is the number input to check
		x is the midpoint of the range
		y is the range to check
		"""
		return self in list(range(x-y, x+(y+1)))

for _ in range(10):
	print(int(randint(0, 200)).pm(100, 20))
	##----psudo code
	#print(randint(0, 200) == 100+/-20)


def pm(x, y):
	return list(range(x-y, x+(y+1)))

for _ in range(10):
	print(randint(0, 200) in pm(100, 20))