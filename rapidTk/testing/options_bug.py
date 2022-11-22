import tkinter as tk

def open_option_menu(event):
    obj = event.widget
    x = obj.winfo_rootx()
    y = obj.winfo_rooty() + obj.winfo_height()
    obj["menu"].post(x, y)
    return "break"


root = tk.Tk()
options = ["Hello", "world", "How", "are", "you"]

v1 = tk.StringVar(root)
v2 = tk.StringVar(root)
v3 = tk.StringVar(root)

o1 = tk.OptionMenu(root, v1, *options)
o2 = tk.OptionMenu(root, v2, *options)
o3 = tk.OptionMenu(root, v3, *options)

o1.configure(takefocus=True)
o2.configure(takefocus=True)
o3.configure(takefocus=True)

o1.bind("<space>", open_option_menu)
o2.bind("<space>", open_option_menu)
o3.bind("<space>", open_option_menu)

o1.pack()
o2.pack()
o3.pack()

root.mainloop()