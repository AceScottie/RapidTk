from tkinter.__init__ import Pack, Place, Grid, _cnfmerge
from tkinter.__init__ import Frame, Button, Canvas, Checkbutton, Entry, Label, Listbox, Menu, Menubutton, Message 
from tkinter.__init__ import Radiobutton, Scale, Scrollbar, Text, Scale, Spinbox, LabelFrame, PanedWindow
from tkinter.__init__ import Misc as tkMisc
##Base Classes
class Misc(tkMisc):
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
    def destroy(self):
        """Destroy this and all descendants widgets."""
        for c in list(self.children.values()): c.destroy()
        self.tk.call('destroy', self._w)
        if self._name in self.master.children:
            del self.master.children[self._name]
        Misc.destroy(self)

    def _do(self, name, args=()):
        # XXX Obsolete -- better use self.tk.call directly!
        return self.tk.call((self._w, name) + args)
class Widget(BaseWidget, Pack, Place, Grid):
    def __init__(self, master=None, widgetName=None, cnf={}, extra=(), **kw):
        super(Widget, self).__init__(master, widgetName, cnf, extra, **kw)

##Widget Monkey Patched
def f__init__(self, master=None, cnf={}, extra=(), **kw):
    cnf = _cnfmerge((cnf, kw))
    extra = (cnf.pop('class_', cnf.pop('class', ())))
    super(Frame, self).__init__(master, 'frame', cnf, extra, **kw)
Frame.__bases__ = (Widget,)
Frame.__init__ = f__init__

def b__init__(self, master=None, cnf={}, **kw):
    super(Button, self).__init__(master, 'button', cnf, (), **kw)
Button.__bases__ = (Widget,)
Button.__init__ = b__init__

def cv__init__(self, master=None, cnf={}, **kw):
    super(Canvas, self).__init__(master, 'canvas', cnf, (), **kw)
Canvas.__bases__ = (Widget,)
Canvas.__init__ = cv__init__

def cb__init__(self, master=None, cnf={}, **kw):
    super(Checkbutton, self).__init__(master, 'checkbutton', cnf, (), **kw)
Checkbutton.__bases__ = (Widget,)
Checkbutton.__init__ = cb__init__

def e__init__(self, master=None, cnf={}, **kw):
    super(Entry, self).__init__(master, 'entry', cnf, (), **kw)
    Button.__bases__ = (Widget,)
Entry.__bases__ = (Widget,)
Entry.__init__ = e__init__

def l__init__(self, master=None, cnf={}, **kw):
    super(Label, self).__init__(master, 'label', cnf, (), **kw)
Label.__bases__ = (Widget,)
Label.__init__ = l__init__

def lb__init__(self, master=None, cnf={}, **kw):
     super(Listbox, self).__init__(master, 'listbox', cnf, (), **kw)
Listbox.__bases__ = (Widget,)
Listbox.__init__ = lb__init__

def m__init__(self, master=None, cnf={}, **kw):
     super(Menu, self).__init__(master, 'menu', cnf, (), **kw)
Menu.__bases__ = (Widget,)
Menu.__init__ = m__init__

def mb__init__(self, master=None, cnf={}, **kw):
     super(Menubutton, self).__init__(master, 'menubutton', cnf, (), **kw)
Menubutton.__bases__ = (Widget,)
Menubutton.__init__ = mb__init__

def msg__init__(self, master=None, cnf={}, **kw):
     super(Message, self).__init__(master, 'message', cnf, (), **kw)
Message.__bases__ = (Widget,)
Message.__init__ = msg__init__

def rb__init__(self, master=None, cnf={}, **kw):
     super(Radiobutton, self).__init__(master, 'radiobutton', cnf, (), **kw)
Radiobutton.__bases__ = (Widget,)
Radiobutton.__init__ = rb__init__

def sc__init__(self, master=None, cnf={}, **kw):
     super(Scale, self).__init__(master, 'scale', cnf, (), **kw)
Scale.__bases__ = (Widget,)
Scale.__init__ = sc__init__

def sb__init__(self, master=None, cnf={}, **kw):
     super(Scrollbar, self).__init__(master, 'scrollbar', cnf, (), **kw)
Scrollbar.__bases__ = (Widget,)
Scrollbar.__init__ = sb__init__

def t__init__(self, master=None, cnf={}, **kw):
     super(Text, self).__init__(master, 'text', cnf, (), **kw)
Text.__bases__ = (Widget,)
Text.__init__ = t__init__

def sp__init__(self, master=None, cnf={}, **kw):
     super(Spinbox, self).__init__(master, 'spinbox', cnf, (), **kw)
Spinbox.__bases__ = (Widget,)
Spinbox.__init__ = sp__init__

def lf__init__(self, master=None, cnf={}, **kw):
     super(LabelFrame, self).__init__(master, 'labelframe', cnf, (), **kw)
LabelFrame.__bases__ = (Widget,)
LabelFrame.__init__ = lf__init__

def pw__init__(self, master=None, cnf={}, **kw):
     super(PanedWindow, self).__init__(master, 'panedwindow', cnf, (), **kw)
PanedWindow.__bases__ = (Widget,)
PanedWindow.__init__ = pw__init__