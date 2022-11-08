from tkinter import Frame, Label, Button, Entry, Checkbutton, OptionMenu
from tkinter import Canvas, Menu
from tkinter import TOP, LEFT, RIGHT, BOTTOM, CENTER, X, Y, BOTH, END, INSERT, StringVar, IntVar
from tkinter.ttk import Treeview
from tkinter.scrolledtext import ScrolledText
import flags
if flags.__ttk_enabled__:
	from tkinter.ttk import Frame, Label, Button, Entry, Checkbutton, OptionMenu
else:
	from tkinter.ttk import Style



from errors import *
from utils import clipboard, master
from theme import _ThemeManager

def pack_opts(**kwargs):
	pak = ["side", "expand", "fill"]
	if flags.__ttk_enabled__:
		style = ['bg', 'height', 'width', 'borderwidth', 'fg', 'padx', 'pady', 'relief', 'selectcolor', 'anchor']
	else:
		style = []
	kw_wid = {}
	kw_pak = {}
	kw_style = {}
	for k, v in kwargs.items():
		if k in pak:
			kw_pak[k] = v
		elif k in style:
			if k == "bg":
				kw_style["background"] = v
			elif k == "fg":
				kw_style["foreground"] = v
			elif k == "width": ##fix for picture lable width only
				if "text" in kwargs.keys():
					kw_style[k] = v
				else:
					kw_style[k] = int(v/10)
			else:
				kw_style[k] = v
		else:
			kw_wid[k] = v
	return kw_wid, kw_pak, kw_style
def style_widget(wd, st, t):
	if st != {}:
		style = _ThemeManager().add_style(f"{str(wd.__repr__())}.{t}", st)
		wd.configure(style=f"{str(wd.__repr__())}.{t}")
		return style
	else:
		return None
