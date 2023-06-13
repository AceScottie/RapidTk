from tkinter import TclError, RAISED, Misc, _setit, StringVar
from tkinter.__init__ import Pack, Place, Grid
from rapidTk.tkoverride import Frame, Widget, Menubutton, Menu, Spinbox, Scrollbar, Text

from rapidTk.rTkUtils import illigalUnicode


class base:
    def __init__(self, master, *args, **kwargs):
        super(base, self).__init__()

class cMenu(Menu, base):
    #_widgetBase__widget_type = rtktypes.noget
    def __init__(self, master, **kwargs):
        super(cMenu, self).__init__(master, **kwargs)



class OptionMenu(Menubutton):
    """OptionMenu which allows the user to select a value from a menu."""
    def __void__(self, *args, **kwargs):
        return
    def __init__(self, master=None, cnf={}, **kw):
        """
        Override of the Tk Option Menu to support kwargs as all other widgets.
        """
        values = kw.pop('values', []) ## adds values kwargs
        value = kw.pop('value', None) ##adds value kwarg
        kw['borderwidth'] = kw.get('borderwidth', 2)
        variable = kw['textvariable'] = kw.pop('textvariable', StringVar(master))
        print(f"OptionMenu {value}:{values}:{variable.get()}")
        if value is not None:
            variable.set(value)
        kw['indicatoron'] = kw.get('indicatoron', 1)
        kw['relief'] = kw.get('relief', RAISED)
        kw['anchor'] = kw.get('anchor', "c")
        kw['highlightthickness'] = kw.get('highlightthickness', 2)
        callback = kw.get('command', self.__void__)
        if 'command' in kw:
            del kw['command']
        super(OptionMenu, self).__init__(master, cnf, **kw)

        self.widgetName = 'tk_optionMenu'
        menu = self.__menu = cMenu(self, name="menu", tearoff=0)
        self.menuname = menu._w
        menu.add_command(label=value, command=_setit(variable, value, callback))
        for v in values:
            menu.add_command(label=v, command=_setit(variable, v, callback))
        self['menu'] = menu
        self.update()
    def __getitem__(self, name):
        if name == 'menu':
            return self.__menu
        return super().__getitem__(self, name)
    def destroy(self):
        """Destroy this widget and the associated menu."""
        super().destroy()
        self.__menu = None
class Spinbox(Spinbox):
    """
        Override of the Tk Spinbox. Adds `values` attribute along with next() and previous() methods.
    """
    def __init__(self, master, **kwargs):
        """
        Adds values as an attribute.
        """
        self.values = kwargs.get('values', None)
        super(Spinbox, self).__init__(master, **kwargs)
    def configure(self, **kwargs):
        """
        overrides to ensure any change to values is changed with the attributes.
        """
        if 'values' in kwargs:
            self.values = kwargs.get('values')
        super().configure(**kwargs)
    def config(self, **kwargs):
        self.configure(**kwargs)
    def next(self, wrap:bool=0):
        """
        returns the next item from inputted values, if value is last in list istead wraps to first item in list.
        """
        if wrap:
            return self.values[0 if self.values.index(self.get()) >= len(self.values)-1 else self.values.index(self.get())+1]
        else:
            return self.values[self.values.index(self.get()) if self.values.index(self.get()) >= len(self.values)-1 else self.values.index(self.get())+1]
    def previous(self, wrap:bool=0):
        """
        returns the previous item from inputted values, if value is first in list istead wraps to last item in list.
        """
        if wrap:
            return self.values[len(self.values)-1 if self.values.index(self.get()) <= 0 else self.values.index(self.get())-1]
        else:
            return self.values[self.values.index(self.get()) if self.values.index(self.get()) <= 0 else self.values.index(self.get())-1]
    def spin(self, direction:bool=0, wrap:bool=0):
        """
        increments the value in the direction provided: True:up, False:down
        """
        if direction: #direction up
            self.configure(value=self.next(wrap))
        else: #direction down
            self.configure(value=self.previous(wrap))


if __name__ == "__main__":
    import tkinter as tk
    def cnf(event, menu, opt):
        print(menu['menu'])
        menu['menu'].configure(**opt)
    r = tk.Tk()
    sv = tk.StringVar()
    sv2 = tk.StringVar()
    sv2.set("test")
    o = [1, 2, 3, 4]
    om= OptionMenu(r, value='0', values=o, textvariable=sv)
    om.pack(side=tk.TOP)
    tk.Button(r, text="config", command=lambda e=tk.Event(), m=om, opt={'activebackground':'red'}:cnf(e, m ,opt)).pack(side=tk.TOP)
    r.mainloop()