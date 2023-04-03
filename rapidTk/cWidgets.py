import logging
from tkinter import Frame, Label, Button, Entry, Checkbutton, Radiobutton, Listbox, Scale
from tkinter import Canvas, Menu
from tkinter import TOP, LEFT, RIGHT, BOTTOM, CENTER, X, Y, BOTH, END, INSERT, StringVar, IntVar, DoubleVar, Event
from tkinter.ttk import Treeview, Combobox
from tkinter.scrolledtext import ScrolledText
from rapidTk.__main__ import rapidTk
from rapidTk.rTkOverrides import OptionMenu, Spinbox
from rapidTk.flags import __ttk_enabled__
if __ttk_enabled__:
	from tkinter.ttk import Frame, Label, Button, Entry, Checkbutton
else:
	from tkinter.ttk import Style

from rapidTk.rTkErrors import *
from rapidTk.rTkUtils import clipboard, widgetBase, time_it, inline_layout, _UniqueIdentifiers
from rapidTk.rTkTheme import _ThemeManager, style_widget
import rapidTk.types as rtktypes

class cFrame(Frame, widgetBase):
	_widgetBase__widget_type = rtktypes.noget
	@time_it
	def __xinit__(self, master, **kwargs):
		super(cFrame, self).__init__(master, **kwargs)
		widgetBase.__init__(self, master, **kwargs)
	@time_it
	def __init__(self, master, **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		print("calling super method")
		self.__xinit__(master, **widget_args)
		print("super complete")
		if layout.method is not None:
			layout.inline(self)


class cLabel(Label, widgetBase):
	_widgetBase__widget_type = rtktypes.disget
	@time_it
	def __xinit__(self, master, **kwargs):
		super(cLabel, self).__init__(master, **kwargs)
		widgetBase.__init__(self, master, **kwargs)
	@time_it
	def __init__(self, master,  **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		self.bg = kwargs.get('bg', kwargs.get('background', None))
		self.fg = kwargs.get('fg', kwargs.get('foreground', None))
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		self.__xinit__(master, **widget_args)
		if self.bg is None:
			self.bg = self.cget('background')
		if self.fg is None:
			self.fg = self.cget('foreground')
		
		##style_widget(self, kw_style, "TFrame") ##going to be part of ttk and theme manager
		if layout.method is not None:
			layout.inline(self)


class cButton(Button, widgetBase):
	_widgetBase__widget_type = rtktypes.disget
	@time_it
	def __xinit__(self, master, **kwargs):
		super(cButton, self).__init__(master, **kwargs)
		widgetBase.__init__(self, master, **kwargs)
	@time_it
	def __init__(self, master,  **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		kwargs['cursor'] = kwargs.pop('cursor', 'hand2')
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		self.__xinit__(master, **widget_args)
		logging.getLogger('rapidTk').rtkverbose(f"created widget {self} with args {widget_args}")
		if layout.method is not None:
			layout.inline(self)


class cEntry(Entry, widgetBase):
	_widgetBase__widget_type = rtktypes.singleget
	@time_it
	def __xinit__(self, master, **kwargs):
		super(cEntry, self).__init__(master, **kwargs)
		widgetBase.__init__(self, master, **kwargs)
	@time_it
	def __init__(self, master, **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		logging.getLogger('rapidTk').rtkverbose(f"cEntry got kwargs {kwargs}")
		value = kwargs.pop('value', '')
		kwargs['textvariable'], self.var = (kwargs.get('textvariable', StringVar()),)*2
		self.var.set(value)
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		logging.getLogger('rapidTk').rtkverbose(f"cEntry got widget_args {widget_args} and {layout.method}")
		self.__xinit__(master, **widget_args)
		logging.getLogger('rapidTk').rtkverbose(f"created cEntry {self} with args {widget_args}")
		##style_widget(self, kw_style, "TFrame") ##going to be part of ttk and theme manager
		self.__menu = Menu(self, tearoff=0)
		self.__menu.add_command(label="Cut", command=self._cut)
		self.__menu.add_command(label="Copy", command=self._copy)
		self.__menu.add_command(label="Paste", command=self._paste)
		self.__menu.add_command(label="Select All", command=self._select_all)
		self.bind("<Button-3>", self._do_popup)
		
		if layout.method is not None:
			layout.inline(self)
	@time_it
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
	_widgetBase__widget_type = rtktypes.noget
	@time_it
	def __xinit__(self, master, **kwargs):
		super(cCanvas, self).__init__(master, **kwargs)
		widgetBase.__init__(self, master, **kwargs)
	@time_it
	def __init__(self, master,  **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		if 'bd' not in kwargs or 'boarder' not in kwargs:
			kwargs['bd'] = -2
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		self.__xinit__(master, **widget_args)
		
		##style_widget(self, kw_style, "TFrame") ##going to be part of ttk and theme manager
		if layout.method is not None:
			layout.inline(self)


class cTreeview(Treeview, widgetBase):
	_widgetBase__widget_type = rtktypes.treeget
	@time_it
	def __xinit__(self, master, **kwargs):
		super(cTreeview, self).__init__(master, **kwargs)
		widgetBase.__init__(self, master, **kwargs)
	@time_it
	def __init__(self, master, **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		self.master = master
		self.i = 0
		self.detached_data = []
		bg = kwargs.pop('bg', '#FFFFFF')
		fg = kwargs.pop('fg', '#000000')

		rgb = [int(bg.replace("#","")[i:i+2], 16) for i in (0, 2, 4)]
		rgbt1 = []
		rgbt2 = []
		for i in range(len(rgb)):
			if rgb[i] < 255/2:
				rgb[i] += 30
				rgbt1.append(rgb[i]+20)
				rgbt2.append(rgb[i]+40)
			else:
				rgb[i] -= 30
				rgbt1.append(rgb[i]-20)
				rgbt2.append(rgb[i]-40)
		colour1, colour2, colour3 = '#%02x%02x%02x'%(rgb[0], rgb[1], rgb[2]), '#%02x%02x%02x'%(rgbt1[0], rgbt1[1], rgbt1[2]), '#%02x%02x%02x'%(rgbt2[0], rgbt2[1], rgbt2[2])
		self.style = self.get_root().thm.style
		self.style.map(f"{str(self.__repr__())}.Treeview", foreground=self._fixed_map("foreground", self.style), background=self._fixed_map("background", self.style))
		self.style.configure(f"{str(self.__repr__())}.Treeview", background=bg, fieldbackground=bg, foreground=fg)
		self.style.configure(f"{str(self.__repr__())}.Treeview.Heading",background=colour1, foreground=fg)
		kwargs['style'] = kwargs.pop('style', f"{str(self.__repr__())}.Treeview")
		
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		self.__xinit__(master, **widget_args)
		self.tag_configure('highlight', background='lightblue', foreground="black")
		self.tag_configure("t1", background=colour2, foreground=fg)
		self.tag_configure("t2", background=colour3, foreground=fg)
		self['show'] = 'headings'
		if layout.method is not None:
			layout.inline(self)
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
	def detach(self, a):
		self.detached_data.append(a)
		super().detach(a)
	@time_it
	def hide(self, a, b, c, event, ivar): # hides data based on input
		if ivar.get() == 1:
			for a in self.detached_data:
				self.reattach(a,'',a)
		else:
			for a in self.detached_data:
				super().detach(a)
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
	_widgetBase__widget_type = rtktypes.multiget
	@time_it
	def __xinit__(self, master, **kwargs):
		super(cScrolledText, self).__init__(master, **kwargs)
		widgetBase.__init__(self, master, **kwargs)
	@time_it
	def __init__(self, master, **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		value = kwargs.pop('value', '')
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		self.__xinit__(master, **widget_args)
		if isinstance(self.get_root(), rapidTk):
			self.get_root().sm.add_widget(self)
		##style_widget(self, kw_style, "TFrame") ##going to be part of ttk and theme manager
		if value != '':
			self.insert(1.0, value)
		#style_widget(self, kw_style, "TScrolledText")
		self.__menu = Menu(self, tearoff=0)
		self.__menu.add_command(label="Cut", command=self._cut)
		self.__menu.add_command(label="Copy", command=self._copy)
		self.__menu.add_command(label="Paste", command=self._paste)
		self.__menu.add_command(label="Select All", command=self._select_all)
		self.bind("<Button-3>", self._do_popup)
		if layout.method is not None:
			layout.inline(self)
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
	_widgetBase__widget_type = rtktypes.intget
	@time_it
	def __xinit__(self, master, **kwargs):
		super(cCheckbutton, self).__init__(master, **kwargs)
		widgetBase.__init__(self, master, **kwargs)
	@time_it
	def __init__(self, master, **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		kwargs['variable'] = self.var = kwargs.get('variable', IntVar())
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		self.__xinit__(master, **widget_args)
		if layout.method is not None:
			layout.inline(self)
	@time_it
	def get(self, **kwargs):
		return self.var.get()
	@time_it
	def set(self, value):
		self.var.set(value)


class cOptionMenu(OptionMenu, widgetBase): ##OptionMenu overrideen from rTkOverrides
	_widgetBase__widget_type = rtktypes.strget
	@time_it
	def __xinit__(self, master, **kwargs):
		super(cOptionMenu, self).__init__(master, **kwargs)
		widgetBase.__init__(self, master, **kwargs)
	@time_it
	def __init__(self, master, **kwargs): ##TODO: fix removing invalid options from this and add to reOptionMenu
		#self.uuid = _UniqueIdentifiers().new()
		self.options = kwargs.pop('options', kwargs.pop('values', [])) ##this will be the full list of options used for validation
		self.selectable_options = [str(x) for x in self.options] ## modified options for display
		kwargs['textvariable'] = self.var = kwargs.pop('variable', kwargs.pop('textvariable',StringVar()))
		kwargs['value'] = self.__value = kwargs.pop('default', None) 
		if self.__value is not None:
			self.var.set(self.__value)
			if self.__value in self.selectable_options:
				self.selectable_options.remove(self.__value)
		
		#nv = kwargs.pop('non_valid', []) 
		
		kwargs['takefocus'] = kwargs.pop('takefocus', 1) ##allows tab selection
		kwargs['values'] = self.selectable_options
		
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		self.__xinit__(master, **widget_args)
		self['menu'].configure(activebackground="blue", activeforeground="white")
		self.bind("<space>", self.open_option_menu)

		if layout.method is not None:
			layout.inline(self)
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
	_widgetBase__widget_type = rtktypes.strget
	@time_it
	def __xinit__(self, master, **kwargs):
		super(cCombobox, self).__init__(master, **kwargs)
		widgetBase.__init__(self, master, **kwargs)
	@time_it
	def __init__(self, master, **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		self.values, kwargs['values'] = (kwargs.pop('options', []),)*2
		kwargs['textvariable']  = kwargs.get('textvariable', StringVar())
		self.var = kwargs['textvariable']
		kwargs['state'] = kwargs.pop('state', 'readonly')
		default = kwargs.pop('default', None)
		if default is not None:
			self.var.set(default)
		bg = kwargs.get('bg', 'white')
		fg = kwargs.get('fg', 'black')
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		print(f'cCombobox {widget_args}')
		self.__xinit__(master, **widget_args)

		self.style = self.get_root().thm.style
		self.style.map(f'{str(self.__repr__())}.Main.TCombobox', selectbackground=[('readonly', 'blue')])
		self.style.map(f'{str(self.__repr__())}.Main.TCombobox',fieldbackground=[('readonly', bg)])
		self.style.map(f'{str(self.__repr__())}.Main.TCombobox',background=[('readonly', bg)])
		self.style.map(f'{str(self.__repr__())}.Main.TCombobox',foreground=[('readonly', fg)])
		self.style.map(f'{str(self.__repr__())}.Fail.TCombobox', selectbackground=[('readonly', 'blue')])
		self.style.map(f'{str(self.__repr__())}.Fail.TCombobox', fieldbackground=[('readonly', 'red')])
		self.style.map(f'{str(self.__repr__())}.Fail.TCombobox', background=[('readonly', 'red')])
		self.style.map(f'{str(self.__repr__())}.Fail.TCombobox', foreground=[('readonly', 'white')])
		self.configure(style=kwargs.pop('style', f'{str(self.__repr__())}.Main.TCombobox'))

		

		self.bind("<FocusIn>", self.unselect)
		self.var.trace("w", self.unselect)
		if layout.method is not None:
			layout.inline(self)
	@time_it
	def get(self):
		print(f"getting cCombobox: {self.var.get()}.")
		return self.var.get()
	@time_it
	def unselect(self, a=None, b=None, c=None, e=None):
		self.selection_clear()
	@time_it
	def __repr__(self):
		return "<%s instance at %s>" % (self.__class__.__name__, id(self))

#TODO: add option for MenuButton
class cMenu(Menu, widgetBase):
	_widgetBase__widget_type = rtktypes.noget
	@time_it
	def __xinit__(self, master, **kwargs):
		super(cMenu, self).__init__(master, **kwargs)
		widgetBase.__init__(self, master, **kwargs)
	@time_it
	def __init__(self, master, **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		context = kwargs.pop('context', None) # get context builder or None
		if not isinstance(context, dict):
			raise MenuContexError 
		self.__xinit__(master, tearoff=0)
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
	_widgetBase__widget_type = rtktypes.intget
	@time_it
	def __xinit__(self, master, **kwargs):
		super(cRadiobutton, self).__init__(master, **kwargs)
		widgetBase.__init__(self, master, **kwargs)
	@time_it
	def __init__(self, master, **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		self.__xinit__(master, **widget_args)
		if layout.method is not None:
			layout.inline(self)


class cListbox(Listbox, widgetBase):
	_widgetBase__widget_type = rtktypes.strget
	@time_it
	def __xinit__(self, master, **kwargs):
		super(cListbox, self).__init__(master, **kwargs)
		widgetBase.__init__(self, master, **kwargs)
	@time_it
	def __init__(self, master, **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		self.__xinit__(master, **widget_args)
		if layout.method is not None:
			layout.inline(self)


class cScale(Scale, widgetBase):
	_widgetBase__widget_type = rtktypes.intget
	@time_it
	def __xinit__(self, master, **kwargs):
		super(cScale, self).__init__(master, **kwargs)
		widgetBase.__init__(self, master, **kwargs)
	@time_it
	def __init__(self, master, **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		self.var, kwargs['variable'] = (kwargs.pop('variable', IntVar()),)*2
		vals = kwargs.pop('range', [0, 1])
		kwargs['from_'] = vals[0]
		kwargs['to'] = vals[-1]
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		self.__xinit__(master, **widget_args)
		if layout.method is not None:
			layout.inline(self)


class cSpinbox(Spinbox, widgetBase): ##Spinbox overrideen from rTkOverrides
	_widgetBase__widget_type = rtktypes.strget
	@time_it
	def __xinit__(self, master, **kwargs):
		super(cSpinbox, self).__init__(master, **kwargs)
		widgetBase.__init__(self, master, **kwargs)
	@time_it
	def __init__(self, master, **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		self.values = kwargs.get('values', ['0','1','2'])
		kwargs['textvariable'] = self.var = kwargs.pop('textvariable', StringVar())
		kwargs['value'] = kwargs.get('value', self.values[0])
		self.wrap = kwargs.pop('wrap', 0)
		root = master.nametowidget('.')
		fn = root.register(self._on_command)
		kwargs['command'] = kwargs.get('command', (fn, '%d')) ##on button
		self._callback = kwargs.pop('callback', self.__void__)
		self._inc = kwargs['increment'] = kwargs.get('increment', 1)
		self.var.set(kwargs['value'])
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		self.__xinit__(master, **widget_args)
		if isinstance(self.get_root(), rapidTk):
			self.get_root().sm.add_widget(self, self._on_scroll)
		if layout.method is not None:
			layout.inline(self)
	def __void__(self, *args):
		pass
	def _on_command(self, direction):
		if direction == 'up': #button up click
			self.spin(1, self.wrap)
			self._callback(self, 1)
		elif direction == 'down': #button down click
			self.spin(0, self.wrap)
			self._callback(self, 0)
	def _on_scroll(self, event):
		if event.delta >= 0: #mouse scroll up
			self.spin(1, self.wrap)
			self._callback(self, 1)
		elif event.delta <= 0: #mouse scroll down
			self.spin(0, self.wrap)
			self._callback(self, 0)


class cDate(cFrame, widgetBase):
	_widgetBase__widget_type = rtktypes.strget
	@time_it
	def __xinit__(self, master, **kwargs):
		super(cDate, self).__init__(master, **kwargs)
		widgetBase.__init__(self, master, **kwargs)
	@time_it
	def __init__(self, master, **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		base_formats = [
		'dd{sep}mm{sep}yyyy',
		'dd{sep}mm{sep}yy',
		'yyyy{sep}mm{sep}dd',
		'yy{sep}mm{sep}dd',
		'mm{sep}dd{sep}yyyy',
		'mm{sep}dd{sep}yy'
		]
		seperators = ['/', '-', '.']
		formats = []
		formats.append([[x.format(sep=y) for y in seperators] for x in base_formats])
		self.formats = [item for sub in formats[0] for item in sub]
		self.d_format = kwargs.pop('format', 'dd/mm/yyyy')
		if self.d_format not in self.formats:
			local_formats = '\t\n'.join(self.formats)
			raise ValueError(f"{self.d_format} is not a valid format, please select from one of the standard formats:\n{local_formats}")
		self.seperator = self.d_format[2] if self.d_format[2] in seperators else self.d_format[4]
		self.__xinit__(master)
		
	def _create_entries(self, **kwargs):
		
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		

		if layout.method is not None:
			layout.inline(self)
