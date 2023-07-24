from tkinter.constants import *
from rapidTk import *
from rapidTk.assets.constants import DEFAULT_LIST



def clicked(event, table, data):
	print("clicked")
	print(table.focus(), table.item(table.focus())['values'])
	print(table.values)
	print(isinstance(table.values, dict))
	for i in range(5):
		print(table.values[i])
	print(table.values[int(table.focus())])



data = DEFAULT_LIST
root = rapidTk()
t = cTreeview(root, side=TOP)
cols = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
t.set_cols(cols)
tg = ["t1", "t2"]
for i, row in enumerate(data):
	print(row, i)
	t.insert(parent='',index='end',iid=i, tags=(tg[i%2],), text=row, values=row)
t.bind("<Double-1>", lambda e=Event(), t=t, d=data: clicked(e, t, d))
root.mainloop()