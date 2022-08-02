

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
	x.create()
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


	root.mainloop()