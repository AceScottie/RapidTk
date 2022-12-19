from tkinter import *
from tkinter.ttk import Spinbox

state=False

def draw(c):
	ax, ay, bx, by = 25, 25, 75, 75
	r = (by-ay)/2
	c.create_rectangle(ax, ay, bx, by, fill="#BBBBBB", width=0, tag='aa11')
	c.create_arc(bx-r, ay, bx+r, by, start=-90, extent=180, fill="#BBBBBB", width=0, outline="#BBBBBB", tag='aa11')
	c.create_arc(ax-r, ay, ax+r, by, start=270, extent=-180, fill="#BBBBBB", width=0, outline="#BBBBBB", tag='aa11')
	c.tag_bind('aa11', '<Button-1>', lambda e=Event(), m="Clicked": print(m))

def popup(event, c):
	global state
	if state:
		return
	state=True
	print("popped")
	c.pack_propagate(False)
	c.place(x=20, y=20)
	draw(c)
def popdown(event, c):
	global state
	if not state:
		return
	state=False
	print("deleted")
	c.delete('all')
	c.place_forget()
	#c.destroy()

root=Tk()
root.geometry("500x500+100+100")
Button(root, text="do stuff").pack(side=TOP)

f= Frame(root)
f.pack()

c = Canvas(root, width=100, height=100)

s1 = Spinbox(f, wrap=True, values=tuple(list(str(x).zfill(2) for x in range(10))))
s1.pack(side=LEFT)
Label(f, text=":").pack(side=LEFT)
s2 = Spinbox(f, wrap=True, values=tuple(list(str(x).zfill(2) for x in range(10, 20))))
s2.pack()

s1.bind('<FocusIn>', lambda e=Event(), c=c: popup(e, c))
s2.bind('<FocusIn>', lambda e=Event(), c=c: popup(e, c))

root.bind('<Button-1>', lambda e=Event(), c=c: popdown(e, c))


Button(root, text="do other stuff").pack(side=TOP)

root.mainloop()