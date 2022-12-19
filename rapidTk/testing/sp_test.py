from tkinter import *
from tkinter.ttk import Spinbox

class xSpinbox(Spinbox):
	def __init__(self, master, **kwargs):
		kwargs['command'] = kwargs.pop('command', self.__loop)
		kwargs['values'] = kwargs.pop('values', (0, 1, 2, 3, 4,5, 6, 7, 8, 9))
		super(xSpinbox, self).__init__(master, **kwargs)
		self.bind('<MouseWheel>', self.__loop) ##?? why do i need this ?

	def __loop(self, event=None):
		self.focus_set()
		self.selection_range(0, 0)

if __name__ == "__main__":
	root=Tk()
	sv = StringVar()
	sv.set('00')
	holder_frame= Frame(root)
	holder_frame.pack(side=TOP)
	sp = xSpinbox(holder_frame, textvariable = sv, wrap=True, state="readonly", exportselection=0, width=3, increment=1, values=tuple(list(str(x).zfill(2) for x in range(0, 24))))
	sp.pack(side=TOP)
	root.mainloop()

