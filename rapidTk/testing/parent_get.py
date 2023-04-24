class a:
	def __init__(self):
		super().__init__()
		print("a init")
		self.i = 1
	def test(self):
		return "testing a"
	def get(self, index=0, end=0):
		st = "Hello World"
		return st[index:end if end !=0 else len(st)], self.i, self.test()

class b:
	def __init__(self):
		print("b init")
		super().__init__()
		self.i = 2
	def test2(self):
		return "testing b"
	def get(self, index=0, end=0):
		st = "Goodbye Space"
		return st[index:end if end !=0 else len(st)], self.i, self.test2()

class x(a, b):
	def __init__(self):
		super(x, self).__init__()
	def get(self):
		return b.get(self)
class y(a, b):
	def __init__(self):
		super(y, self).__init__()
class z(a, b):
	def __init__(self):
		super(z, self).__init__()

c1 = x()
c2 = y()
c3 = z()
print(c1.get())
print(c2.get())
print(c3.get())
