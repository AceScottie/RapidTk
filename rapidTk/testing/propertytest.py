from tkinter import *
from tkinter import Button as tkButton
from rapidTk.tkoverride import Frame, Button
from uuid import uuid4
class baseWidget:
	def __init__(self, master, *args, **kwargs):
		super().__init__()
		print("custom baseWidget Initialised")
		self.__unique_id = uuid4() ##example why its needed

class b:
	def __init__(self, master, **kwargs):
		print("b __init__")

class ca(b):
	def __init__(self, master, **kwargs):
		print("a Initialised")
		super(ca, self).__init__(master, **kwargs)

class cFrame(Frame, baseWidget):
#class cFrame(ca, baseWidget):
	def __init__(self, master, **kwargs):
		print("cFrame Initialised")
		super(cFrame, self).__init__(master, **kwargs)
		#baseWidget.__init__(self, master, **kwargs)
class cButton(Button, baseWidget):
#class cFrame(ca, baseWidget):
	def __init__(self, master, **kwargs):
		print("cFrame Initialised")
		super(cButton, self).__init__(master, **kwargs)
		#baseWidget.__init__(self, master, **kwargs)

a=1
if a:
	root = Tk()
	root.geometry("400x400")
	f = cFrame(root, bg="red")
	f.pack(side=TOP, fill=X, expand=1)

	b = tkButton(f, text="submit")
	b.pack(side=TOP)

	root.mainloop()
else:
	cFrame('test', a=1, b=2)