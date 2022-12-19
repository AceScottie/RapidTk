from tkinter import *
from rapidTk import *

def example_TimePicker():
	"""
	@DOCSTR - Here

	"""
	root = rapidTk()
	root.geometry("500x500+300+300")
	f = cFrame(root, side=TOP, expand=1, fill=BOTH)
	cButton(f, text="test", side=TOP)

	f2 = cFrame(f, bg="red", side=TOP)
	
	b = TimePicker(f2)
	b.pack(side=TOP)

	cButton(f, text="test", side=TOP)
	root.mainloop()


if __name__ == "__main__":
	example_TimePicker()
