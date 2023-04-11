import _tkinter
from tkinter import Pack, Place, Grid, Misc, XView, YView
from tkinter import _cnfmerge

##Base Classes
class Misc(Misc):
    def __init__(self, master, widgetName, cnf={}, extra=(), **kw):
        super(Misc, self).__init__(master, widgetName, cnf, extra, **kw)
class BaseWidget(Misc):
    def _setup(self, master, cnf):
        if master is None:
            master = _get_default_root()
        self.master = master
        self.tk = master.tk
        name = None
        if 'name' in cnf:
            name = cnf['name']
            del cnf['name']
        if not name:
            name = self.__class__.__name__.lower()
            if master._last_child_ids is None:
                master._last_child_ids = {}
            count = master._last_child_ids.get(name, 0) + 1
            master._last_child_ids[name] = count
            if count == 1:
                name = '!%s' % (name,)
            else:
                name = '!%s%d' % (name, count)
        self._name = name
        if master._w=='.':
            self._w = '.' + name
        else:
            self._w = master._w + '.' + name
        self.children = {}
        if self._name in self.master.children:
            self.master.children[self._name].destroy()
        self.master.children[self._name] = self
    def __init__(self, master, widgetName, cnf={}, extra=(),  **kw):
        ##PATCH++
        super(BaseWidget, self).__init__(master, widgetName, cnf, extra, **kw)
        ##PATCH--
        if kw:
            cnf = _cnfmerge((cnf, kw))
        self.widgetName = widgetName
        self._setup(master, cnf)
        if self._tclCommands is None:
            self._tclCommands = []
        classes = [(k, v) for k, v in cnf.items() if isinstance(k, type)]
        for k, v in classes:
            del cnf[k]
        self.tk.call(
            (widgetName, self._w) + extra + self._options(cnf))
        for k, v in classes:
            k.configure(self, v)
class Widget(BaseWidget, Pack, Place, Grid):
    def __init__(self, master=None, widgetName=None, cnf={}, extra=(), **kw):
        super(Widget, self).__init__(master, widgetName, cnf, extra, **kw)
##Widgets
class Frame(Widget):
    def __init__(self, master=None, cnf={}, extra=(), **kw):
        cnf = _cnfmerge((cnf, kw))
        extra = (cnf.pop('class_', cnf.pop('class', ())))
        super(Frame, self).__init__(master, 'frame', cnf, extra, **kw)
class Button(Widget):
    def __init__(self, master=None, cnf={}, **kw):
        super(Button, self).__init__(master, 'button', cnf, (), **kw)
class Canvas(Widget, XView, YView):
    def __init__(self, master=None, cnf={}, **kw):
        super(Canvas, self).__init__(master, 'canvas', cnf, (), **kw)
class Checkbutton(Widget):
    def __init__(self, master=None, cnf={}, **kw):
        super(Checkbutton, self).__init__(master, 'checkbutton', cnf, (), **kw)
class Entry(Widget):
    def __init__(self, master=None, cnf={}, **kw):
        super(Entry, self).__init__(master, 'entry', cnf, (), **kw)
class Label(Widget):
    def __init__(self, master=None, cnf={}, **kw):
        super(Label, self).__init__(master, 'label', cnf, (), **kw)
class Listbox(Widget, XView):
    def __init__(self, master=None, cnf={}, **kw):
        super(Listbox, self).__init__(master, 'listbox', cnf, (), **kw)
class Menu(Widget):
    def __init__(self, master=None, cnf={}, **kw):
        super(Menu, self).__init__(master, 'menu', cnf, (), **kw)
class Menubutton(Widget):
    def __init__(self, master=None, cnf={}, **kw):
        super(Menubutton, self).__init__(master, 'menubutton', cnf, (), **kw)
class Message(Widget):
    def __init__(self, master=None, cnf={}, **kw):
        super(Message, self).__init__(master, 'message', cnf, (), **kw)
class Radiobutton(Widget):
    def __init__(self, master=None, cnf={}, **kw):
        super(Radiobutton, self).__init__(master, 'radiobutton', cnf, (), **kw)
class Scale(Widget):
    def __init__(self, master=None, cnf={}, **kw):
        super(Scale, self).__init__(master, 'scale', cnf, (), **kw)
class Scrollbar(Widget):
    def __init__(self, master=None, cnf={}, **kw):
        super(Scrollbar, self).__init__(master, 'scrollbar', cnf, (), **kw)
class Text(Widget, XView, YView):
    def __init__(self, master=None, cnf={}, **kw):
        super(Text, self).__init__(master, 'text', cnf, (), **kw)
class Spinbox(Widget, XView):
    def __init__(self, master=None, cnf={}, **kw):
        super(Spinbox, self).__init__(master, 'spinbox', cnf, (), **kw)
class LabelFrame(Widget):
    def __init__(self, master=None, cnf={}, **kw):
        super(LabelFrame, self).__init__(master, 'labelframe', cnf, (), **kw)
class PanedWindow(Widget):
    def __init__(self, master=None, cnf={}, **kw):
        super(PanedWindow, self).__init__(master, 'panedwindow', cnf, (), **kw)