## Default Widgits override
class cFrame(Frame, master):
	def __init__(self, master,  **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		super(cFrame, self).__init__(master)
		self.configure(kw_wid)
		style_widget(self, kw_style, "TFrame")
		if len(kw_pak) != 0:
			self.pack(kw_pak)

class cLabel(Label, master):
	def __init__(self, master,  **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		super(cLabel, self).__init__(master)
		self.configure(kw_wid)
		style_widget(self, kw_style, "TLabel")
		if len(kw_pak) != 0:
			self.pack(kw_pak)
	def get(self):
		return self.cget('text')
	def set(self, value):
		self.configure(text=value)

class cButton(Button, master):
	def __init__(self, master,  **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		super(cButton, self).__init__(master)
		self.configure(kw_wid)
		style_widget(self, kw_style, "TButton")
		if len(kw_pak) != 0:
			self.pack(kw_pak)

class cEntry(Entry, master):
	def __init__(self, master, value="", **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		super(cEntry, self).__init__( master)
		self.configure(kw_wid)
		style_widget(self, kw_style, "TEntry")
		self.__menu = Menu(self, tearoff=0)
		self.__menu.add_command(label="Cut", command=self._cut)
		self.__menu.add_command(label="Copy", command=self._copy)
		self.__menu.add_command(label="Paste", command=self._paste)
		self.__menu.add_command(label="Select All", command=self._select_all)
		self.bind("<Button-3>", self._do_popup)
		if len(kw_pak) != 0:
			self.pack(kw_pak)
	def _do_popup(self, event):
		try:
			self.__menu.tk_popup(event.x_root, event.y_root)
		finally:
			self.__menu.grab_release()
	def _cut(self):
		try:
			clipboard.copy(self.selection_get())
			self.delete(SEL_FIRST, SEL_LAST)
		except:
			raise
	def _copy(self):
		try:
			clipboard.copy(self.selection_get())
		except:
			raise
	def _paste(self):
		try:
			self.insert(SEL_LAST, clipboard.paste())
			self.delete(SEL_FIRST, SEL_LAST)
		except:
			self.insert(self.index(INSERT), clipboard.paste())
	def _select_all(self):
		self.select_range(0,END)

class cCanvas(Canvas, master):
	def __init__(self, master,  **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		if 'bd' not in kw_wid or 'boarder' not in kw_wid:
			kw_wid['bd'] = -2
		super(cCanvas, self).__init__(master)
		self.configure({**kw_wid, **kw_style})
		#style_widget(self, kw_style, "TCanvas")
		if len(kw_pak) != 0:
			self.pack(kw_pak)

class cTreeview(Treeview, master):
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		self.i = 0
		self.detached_data = []
		bg="#FFFFFF"
		fg="#000000"
		bgp = False
		fgp = False
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		if 'bg' in kw_wid.keys():
			bbg = kw_wid['bg']
			bgp = True
			del kw_wid['bg']
		else:
			bbg = bg
		if 'fg' in kw_wid.keys():
			ffg = kw_wid['fg']
			fgp = True
			del kw_wid['fg']
		else:
			ffg = fg
		rgb = [int(bbg.replace("#","")[i:i+2], 16) for i in (0, 2, 4)]
		rgbt1 = []
		rgbt2 = []
		colours = ["black", "white"]
		for i in range(len(rgb)):
			if rgb[i] < 255/2:
				rgb[i] += 30
				rgbt1.append(rgb[i]+20)
				rgbt2.append(rgb[i]+40)
			else:
				rgb[i] -= 30
				rgbt1.append(rgb[i]-20)
				rgbt2.append(rgb[i]-40)
		colour1 = '#%02x%02x%02x'%(rgb[0], rgb[1], rgb[2])
		colour2 = '#%02x%02x%02x'%(rgbt1[0], rgbt1[1], rgbt1[2])
		colour3 = '#%02x%02x%02x'%(rgbt2[0], rgbt2[1], rgbt2[2])
		self.style = None
		if flags.__ttk_enabled__:
			self.style = _ThemeManager.mystyle
			self.style.map(f"{str(self.__repr__())}.Treeview", foreground=self._fixed_map("foreground", self.style), background=self._fixed_map("background", self.style))
			self.style.configure(f"{str(self.__repr__())}.Treeview", background=bbg, fieldbackground=bbg, foreground=ffg)
			self.style.configure(f"{str(self.__repr__())}.Treeview.Heading",background=colour1, foreground=ffg)
		else:
			self.style = Style()
			self.style.theme_use("clam")
			self.style.map(f"{str(self.__repr__())}.Treeview", foreground=self._fixed_map("foreground", self.style), background=self._fixed_map("background", self.style))
			self.style.configure(f"{str(self.__repr__())}.Treeview", background=bbg, fieldbackground=bbg, foreground=ffg)
			self.style.configure(f"{str(self.__repr__())}.Treeview.Heading",background=colour1, foreground=ffg)
		super(cTreeview, self).__init__(master)
		self.configure(kw_wid)
		if flags.__ttk_enabled__:
			style_widget(self, kw_style, "Treeview")
		self.tag_configure('highlight', background='lightblue', foreground="black")
		if bgp and fgp:
			self.tag_configure("t1", background=colour2, foreground=ffg)
			self.tag_configure("t2", background=colour3, foreground=ffg)
		self.configure(style=f"{str(self.__repr__())}.Treeview")
		self['show'] = 'headings'
		if len(kw_pak) != 0:
			self.pack(kw_pak)
	def _fixed_map(self, option, style):
		return [elm for elm in style.map(f"{str(self.__repr__())}.Treeview", query_opt=option) if elm[:2] != ("!disabled", "!selected")]
	def set_cols(self, cols): ##sets list of colum names
		self['columns'] = tuple(cols)
		for col in cols:
			self.heading(col, text=col, command=lambda _col=col: self._treeview_sort_column(_col, 0))
	def _dir(self, dir): ##changes sort directeion between forward, backward and unsorted
		if dir == 1:
			return 2
		elif dir == 2:
			return 0
		else:
			return 1
	def _treeview_sort_column(self, col, rv):
		dirs = [True, False, None]
		reverse = dirs[self._dir(rv)]
		if reverse == None:
			l = [(self.set(k, col), k) for k in self.get_children('')]
			l.sort(reverse=False, key=lambda tup: int(tup[1]))
		else:
			l = [(self.set(k, col), k) for k in self.get_children('')]
			try:
				int(l[0][0])
				l.sort(reverse=dirs[self._dir(rv)], key=lambda tup: int(tup[0]))
			except:
				l.sort(reverse=dirs[self._dir(rv)])
		for index, (val, k) in enumerate(l):
			self.move(k, '', index)
		self.heading(col, text=col, command=lambda _col=col:self._treeview_sort_column(_col, self._dir(rv)))
	def hide(self, a, b, c, event, ivar): # hides data based on input
		if ivar.get() == 1:
			for a in self.detached_data:
				self.reattach(a,'',a)
		else:
			for a in self.detached_data:
				self.detach(a)
	def insert(self, parent='', index='end', iid=None, tags=(), text="", values=[]):##adds new row 
		self.i += 1
		if iid == None:
			iid = self.i
		super().insert(parent=parent, index=index, iid=iid, tags=tags+(self.i,), text=text, values=values)
		self.tag_bind(self.i, '<Motion>', self._highlight_row) 
	def _highlight_row(self, event): #hover event to hightlight the row under the cursor 
		self.tk.call(self, "tag", "remove", "highlight")
		self.tk.call(self, "tag", "add", "highlight", self.identify_row(event.y)) 
	def __repr__(self):
		return "<%s instance at %s>" % (self.__class__.__name__, id(self))
		pass
	def __del__(self):
		if flags.__ttk_enabled__:
			_ThemeManager.mystyle.configure(f"{str(self.__repr__())}.Treeview", background=None, fieldbackground=None, foreground=None)

class cScrolledText(ScrolledText, master):
	def __init__(self, master, value="", **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		super(cScrolledText, self).__init__(master)
		self.configure(kw_wid)
		if kw_style != {}:
			self.configure(kw_style)
		#style_widget(self, kw_style, "TScrolledText")
		self.__menu = Menu(self, tearoff=0)
		self.__menu.add_command(label="Cut", command=self._cut)
		self.__menu.add_command(label="Copy", command=self._copy)
		self.__menu.add_command(label="Paste", command=self._paste)
		self.__menu.add_command(label="Select All", command=self._select_all)
		if value != "":
			self.insert(0, value)
		self.bind("<Button-3>", self._do_popup)
		if len(kw_pak) != 0:
			self.pack(kw_pak)
	def _hightlight(self):
		pass
	def _do_popup(self, event):
		try:
			self.__menu.tk_popup(event.x_root, event.y_root)
		finally:
			self.__menu.grab_release()
	def _cut(self):
		try:
			clipboard.copy(self.selection_get())
			self.delete(SEL_FIRST, SEL_LAST)
		except:
			pass
	def _copy(self):
		try:
			clipboard.copy(self.selection_get())
		except:
			pass
	def _paste(self):
		try:
			self.insert(SEL_LAST, clipboard.paste())
			self.delete(SEL_FIRST, SEL_LAST)
		except:
			self.insert(self.index(INSERT), clipboard.paste())
	def _select_all(self):
		self.select_range(0,END)
	def get(self, **args):
		return super().get('1.0', END)

class cCheckbutton(Checkbutton, master):
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		self.var = IntVar()
		kw_wid['variable'] = self.var
		#if 'selectcolor' not in kw_style.keys() or kw_style['selectcolor'] is None:
		#	kw_style['selectcolor'] = "#AAFFAA"
		super(cCheckbutton, self).__init__(master)
		self.configure(kw_wid)
		style_widget(self, kw_style, "TCheckbutton")
	def get(self, **kwargs):
		return self.var.get()
	def set(self, value):
		self.var.set(value)

class cOptionMenu(OptionMenu, master):
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		self.options = []
		if 'options' in kwargs.keys():
			self.options = kwargs['options']
			del kwargs['options']
		self.var = StringVar()
		if 'default' in kwargs.keys():
			self.__value = kwargs['default']
			selectable_options = [str(x) for x in self.options]
			del selectable_options[selectable_options.index(str(kwargs['default']))]
			del kwargs['default']
		else:
			self.__value = self.options[0] if len(self.options) > 0 else None
			if len(self.options) > 0:
				selectable_options = [str(x) for x in self.options[1:]]
			else:
				selectable_options = [str(x) for x in self.options]
		if 'non_valid' in kwargs.keys():
			for item in kwargs['non_valid']:
				if item in self.options:
					del self.options[self.options.index(item)]
			del kwargs['non_valid']

		super(cOptionMenu, self).__init__(master, self.var, self.__value, *selectable_options)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		self.configure(kw_wid)
		style_widget(self, kw_style, "TOptionMenu")
		if len(kw_pak) != 0:
			self.pack(kw_pak)
	def get(self, **kwargs):
		return self.var.get()


