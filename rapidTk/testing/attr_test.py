
class x:
	def __init__(self):
		self.background = "blue"
	def __setattr__(self, at, val):
		print(at)
		print(val)

y=x()
x.bg="red"