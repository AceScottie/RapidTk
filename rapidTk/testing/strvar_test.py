from tkinter.__init__ import Pack, Place, Grid, _cnfmerge, XView, YView
from tkinter.constants import RIGHT, LEFT, Y, BOTH
from tkinter.__init__ import Frame, Button, Canvas, Checkbutton, Entry, Label, Listbox, Menu, Menubutton, Message 
from tkinter.__init__ import Radiobutton, Scale, Scrollbar, Text, Scale, Spinbox, LabelFrame, PanedWindow
from tkinter.__init__ import Misc
def misc__init__(self, master, widgetName, cnf={}, extra=(), **kw):
    super(Misc, self).__init__(master, **kw)
Misc.__bases__ = (object,)
Misc.__init__ = misc__init__
class cMisc(Misc):
    def __init__(self, master, widgetName, cnf={}, extra=(), **kw):
        #super().__init__()
        super(cMisc, self).__init__(master, widgetName, cnf, extra, **kw)
class BaseWidget(cMisc):
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
    def __init__(self, master, widgetName, cnf={}, extra=(), **kw):
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
        self.tk.call((widgetName, self._w) + extra + self._options(cnf))
        for k, v in classes:
            k.configure(self, v)
    def destroy(self):
        """Destroy this and all descendants widgets."""
        for c in list(self.children.values()): c.destroy()
        self.tk.call('destroy', self._w)
        if self._name in self.master.children:
            del self.master.children[self._name]
        super().destroy() ##patched

    def _do(self, name, args=()):
        # XXX Obsolete -- better use self.tk.call directly!
        return self.tk.call((self._w, name) + args)
class Widget(BaseWidget, Pack, Place, Grid):
    def __init__(self, master=None, widgetName=None, cnf={}, extra=(), **kw):
        super(Widget, self).__init__(master, widgetName, cnf, extra, **kw)
class widgetBase:
	def __init__(self, master, **kwargs):
		super(widgetBase, self).__init__()
		print("widgetBase init")
		self.master = master
		self.uid = "1234567890"
def cv__init__(self, master=None, cnf={}, **kw):
	print("override canvas init")
	super(Canvas, self).__init__(master, 'canvas', cnf, (), **kw)
Canvas.__bases__ = (Widget,)
Canvas.__init__ = cv__init__


class cCanvas(Canvas, widgetBase):
	def __init__(self, master=None, **kwargs):
		super(cCanvas, self).__init__(master, **kwargs)

from tkinter import Tk, TOP

root = Tk()

c = cCanvas(root)
c.pack(side=TOP)
print(c.uid)
root.mainloop()