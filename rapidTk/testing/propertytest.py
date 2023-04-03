
class Frame:
	def __init__(self, master, **kwargs):
		print("parent initilised")
		super().__init__(master, **kwargs)
		self.master = master
		self.__dict__.update(**kwargs)

class widgetBase:
	def __init__(self,  master, **kwargs):
		print("base initilised")
		super().__init__()
		self.uid = 'Hello World'

class cFrame(Frame, widgetBase):
	def __init__(self, master, **kwargs):
		super(cFrame, self).__init__(master, **kwargs)


c1 = c('test', a=1, b=2)
print(c1.uid)
#print(c1.x, c1.y)