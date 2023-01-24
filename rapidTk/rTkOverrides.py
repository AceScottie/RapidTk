from tkinter import Widget, Menubutton, Menu, TclError, RAISED, Misc, _setit, StringVar

class OptionMenu(Menubutton):
    """OptionMenu which allows the user to select a value from a menu."""
    def __void__(self, *args, **kwargs):
        return
    def __init__(self, master=None, cnf={}, **kw):
        """
        Override of the Tk Option Menu to support kwargs as all other widgets.
        """
        values = kw.pop('values', []) ## adds vaues kwargs
        value = kw.pop('value', None) ##adds value kwarg
        kw['borderwidth'] = kw.get('borderwidth', 2)
        variable = kw['textvariable'] = kw.pop('variable', StringVar())
        if value is not None:variable.set(value)
        kw['indicatoron'] = kw.get('indicatoron', 1)
        kw['relief'] = kw.get('relief', RAISED)
        kw['anchor'] = kw.get('anchor', "c")
        kw['highlightthickness'] = kw.get('highlightthickness', 2)
        callback = kw.get('command', self.__void__)
        if 'command' in kw:
            del kw['command']
        Widget.__init__(self, master, "menubutton", cnf, kw)

        self.widgetName = 'tk_optionMenu'
        menu = self.__menu = Menu(self, name="menu", tearoff=0)
        self.menuname = menu._w
        
        menu.add_command(label=value, command=_setit(variable, value, callback))
        for v in values:
            menu.add_command(label=v, command=_setit(variable, v, callback))
        self['menu'] = menu
    def __getitem__(self, name):
        if name == 'menu':
            return self.__menu
        return Widget.__getitem__(self, name)


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