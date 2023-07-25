from tkinter.constants import *
from rapidTk import *


def check(entry):
	print(entry.get())

root = rapidTk()

e1 = typedEntry(root, max=3, type='float', side=TOP)
cButton(root, text="test", command=lambda e=e1:check(e), side=TOP)

root.mainloop()