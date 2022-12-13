from tkinter import Frame, Label, Button, Entry, Checkbutton, OptionMenu, Radiobutton, Listbox, Scale
from tkinter import Canvas, Menu
from tkinter import TOP, LEFT, RIGHT, BOTTOM, CENTER, X, Y, BOTH, END, INSERT, StringVar, IntVar
from tkinter.ttk import Treeview, Combobox, Spinbox
from tkinter.scrolledtext import ScrolledText
from .flags import __ttk_enabled__
if __ttk_enabled__:
	from tkinter.ttk import Frame, Label, Button, Entry, Checkbutton, OptionMenu
else:
	from tkinter.ttk import Style

from .rTkErrors import *
from .rTkUtils import clipboard, widgetBase, time_it
from .rTkTheme import _ThemeManager

def pack_opts(**kwargs):
	pak = ["side", "expand", "fill"]
	if __ttk_enabled__:
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

class cFrame(Frame, widgetBase):
	@time_it
	def __init__(self, master,  **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		super(cFrame, self).__init__(master)
		self.configure(kw_wid)
		style_widget(self, kw_style, "TFrame")
		if len(kw_pak) != 0:
			self.pack(kw_pak)

class cLabel(Label, widgetBase):
	@time_it
	def __init__(self, master,  **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		super(cLabel, self).__init__(master)
		self.configure(kw_wid)
		style_widget(self, kw_style, "TLabel")
		if len(kw_pak) != 0:
			self.pack(kw_pak)
	@time_it
	def set(self, value):
		self.configure(text=value)

class cButton(Button, widgetBase):
	@time_it
	def __init__(self, master,  **kwargs):
		self.__dict__.update(kwargs)
		kwargs['cursor'] = kwargs.pop('cursor', 'hand2')
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		super(cButton, self).__init__(master)
		self.configure(kw_wid)
		style_widget(self, kw_style, "TButton")
		if len(kw_pak) != 0:
			self.pack(kw_pak)

class cEntry(Entry, widgetBase):
	@time_it
	def __init__(self, master, value="", **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		if 'value' in kw_wid:
			del kw_wid['value']
		super(cEntry, self).__init__(master)
		if 'textvariable' not in kwargs.keys():
			self.var = StringVar()
			if value != "":
				self.var.set(value)
			kw_wid['textvariable'] = self.var
		else:
			self.var = kw_wid['textvariable']
			self.var.set(value)
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
	def get(self, *args):
		return widgetBase.get(self, *args)
	@time_it
	def _do_popup(self, event):
		try:
			self.__menu.tk_popup(event.x_root, event.y_root)
		finally:
			self.__menu.grab_release()
	@time_it
	def _cut(self):
		try:
			clipboard.copy(self.selection_get())
			self.delete(SEL_FIRST, SEL_LAST)
		except:
			raise
	@time_it
	def _copy(self):
		try:
			clipboard.copy(self.selection_get())
		except:
			raise
	@time_it
	def _paste(self):
		try:
			self.insert(SEL_LAST, clipboard.paste())
			self.delete(SEL_FIRST, SEL_LAST)
		except:
			self.insert(self.index(INSERT), clipboard.paste())
	@time_it
	def _select_all(self):
		self.select_range(0,END)

class cCanvas(Canvas, widgetBase):
	@time_it
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

class cTreeview(Treeview, widgetBase):
	@time_it
	def __init__(self, master, **kwargs):
		self.master = master
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
		self.style = self.get_root().thm.style
		#self.style = Style()
		
		self.style.map(f"{str(self.__repr__())}.Treeview", foreground=self._fixed_map("foreground", self.style), background=self._fixed_map("background", self.style))
		self.style.configure(f"{str(self.__repr__())}.Treeview", background=bbg, fieldbackground=bbg, foreground=ffg)
		self.style.configure(f"{str(self.__repr__())}.Treeview.Heading",background=colour1, foreground=ffg)
		super(cTreeview, self).__init__(master)
		self.configure(kw_wid)
		if __ttk_enabled__:
			style_widget(self, kw_style, "Treeview")
		self.tag_configure('highlight', background='lightblue', foreground="black")
		if bgp and fgp:
			self.tag_configure("t1", background=colour2, foreground=ffg)
			self.tag_configure("t2", background=colour3, foreground=ffg)
		self.configure(style=f"{str(self.__repr__())}.Treeview")
		self['show'] = 'headings'
		if len(kw_pak) != 0:
			self.pack(kw_pak)
	@time_it
	def _fixed_map(self, option, style):
		return [elm for elm in style.map(f"{str(self.__repr__())}.Treeview", query_opt=option) if elm[:2] != ("!disabled", "!selected")]
	@time_it
	def set_cols(self, cols): ##sets list of colum names
		self['columns'] = tuple(cols)
		for col in cols:
			self.heading(col, text=col, command=lambda _col=col: self._treeview_sort_column(_col, 0))
	@time_it
	def _dir(self, dir): ##changes sort directeion between forward, backward and unsorted
		if dir == 1:
			return 2
		elif dir == 2:
			return 0
		else:
			return 1
	@time_it
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
	@time_it
	def hide(self, a, b, c, event, ivar): # hides data based on input
		if ivar.get() == 1:
			for a in self.detached_data:
				self.reattach(a,'',a)
		else:
			for a in self.detached_data:
				self.detach(a)
	@time_it
	def insert(self, parent='', index='end', iid=None, tags=(), text="", values=[]):##adds new row 
		self.i += 1
		if iid == None:
			iid = self.i
		super().insert(parent=parent, index=index, iid=iid, tags=tags+(self.i,), text=text, values=values)
		self.tag_bind(self.i, '<Motion>', self._highlight_row)
		return iid
	@time_it
	def _highlight_row(self, event): #hover event to hightlight the row under the cursor 
		self.tk.call(self, "tag", "remove", "highlight")
		self.tk.call(self, "tag", "add", "highlight", self.identify_row(event.y)) 
	@time_it
	def __repr__(self):
		return "<%s instance at %s>" % (self.__class__.__name__, id(self))
		pass
	@time_it
	def __del__(self):
		if __ttk_enabled__:
			_ThemeManager.mystyle.configure(f"{str(self.__repr__())}.Treeview", background=None, fieldbackground=None, foreground=None)

class cScrolledText(ScrolledText, widgetBase):
	@time_it
	def __init__(self, master, value="", **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		super(cScrolledText, self).__init__(master)
		self.configure(kw_wid)
		if value != "":
			self.insert(1.0, value)
		if kw_style != {}:
			self.configure(kw_style)
		#style_widget(self, kw_style, "TScrolledText")
		self.__menu = Menu(self, tearoff=0)
		self.__menu.add_command(label="Cut", command=self._cut)
		self.__menu.add_command(label="Copy", command=self._copy)
		self.__menu.add_command(label="Paste", command=self._paste)
		self.__menu.add_command(label="Select All", command=self._select_all)
		self.bind("<Button-3>", self._do_popup)
		if len(kw_pak) != 0:
			self.pack(kw_pak)
	@time_it
	def _hightlight(self):
		pass
	@time_it
	def _do_popup(self, event):
		try:
			self.__menu.tk_popup(event.x_root, event.y_root)
		finally:
			self.__menu.grab_release()
	@time_it
	def _cut(self):
		try:
			clipboard.copy(self.selection_get())
			self.delete(SEL_FIRST, SEL_LAST)
		except:
			pass
	@time_it
	def _copy(self):
		try:
			clipboard.copy(self.selection_get())
		except:
			pass
	@time_it
	def _paste(self):
		try:
			self.insert(SEL_LAST, clipboard.paste())
			self.delete(SEL_FIRST, SEL_LAST)
		except:
			self.insert(self.index(INSERT), clipboard.paste())
	@time_it
	def _select_all(self):
		self.select_range(0,END)
	@time_it
	def get(self, **args):
		return super().get('1.0', END)

class cCheckbutton(Checkbutton, widgetBase):
	@time_it
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		if 'variable' not in kw_wid.keys():
			self.var = IntVar()
			kw_wid['variable'] = self.var
		else:
			self.var = kw_wid['variable']
		#if 'selectcolor' not in kw_style.keys() or kw_style['selectcolor'] is None:
		#	kw_style['selectcolor'] = "#AAFFAA"
		super(cCheckbutton, self).__init__(master)
		self.configure(kw_wid)
		style_widget(self, kw_style, "TCheckbutton")
	@time_it
	def get(self, **kwargs):
		return self.var.get()
	@time_it
	def set(self, value):
		self.var.set(value)

class cOptionMenu(OptionMenu, widgetBase):
	@time_it
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		self.options = kwargs.pop('options', [])
		
		self.var = StringVar()
		if 'default' in kwargs.keys():
			self.__value = kwargs['default']
			selectable_options = [str(x) for x in self.options]
			if kwargs['default'] in selectable_options:
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
		self.var.set(self.__value)
		super(cOptionMenu, self).__init__(master, self.var, self.__value, *selectable_options)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		if 'takefocus' not in kw_wid.keys():
			kw_wid['takefocus'] = 1
		self['menu'].configure(activebackground="blue", activeforeground="white")
		self.configure(kw_wid)
		style_widget(self, kw_style, "TOptionMenu")
		self.bind("<space>", self.open_option_menu)
		if len(kw_pak) != 0:
			self.pack(kw_pak)
	@time_it
	def set(self, value):
		self.var.set(value)
	@time_it
	def get(self, **kwargs):
		return self.var.get()
	@time_it
	def open_option_menu(self, event):
		obj = event.widget
		x = obj.winfo_rootx()
		y = obj.winfo_rooty() + obj.winfo_height()
		obj["menu"].post(x, y)
		return "break"

class cCombobox(Combobox, widgetBase):
	@time_it
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		if 'textvariable' in kwargs:
			raise KeywordError('textvariable')
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		self.var = StringVar()
		super(cCombobox, self).__init__(master)

		if 'state' not in kw_wid:
			kw_wid['state'] = 'readonly'
		if 'default' in kw_wid:
			self.var.set(kw_wid['default'])
			del kw_wid['default']
		kw_wid['textvariable'] = self.var
		self.configure(kw_wid)
		if 'background' in kw_wid:
			bg = kw_wid['background']
		else:
			bg = 'white'

		if 'foreground' in kw_wid:
			fg = kw_wid['foreground']
		else:
			fg = 'black'
		self.style = self.get_root().thm.style
		self.style.map(f'{str(self.__repr__())}.Main.TCombobox', selectbackground=[('readonly', 'blue')])
		self.style.map(f'{str(self.__repr__())}.Main.TCombobox',fieldbackground=[('readonly', bg)])
		self.style.map(f'{str(self.__repr__())}.Main.TCombobox',background=[('readonly', bg)])
		self.style.map(f'{str(self.__repr__())}.Main.TCombobox',foreground=[('readonly', fg)])
		self.style.map(f'{str(self.__repr__())}.Fail.TCombobox', selectbackground=[('readonly', 'blue')])
		self.style.map(f'{str(self.__repr__())}.Fail.TCombobox', fieldbackground=[('readonly', 'red')])
		self.style.map(f'{str(self.__repr__())}.Fail.TCombobox', background=[('readonly', 'red')])
		self.style.map(f'{str(self.__repr__())}.Fail.TCombobox', foreground=[('readonly', 'white')])
		self.configure(style=f'{str(self.__repr__())}.Main.TCombobox')
		self.bind("<FocusIn>", self.unselect)
		if len(kw_pak) != 0:
			self.pack(kw_pak)
		self.var.trace("w", self.unselect)
	@time_it
	def get(self):
		return self.var.get()
	@time_it
	def unselect(self, a=None, b=None, c=None, e=None):
		self.selection_clear()
	@time_it
	def __repr__(self):
		return "<%s instance at %s>" % (self.__class__.__name__, id(self))

#TODO: add option for MenuButton
class cMenu(Menu, widgetBase):
	@time_it
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		context = kwargs.pop('context', None) # get context builder or None
		if not isinstance(context, dict):
			raise MenuContexError 
		super(cMenu, self).__init__(master, tearoff=0)
		self.sub_menus = {}
		self.options = {}
		menu_context = []
		if context:
			for k, v in context.items():
				sub_catagories = []
				if "|" in k:
					mtype = k.split("|")[0]
					mname = k.split("|")[-1].split(".")[-1]
				else:
					mtype = "selection"
					mname = k.split(".")[-1]
				if "." in k:
					for sub in k.split("|")[-1].split("."):
						sub_catagories.append(sub)
					del sub_catagories[-1]
				menu_context.append({'type':mtype, 'name':mname, 'subcatagories':sub_catagories, 'command':v})
		self._build_menu(master, menu_context)
		for menu in menu_context:
			if menu['subcatagories']:
				self.options[f"{'.'.join(menu['subcatagories'])}.{menu['name']}"] = self.sub_menus['.'.join(menu['subcatagories'])].add_command(label=menu['name'], command=menu['command'])
			else:
				self.options[menu['name']] = self.add_command(label=menu['name'], command=menu['command'])
	@time_it
	def _build_menu(self, master, context):
		for item in context:
			if item['subcatagories']:
				if ".".join(item['subcatagories']) not in self.sub_menus: ##if the full sub_menu has been created skip.
					sub_name = ""
					for sub in item['subcatagories']:
						old_name = sub_name
						sub_name += f'.{sub}'
						if sub not in self.sub_menus:
							self.sub_menus[sub_name[1:]] = Menu(self.sub_menus[old_name] if old_name in self.sub_menus else self, tearoff=0)
							if old_name[1:] in self.sub_menus:
								self.sub_menus[old_name[1:]].add_cascade(label=sub, menu=self.sub_menus[sub_name[1:]])
							else:
								self.add_cascade(label=sub, menu=self.sub_menus[sub_name[1:]])
	@time_it
	def _do_popup(self, event):
		try:
			self.tk_popup(event.x_root, event.y_root)
		finally:
			self.grab_release()

class cRadiobutton(Radiobutton, widgetBase):
	@time_it
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		super(cRadioButton, self).__init__(master)
		self.configure(kw_wid)
		style_widget(self, kw_style, "TRadioButton")
		if len(kw_pak) != 0:
			self.pack(kw_pak)

class cListbox(Listbox, widgetBase):
	@time_it
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		super(cListBox, self).__init__(master)
		self.configure(kw_wid)
		style_widget(self, kw_style, "TListBox")
		if len(kw_pak) != 0:
			self.pack(kw_pak)

class cScale(Scale, widgetBase):
	@time_it
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		super(cScale, self).__init__(master)
		self.configure(kw_wid)
		style_widget(self, kw_style, "TScale")
		if len(kw_pak) != 0:
			self.pack(kw_pak)

class cSpinbox(Spinbox, widgetBase): ##incremental box
	@time_it
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		super(cSpinbox, self).__init__(master)
		self.configure(kw_wid)
		style_widget(self, kw_style, "TSpinbox")
		if len(kw_pak) != 0:
			self.pack(kw_pak)