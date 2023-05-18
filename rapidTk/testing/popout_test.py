from tkinter.constants import *
from rapidTk import *





root = rapidTk()
def from_path(window, p):
	print(f"getting from path {p}")
	return window.nametowidget(p)

def test(event, base, widget):
	print(base.popped)
	print(widget.rel(base.body))
	if base.popped is not None:
		for c in base.popped.winfo_children():
			print(c)
		w = from_path(base.popped, str(base.popped)+widget.rel(base))
		print(f"from path:{w}")
		w.configure(bg="red")

print(root.option_get('background', '.'))
root.geometry("800x800+100+100")
a = movableWindow(root, title="test", width=400, height=400)

b=cEntry(a.body, side=TOP)

print(b.rel(a.body)) ##relative path of w

cButton(root, text="test", command=lambda e=Event(), h=a, w=b:test(e,h,b), side=TOP)


root.mainloop()