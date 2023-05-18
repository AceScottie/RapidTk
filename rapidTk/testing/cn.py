from tkinter import *
from so_clone import clone_widget

def test(event, widget):
    print(widget.get())
def clone(event, widget, root):
    t= Toplevel(root)
    c = clone_widget(widget, t)
    c.pack(side=TOP)

root = Tk()
f = Frame(root)
f.pack(side=TOP, fill=BOTH, expand=1)
e = Entry(f)
e.pack(side=TOP)
Button(f, text="print", command=lambda e=Event(), w=e:test(e, w)).pack(side=BOTTOM)

Button(root, text="clone", command=lambda e=Event(), c=f, r=root:clone(e, c, r)).pack(side=BOTTOM)


root.mainloop()