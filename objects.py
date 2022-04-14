from tkinter import Frame, Label, Button, Entry, Canvas, Checkbutton, OptionMenu, Menu, END, INSERT, StringVar, IntVar
from tkinter import TOP, LEFT, RIGHT, BOTTOM, CENTER, X, Y, BOTH
from tkinter.ttk import Treeview, Style
from tkinter.scrolledtext import ScrolledText
from tkcalendar import DateEntry
from .errors import *
from .utils import clipboard
def pack_opts(**kwargs):
	pak = ["side", "expand", "fill"]
	kw_wid = {}
	kw_pak = {}
	for k, v in kwargs.items():
		if k in pak:
			kw_pak[k] = v
		else:
			kw_wid[k] = v
	return kw_wid, kw_pak
## Default Widgits override
class cFrame(Frame):
	def __init__(self, master,  **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak = pack_opts(**kwargs)
		Frame.__init__(*(self, master), kw_wid)
		if len(kw_pak) != 0:
			self.pack(kw_pak)
class cLabel(Label):
	def __init__(self, master,  **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak = pack_opts(**kwargs)
		Label.__init__(*(self, master), kw_wid)
		if len(kw_pak) != 0:
			self.pack(kw_pak)
	def get(self):
		return self.cget('text')
	def set(self, value):
		self.configure(text=value)
class cButton(Button):
	def __init__(self, master,  **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak = pack_opts(**kwargs)
		Button.__init__(*(self, master), kw_wid)
		if len(kw_pak) != 0:
			self.pack(kw_pak)
class cEntry(Entry):
	def __init__(self, master, value="", **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak = pack_opts(**kwargs)
		Entry.__init__(*(self, master), kw_wid)
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
	#def get(self, **args):
	#	return super().get()
class cCanvas(Canvas):
	def __init__(self, master,  **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak = pack_opts(**kwargs)
		if 'bd' not in kw_wid or 'boarder' not in kw_wid:
			kw_wid['bd'] = -2
		Canvas.__init__(*(self, master), kw_wid)
		if len(kw_pak) != 0:
			self.pack(kw_pak)
class cTreeview(Treeview):
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		self.i = 0
		bg="#FFFFFF"
		fg="#000000"
		kw_wid, kw_pak = pack_opts(**kwargs)
		
		style = Style()
		if "bg" not in kw_wid.keys():
			kw_wid['bg'] = bg
		if "fg" not in kw_wid.keys():
			kw_wid['fg'] = fg
		rgb = [int(kw_wid['bg'].replace("#","")[i:i+2], 16) for i in (0, 2, 4)]
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
		
		style.theme_use("clam")
		style.map(f"{str(self.__repr__())}.Treeview", foreground=self._fixed_map("foreground", style), background=self._fixed_map("background", style))
		style.configure(f"{str(self.__repr__())}.Treeview", background=kw_wid['bg'], fieldbackground=kw_wid['bg'], foreground=kw_wid['fg'])
		style.configure(f"{str(self.__repr__())}.Treeview.Heading",background=colour1, foreground=kw_wid['fg'])
		
		Treeview.__init__(*(self, master))
		self.tag_configure('highlight', background='lightblue', foreground="black")
		if "bg" in kw_wid.keys() and "fg" in kw_wid.keys():
			self.tag_configure("t1", background=colour2, foreground=kw_wid['fg'])
			self.tag_configure("t2", background=colour3, foreground=kw_wid['fg'])
		self.configure(style=f"{str(self.__repr__())}.Treeview")
		self['show'] = 'headings'
		if len(kw_pak) != 0:
			self.pack(kw_pak)
	def _fixed_map(self, option, style):
		return [elm for elm in style.map(f"{str(self.__repr__())}.Treeview", query_opt=option) if elm[:2] != ("!disabled", "!selected")]
	def set_cols(self, cols):
		self['columns'] = tuple(cols)
		for col in cols:
			self.heading(col, text=col, command=lambda _col=col: self._treeview_sort_column(_col, 0))
	def _dir(self, dir):
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
	def hide(self, a, b, c, event, ivar, data):
		if ivar.get() == 1:
			for a in data:
				self.reattach(a,'',a)
		else:
			for a in data:
				self.detach(a)
	def insert(self, parent='', index='end', iid=None, tags=(), text="", values=[]):
		self.i += 1
		if iid == None:
			iid = self.i
		super().insert(parent=parent, index=index, iid=iid, tags=tags+(self.i,), text=text, values=values)
		self.tag_bind(self.i, '<Motion>', self._highlight_row)
	def _highlight_row(self, event):
		self.tk.call(self, "tag", "remove", "highlight")
		self.tk.call(self, "tag", "add", "highlight", self.identify_row(event.y))
	def __repr__(self):
		 return "<%s instance at %s>" % (self.__class__.__name__, id(self))
class cScrolledText(ScrolledText):
	def __init__(self, master, value="", **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak = pack_opts(**kwargs)
		ScrolledText.__init__(*(self, master), **kw_wid)
		print("colour:%s"%self['background'])
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
class cCheckbutton(Checkbutton):
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak = pack_opts(**kwargs)
		self.var = IntVar()
		kw_wid['variable'] = self.var
		Checkbutton.__init__(*(self, master), **kw_wid)
	def get(self, **kwargs):
		return self.var.get()
	def set(self, value):
		self.var.set(value)
class cOptionMenu(OptionMenu):
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak = pack_opts(**kwargs)
		self.var = StringVar()
		OptionMenu.__init__(*(self, master), **kw_wid)
	def get(self, **kwargs):
		return self.var.get()
class cDateEntry(DateEntry):
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak = pack_opts(**kwargs)
		if 'date_pattern' not in kw_wid.keys():
			kw_wid['date_pattern'] = "dd/mm/yyyy"
		DateEntry.__init__(*(self, master), **kw_wid)
		if len(kw_pak) != 0:
			self.pack(kw_pak)
	def insert(self, data):
		try:
			if isinstance(data, datetime.datetime) or isinstance(data, datetime.date):
				super().insert(data.strftime("%d/%m/%Y"))
			else:
				super().insert(data)
		except:
			super().insert(data)

