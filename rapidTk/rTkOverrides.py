from tkinter import Widget, Menubutton, Menu, TclError, RAISED, Misc, _setit, StringVar

class OptionMenu(Menubutton):
    """OptionMenu which allows the user to select a value from a menu."""
    def __init__(self, master=None, cnf={}, **kw):
        """
        Override of the Tk Option Menu to support kwargs as all other widgets.
        """
        values = kw.pop('values', []) ## adds vaues kwargs
        value = kw.pop('value', None) ##adds value kwarg
        kw['borderwidth'] = kw.get('borderwidth', 2)
        variable = kw['textvariable'] = kw.pop('variable', StringVar())
        variable.set(value)
        kw['indicatoron'] = kw.get('indicatoron', 1)
        kw['relief'] = kw.get('relief', RAISED)
        kw['anchor'] = kw.get('anchor', "c")
        kw['highlightthickness'] = kw.get('highlightthickness', 2)
        callback = kw.pop('command', None)
        Widget.__init__(self, master, "menubutton", cnf, kw)
        self.widgetName = 'tk_optionMenu'
        menu = self.__menu = Menu(self, name="menu", tearoff=0)
        self.menuname = menu._w
        menu.add_command(label=value,
                 command=_setit(variable, value, callback))
        for v in values:
            menu.add_command(label=v,
                     command=_setit(variable, v, callback))
        self["menu"] = menu