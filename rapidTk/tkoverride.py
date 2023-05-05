from tkinter.__init__ import Pack, Place, Grid, _cnfmerge, XView, YView
from tkinter.__init__ import Frame as tkFrame
from tkinter.__init__ import Scrollbar as tkScrollbar
from tkinter.constants import RIGHT, LEFT, Y, BOTH
from tkinter.__init__ import Frame, Button, Canvas, Checkbutton, Entry, Label, Listbox, Menu, Menubutton, Message 
from tkinter.__init__ import Radiobutton, Scale, Scrollbar, Text, Scale, Spinbox, LabelFrame, PanedWindow
from tkinter.__init__ import Misc

from tkinter.scrolledtext import ScrolledText
##Base Classes
def misc__init__(self, master, widgetName, cnf={}, extra=(), **kw):
    try:
        super(Misc, self).__init__(master, **kw)
    except:
        super(Misc, self).__init__()
Misc.__bases__ = (object,)
Misc.__init__ = misc__init__
class cMisc(Misc):
    def __init__(self, master, widgetName, cnf={}, extra=(), **kw):
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
Canvas.__bases__ = (Widget, XView, YView)
Canvas.__init__ = cv__init__

def cb__init__(self, master=None, cnf={}, **kw):
    super(Checkbutton, self).__init__(master, 'checkbutton', cnf, (), **kw)
Checkbutton.__bases__ = (Widget,)
Checkbutton.__init__ = cb__init__

def e__init__(self, master=None, cnf={}, **kw):
    super(Entry, self).__init__(master, 'entry', cnf, (), **kw)
    Button.__bases__ = (Widget,)
Entry.__bases__ = (Widget,XView)
Entry.__init__ = e__init__

def l__init__(self, master=None, cnf={}, **kw):
    super(Label, self).__init__(master, 'label', cnf, (), **kw)
Label.__bases__ = (Widget,)
Label.__init__ = l__init__

def lb__init__(self, master=None, cnf={}, **kw):
     super(Listbox, self).__init__(master, 'listbox', cnf, (), **kw)
Listbox.__bases__ = (Widget, XView, YView)
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

def sp__init__(self, master=None, cnf={}, **kw):
     super(Spinbox, self).__init__(master, 'spinbox', cnf, (), **kw)
Spinbox.__bases__ = (Widget, XView)
Spinbox.__init__ = sp__init__

def lf__init__(self, master=None, cnf={}, **kw):
     super(LabelFrame, self).__init__(master, 'labelframe', cnf, (), **kw)
LabelFrame.__bases__ = (Widget,)
LabelFrame.__init__ = lf__init__

def pw__init__(self, master=None, cnf={}, **kw):
     super(PanedWindow, self).__init__(master, 'panedwindow', cnf, (), **kw)
PanedWindow.__bases__ = (Widget,)
PanedWindow.__init__ = pw__init__

def pw__init__(self, master=None, cnf={}, **kw):
     super(Scrollbar, self).__init__(master, 'scrollbar', cnf, (), **kw)
Scrollbar.__bases__ = (Widget,)
Scrollbar.__init__ = pw__init__

class Content(Text):
    def __init__(self, master=None, cnf={}, **kw):
        super(Content, self).__init__(master, cnf, **kw)

#class Text(Widget, XView, YView):
def text__init__(self, master=None, cnf={}, **kw):
    self._textvariable = kw.pop("textvariable", None)
    super(Text, self).__init__(master, 'text', cnf, (), **kw)
    if self._textvariable is not None:
        self.tk.call(self._w, 'insert', '1.0', self._textvariable.get())
    self.tk.eval('''
        proc widget_proxy {widget widget_command args} {

            # call the real tk widget command with the real args
            set result [uplevel [linsert $args 0 $widget_command]]

            # if the contents changed, generate an event we can bind to
            if {([lindex $args 0] in {insert replace delete})} {
                event generate $widget <<Change>> -when tail
            }
            # return the result from the real widget command
            return $result
        }
        ''')
    self.tk.eval('''
        rename {widget} _TEXT_{widget}
        interp alias {{}} ::{widget} {{}} widget_proxy {widget} _TEXT_{widget}
    '''.format(widget=str(self)))
    self.bind("<<Change>>", self._on_widget_change)
    if self._textvariable is not None:
        self._textvariable.trace("wu", self._on_var_change)
def text_on_var_change(self, *args):
    text_current = self.tk.call(self._w, 'get', "1.0", "end-1c")
    var_current = self._textvariable.get()
    if text_current != var_current:
        self.tk.call(self._w, 'delete', "1.0", "end")
        self.tk.call(self._w, 'insert', "1.0", var_current)
def text_on_widget_change(self, event=None):
    if self._textvariable is not None:
        self._textvariable.set(self.tk.call(self._w, 'get', "1.0", "end-1c"))
Text.__bases__ = (Widget, XView, YView)
Text.__init__ = text__init__
Text._on_var_change = text_on_var_change
Text._on_widget_change = text_on_widget_change

class ScrolledText(Text):
    def __init__(self, master=None, **kw):
        self._textvariable = kw.get('textvariable', None)
        self.frame = Frame(master)
        self.vbar = Scrollbar(self.frame)
        self.vbar.pack(side=RIGHT, fill=Y)
        kw.update({'yscrollcommand': self.vbar.set})
        super(ScrolledText, self).__init__(self.frame, {}, **kw)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.vbar['command'] = self.yview
        text_meths = vars(Text).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))
        self.tk.eval('''
            proc widget_proxy {widget widget_command args} {

                # call the real tk widget command with the real args
                set result [uplevel [linsert $args 0 $widget_command]]

                # if the contents changed, generate an event we can bind to
                if {([lindex $args 0] in {insert replace delete})} {
                    event generate $widget <<Change>> -when tail
                }
                # return the result from the real widget command
                return $result
            }
            ''')
        self.tk.eval('''
            rename {widget} _SCROLLEDTEXT_{widget}
            interp alias {{}} ::{widget} {{}} widget_proxy {widget} _SCROLLEDTEXT_{widget}
        '''.format(widget=str(self)))
        self.bind("<<Change>>", self._on_widget_change)
        if self._textvariable is not None:
            self._textvariable.trace("wu", self._on_var_change)
ScrolledText._on_var_change = text_on_var_change
ScrolledText._on_widget_change = text_on_widget_change