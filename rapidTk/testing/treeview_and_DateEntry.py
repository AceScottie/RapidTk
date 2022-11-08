import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        button1 = tk.Button(self, text='open topwindow', command=(lambda: self.controller.click()))
        button1.grid(row=0, column=0, sticky=tk.NSEW, padx=4, pady=4)
        self.tree = ttk.Treeview(self, selectmode='browse', columns=('col1', 'col2', 'col3'), show='headings', height=20)
        cols_names = [('col1', 'column 1'), ('col2', 'column 2'), ('col3', 'column 3')]
        for (name, txt) in cols_names:
            self.tree.heading(name, text = txt)
            self.tree.column(name, width = 100, anchor=tk.CENTER)
        self.tree.grid(row=1, column=0, sticky=tk.NSEW, padx=4, pady=4)

    def main(self):
        self.mainloop()

class PopUp(tk.Toplevel):
    def __init__(self, controller, parent):
        super().__init__(parent)
        self.controller = controller
        entry7 = DateEntry(self, date_pattern='dd/mm/yy')
        entry7.grid(row=0, column=0, sticky=tk.NSEW, padx=4, pady=4)
        button1 = tk.Button(self, text='exit', command=(lambda: self.destroy()))
        button1.grid(row=1, column=0, sticky=tk.NSEW, padx=4, pady=4)

class Controller:
    def __init__(self):
        self.view = View(self)

    def main(self):
        self.view.main()
    
    def click(self):
        print(f'height before: {self.view.winfo_height()}, width before: {self.view.winfo_width()}')
        window = PopUp(self, self.view)
        window.grab_set()
        window.wait_window()
        print(f'height after: {self.view.winfo_height()}, width after: {self.view.winfo_width()}')
        
if __name__ == "__main__":
    app = Controller()
    app.main()