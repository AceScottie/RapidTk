from rTk.src import rapidTk
from rTk.src.objects import cFrame, cLabel, cOptionMenu
from rTk.src.objects_ext import movableWindow, scrollArea
from rTk.src.validated_objects import reOptionMenu
from tkinter import TOP, LEFT, RIGHT, BOTTOM, CENTER, X, Y, BOTH, END, INSERT, StringVar, IntVar

if __name__ == "__main__":
	#x=_UniqueIdentifiers()
	#x.append(0)
	#x.append(0)
	#print(x)
	root = rapidTk()
	root.geometry("500x500+100+100")
	root.update()
	print(root)
	a = cFrame(root, side=TOP,  fill=BOTH, expand=1)

	##EXAMPLE moveable window
	x=movableWindow(a, title="Hello", width=300, height=300, bg="#FFFFFF", fg="#000000")
	#for i in range(100):
	#	cLabel(x.body, text="Hello %s"%i, side=TOP)
	##example autocomplete:
	#opts = ["Apple", "Banana", "Pear", "grape", "Soft Banana", "Hard Apple"]
	#e = autoEntry(a, width=15, auto=opts, side=LEFT)
	
	##EXAMPLE scroll areas
	s = scrollArea(x.body, side=TOP,  h=1, v=1, fill=BOTH, expand=1)
	root.sm.add(s.sCanvas)
	f = []
	for i in range(10):
		f.append(cFrame(s.sFrame, side=LEFT))
	for p in f:
		for i in range(50):
			cLabel(p, text="Hello %s"%i, side=TOP)

	##EXAMPLE treeview
	#x = cTreeview(root, side=TOP)
	#x.set_cols(["test"])
	#for i in range(100):
	#	x.insert("", "end", value=["test"])

	x = cOptionMenu(a, options=['1', '2', '3', '4'], side=TOP)

	y = reOptionMenu(a, options=[1, 2, 3, 4, 5], non_valid=[5, 4, 6], side=TOP)
	y.get_root()
	print(y.get_master())
	print(y.get_self())
	root.mainloop()