from tkinter.constants import *
from rapidTk import *


def packer(w):
	w.pack(side=TOP)

root = rapidTk()

options = ['Hello', 'World', 'How', 'Are', 'You']

o1 = reOptionMenu(root, value=options[0], options=options, non_valid=['World'], side=TOP)
o2 = cOptionMenu(root, value=options[0], options=options)
edits = {}
profile_data = {"data":{'gender':'Male'}}
edits['genderE'] = reOptionMenu(root, value=profile_data['data']["gender"], options=["Female", "Male", "Other"])

b=cButton(root, text="pack", command=lambda w=edits['genderE'] :packer(w), side=BOTTOM)

root.mainloop()