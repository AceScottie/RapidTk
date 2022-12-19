import base64
import tkinter as tk
from tkinter.ttk import *

class Images(dict):
    def __init__(self) -> None:
        self['addUser']= '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'


class Window1:

    def __init__(self) -> None:
        self.windowConfig()
        self.widgets()

    def windowConfig(self):
        self.window_menu = tk.Tk()
        self.window_menu.title('Window Main')
        self.window_menu.geometry('200x200')
            
    def widgets(self):
        frame = tk.Frame(self.window_menu, background='Green')
        frame.pack()
        butt = Botoes(local=frame, img='addUser', command=Window2)
        butt.localization()
        
        self.window_menu.mainloop()


class Window2:
    def __init__(self) -> None:
        self.windowConfig()
        self.widgets()

    def windowConfig(self):
        self.window_secundary = tk.Toplevel()
        self.window_secundary.title('Window Secundary')
        self.window_secundary.geometry('200x200')        

    def widgets(self):
        frame = tk.Frame(self.window_secundary, background='Green')
        frame.pack()
        butt = Botoes(local=frame, img='addUser')
        butt.localization()


class Botoes(Button):
    def __init__(self, local, img=None, line=0, col=0, command=None) -> None:
        self.__local = local
        self.__img = img
        self.__line = line
        self.__col = col
        self.__command = command
        
        super(Botoes, self).__init__(local)
        self.image_b64 = Images()[img]
        self.img = tk.PhotoImage(data=base64.b64decode(self.image_b64))
        self.configure(image=self.img, command=self.__command)
    
        style = Style()
        style.theme_use("default")

        # Styles
        style.configure('TButton', background='#4F4F4F')
        style.map('TButton', background=[('active', '#00FA9A')])

    def localization(self) -> None:
        self.grid(row=self.__line, column=self.__col)



Window1()