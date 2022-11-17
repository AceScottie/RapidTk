from rapidTk import *
from tkinter import *
from tkinter import ttk


def skillUsed():
    if chkUsedVar.get() == 1:
        style.map('custom.TCombobox', fieldbackground=[('readonly','green')])
        style.map('custom.TCombobox', foreground=[('readonly','red')])
    else:
        style.map('custom.TCombobox', fieldbackground=[('readonly','white')])
        style.map('custom.TCombobox', foreground=[('readonly','black')])

root = rapidTk()

style = root.thm.style
root.thm.set_theme('clam')

cboxVar1 = StringVar()
cboxVar1.set("spam")

cboxVar2 = StringVar()
cboxVar2.set("silly")

chkUsedVar = IntVar()
chk = cCheckbutton(root, text='Used', variable=chkUsedVar, command=skillUsed)
chk.grid(row=0, column=2)

combo01 = cCombobox(root, values=['spam', 'eric', 'moose'])
combo01['state'] = 'readonly'
combo01.grid(row=0, column=0)

combo02 = cCombobox(root, values=['parrot', 'silly', 'walk'])
combo02.configure(style='custom.TCombobox')
combo02['state'] = 'readonly'
combo02.grid(row=0, column=1)

root.mainloop()