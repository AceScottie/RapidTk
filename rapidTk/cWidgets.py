import logging
#tkinter overrides
from rapidTk.tkoverride import Frame, Label, Button, Entry, Checkbutton, Radiobutton, Listbox, Scale, Canvas, Menu, Text, ScrolledText, Scrollbar
#tkinter imports
from tkinter.constants import TOP, LEFT, RIGHT, BOTTOM, CENTER, X, Y, BOTH, END, INSERT
from tkinter import StringVar, IntVar, DoubleVar, Event
from tkinter.__init__ import Menu as tkMenu
from tkinter.ttk import Treeview, Combobox
from tkinter.ttk import Style
#rapidTk imports
from rapidTk.__main__ import rapidTk
from rapidTk.rTkOverrides import OptionMenu, Spinbox
from rapidTk.flags import __ttk_enabled__
from rapidTk.rTkErrors import *
from rapidTk.rTkUtils import widgetBase, time_it, inline_layout, _UniqueIdentifiers, iList
from rapidTk.rTkTheme import _ThemeManager, style_widget
import rapidTk.types as rtktypes
import sys
##platform specific
if sys.platform == "win32":
	from rapidTk.rTkUtils import clipboard_WIN as clipboard
elif sys.platform == "linux":
	from rapidTk.rTkUtils import clipboard_LINUX as clipboard
elif sys.platform == "macos":
	from rapidTk.rTkUtils import clipboard_MAC as clipboard



class cFrame(Frame, widgetBase):
	"""
	Basic Frame, Similar to tkinter.Frame.
	Supports inline layouts using the standard layout params of Pack, Place and Grid.
	Uses overriden tkiniter classes.
	"""
	_widgetBase__widget_type = rtktypes.noget
	@time_it
	def __init__(self, master, **kwargs):
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		super(cFrame, self).__init__(master, **widget_args)
		if layout.method is not None:
			layout.inline(self)


class cLabel(Label, widgetBase):
	_widgetBase__widget_type = rtktypes.singleget
	@time_it
	def __init__(self, master, **kwargs):
		self.bg = kwargs.get('bg', kwargs.get('background', None))
		self.fg = kwargs.get('fg', kwargs.get('foreground', None))
		self.var = kwargs['textvariable'] = kwargs.get('textvariable', StringVar())
		self.var.set(kwargs.get('text', ''))
		self.var.trace("w", self._update)
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		super(cLabel, self).__init__(master, **widget_args)
		if self.bg is None:
			self.bg = self.cget('background')
		if self.fg is None:
			self.fg = self.cget('foreground')
		
		##style_widget(self, kw_style, "TFrame") ##going to be part of ttk and theme manager
		if layout.method is not None:
			layout.inline(self)
	def get(self, *args): return widgetBase.get(self, *args)
	def set(self, *args): return widgetBase.set(self, *args)
	def insert(self, *args): return widgetBase.insert(self, *args)
	def delete(self, *args): return widgetBase.delete(self, *args)

	def _update(self, *args):
		self.configure(text=self.var.get())


class cButton(Button, widgetBase):
	_widgetBase__widget_type = rtktypes.disget
	@time_it
	def __init__(self, master,  **kwargs):
		kwargs['cursor'] = kwargs.pop('cursor', 'hand2')
		self.var = kwargs['textvariable'] = kwargs.get('textvariable', StringVar())
		self.var.set(kwargs.get('text', ''))
		self._command = kwargs.get('command', None)
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		super(cButton, self).__init__(master, **widget_args)
		#logging.getLogger('rapidTk').rtkverbose(f"created widget {self} with args {widget_args}")
		if layout.method is not None:
			layout.inline(self)
	def get(self, *args): return widgetBase.get(self, *args)
	def set(self, *args): return widgetBase.set(self, *args)
	def insert(self, *args): return widgetBase.insert(self, *args)
	def delete(self, *args): return widgetBase.delete(self, *args)


class cEntry(Entry, widgetBase):
	_widgetBase__widget_type = rtktypes.singleget
	@time_it
	def __init__(self, master, **kwargs):
		logging.getLogger('rapidTk').rtkverbose(f"cEntry got kwargs {kwargs}")
		value = kwargs.pop('value', '')
		kwargs['textvariable'], self.var = (kwargs.get('textvariable', StringVar()),)*2
		if value != '':
			self.var.set(value)
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		logging.getLogger('rapidTk').rtkverbose(f"cEntry got widget_args {widget_args} and {layout.method}")
		super(cEntry, self).__init__(master, **widget_args)
		logging.getLogger('rapidTk').rtkverbose(f"created cEntry {self} with args {widget_args}")
		##style_widget(self, kw_style, "TFrame") ##going to be part of ttk and theme manager
		self.__menu = cMenu(self, tearoff=0)
		self.__menu.add_command(label="Cut", command=self._cut)
		self.__menu.add_command(label="Copy", command=self._copy)
		self.__menu.add_command(label="Paste", command=self._paste)
		self.__menu.add_command(label="Select All", command=self._select_all)
		self.bind("<Button-3>", self._do_popup)
		
		if layout.method is not None:
			layout.inline(self)
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
	def get(self, *args): return widgetBase.get(self, *args)
	def set(self, *args): return widgetBase.set(self, *args)
	def insert(self, *args): return widgetBase.insert(self, *args)
	def delete(self, *args): return widgetBase.delete(self, *args)


class cCanvas(Canvas, widgetBase):
	_widgetBase__widget_type = rtktypes.noget
	@time_it
	def __init__(self, master,  **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		if 'bd' not in kwargs or 'boarder' not in kwargs:
			kwargs['bd'] = -2
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		super(cCanvas, self).__init__(master, **widget_args)
		##style_widget(self, kw_style, "TFrame") ##going to be part of ttk and theme manager
		if layout.method is not None:
			layout.inline(self)


class cTreeview(Treeview, widgetBase):
	_widgetBase__widget_type = rtktypes.treeget
	@time_it
	def __init__(self, master, **kwargs):
		self.master = master
		self.iid = 0
		self.detached_data = []
		bg = kwargs.pop('bg', '#FFFFFF')
		fg = kwargs.pop('fg', '#000000')
		self.values = iList()

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
		super(cTreeview, self).__init__(master, **widget_args)
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
	def columns(self):
		return self['columns']
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
		if iid == None:
			iid = self.iid
		self.iid += 1
		self.values[iid] = (values)
		super().insert(parent=parent, index=index, iid=iid, tags=tags+(self.iid,), text=text, values=values)
		self.tag_bind(self.iid, '<Motion>', self._highlight_row)

		return iid
	@time_it
	def get_rows(self):
		return self.values.get()
	def get_row(self, index):
		try:
			int(index)
			return self.values[int(index)]
		except:
			raise Exception("index must be `int` and must be in the iList")
	@time_it
	def item(self, index, **kwargs):
		vals = kwargs.get('values', None)
		row = self.values[int(index)]
		for i in range(len(row)):
			pass ##TODO: implement this
		return super().item(index, **kwargs)
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
	def __init__(self, master, **kwargs):
		value = kwargs.pop('value', None)
		self.var = kwargs['textvariable'] = kwargs.pop('textvariable', StringVar())
		if value:
			self.var.set(value)
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		super(cScrolledText, self).__init__(master, **widget_args)
		#self.trace('w', self.__wright)
		if isinstance(self.get_root(), rapidTk):
			self.get_root().sm.add_widget(self)
		##style_widget(self, kw_style, "TFrame") ##going to be part of ttk and theme manager
		if value != None:
			self.insert(0, value)
		#style_widget(self, kw_style, "TScrolledText")
		self.__menu = tkMenu(self, tearoff=0)
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
	def old_select_all(self):
		self.select_range(0,END)
	@time_it
	def _select_all(self):
		self.tag_add(SEL, "1.0", END)
		self.mark_set(INSERT, "1.0")
		self.see(INSERT)
		return 'break'

	def __wright(self, *args):
		print(args)
	
	def get(self, *args): return widgetBase.get(self, *args)
	def set(self, *args): return widgetBase.set(self, *args)
	def insert(self, *args): return widgetBase.insert(self, *args)
	def delete(self, *args): return widgetBase.delete(self, *args)


class cCheckbutton(Checkbutton, widgetBase):
	_widgetBase__widget_type = rtktypes.intget
	@time_it
	def __init__(self, master, **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		self.text = kwargs['textvariable'] = kwargs.pop("textvariable", StringVar()) ##text property for the lable
		self.text.set(kwargs.get('text', ''))
		self.text.trace("w", self._update) ##updates the label when text property updated
		kwargs['selectcolor'] = kwargs.pop("selectcolor", master.get_root().option_get('background', '.'))
		self.var = kwargs['variable'] = kwargs.get('variable', IntVar())
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		super(cCheckbutton, self).__init__(master, **widget_args)
		if layout.method is not None:
			layout.inline(self)
	
	def get(self, *args): return widgetBase.get(self, *args)
	def set(self, *args): return widgetBase.set(self, *args)
	def _update(self, *args):
		self.configure(text=self.text.get())


class cOptionMenu(OptionMenu, widgetBase): ##OptionMenu overrideen from rTkOverrides
	_widgetBase__widget_type = rtktypes.strget
	@time_it
	def __init__(self, master, **kwargs): ##TODO: fix removing invalid options from this and add to reOptionMenu
		print(f"cOptionMenu.__init({master}, {kwargs})")
		self.options = kwargs.pop('options', kwargs.pop('values', [])) ##this will be the full list of options used for validation
		kwargs['value'] = self._value = kwargs.pop('value', None)
		self.selectable_options = kwargs['values'] = [str(x) for x in self.options if x != self._value] ## modified options for display
		self.var = kwargs['textvariable'] = kwargs.pop('variable', kwargs.pop('textvariable',StringVar(master)))
		
		if self._value is not None:
			self.var.set(self._value)
		else:
			self._value = self.options[0]
			self.var.set(self.options[0])
			del kwargs['values'][0]
		#if self._value in self.selectable_options:
		#	self.selectable_options.remove(self._value)
		kwargs['show_cur'] = kwargs.pop('show_cur', False)
		nv = kwargs.pop('non_valid', [])
		x = kwargs.pop('default', None)
		if x is not None:
			raise Exception('keyword "default" has been Deprecated. Please use "value" instead')
		
		kwargs['takefocus'] = kwargs.pop('takefocus', 1) ##allows tab selection
		#kwargs['values'] = self.selectable_options
		
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		super(cOptionMenu, self).__init__(master, **widget_args)
		self['menu'].configure(activebackground="blue", activeforeground="white")
		self.bind("<space>", self._open_option_menu)
		#self['menu'].bind("<space>", self._on_select)

		if self.var is not None:
			self.var.trace("wu", self._on_var_change)

		if layout.method is not None:
			layout.inline(self)
	#def _on_select(self, event):
	#	print("item selected")

	def _on_var_change(self, *args):
		val = self.var.get()
		self.reset_values(value=val, values=[str(x) for x in self.options if str(x) != str(val)])

	def _on_widget_change(self, event=None):
		if self.var is not None:
			self.var.set(self.tk.call(self._w, 'get', 0, "end"))
	@time_it
	def _open_option_menu(self, event):
		obj = event.widget
		x = obj.winfo_rootx()
		y = obj.winfo_rooty() + obj.winfo_height()
		obj["menu"].post(x, y)
		return "break"
	def get(self, *args): return widgetBase.get(self, *args)
	def set(self, *args):
		print("cOpt setter")
		widgetBase.set(self, *args)
		self._on_var_change()
	def insert(self, *args): return widgetBase.insert(self, *args)
	def delete(self, *args): return widgetBase.delete(self, *args)

class cCombobox(Combobox, widgetBase):
	_widgetBase__widget_type = rtktypes.strget
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
		super(cCombobox, self).__init__(master, **widget_args)
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
	def unselect(self, a=None, b=None, c=None, e=None):
		self.selection_clear()
	@time_it
	def __repr__(self):
		return "<%s instance at %s>" % (self.__class__.__name__, id(self))

	def get(self, *args): return widgetBase.get(self, *args)
	def set(self, *args): return widgetBase.set(self, *args)
	def insert(self, *args): return widgetBase.insert(self, *args)
	def delete(self, *args): return widgetBase.delete(self, *args)

#TODO: add option for MenuButton

class cMenu(Menu, widgetBase):
	_widgetBase__widget_type = rtktypes.noget
	@time_it
	def __init__(self, master, **kwargs):
		super(cMenu, self).__init__(master, **kwargs)


class cRadiobutton(Radiobutton, widgetBase):
	_widgetBase__widget_type = rtktypes.intget
	@time_it
	def __init__(self, master, **kwargs):
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		super(cRadiobutton, self).__init__(master, **widget_args)
		if layout.method is not None:
			layout.inline(self)


class cListbox(Listbox, widgetBase):
	_widgetBase__widget_type = rtktypes.strget
	@time_it
	def __init__(self, master, **kwargs):
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		super(cListbox, self).__init__(master, **widget_args)
		if layout.method is not None:
			layout.inline(self)


class cScale(Scale, widgetBase):
	_widgetBase__widget_type = rtktypes.intget
	@time_it
	def __init__(self, master, **kwargs):
		#self.uuid = _UniqueIdentifiers().new()
		self.var, kwargs['variable'] = (kwargs.pop('variable', IntVar()),)*2
		vals = kwargs.pop('range', [0, 1])
		kwargs['from_'] = vals[0]
		kwargs['to'] = vals[-1]
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		super(cScale, self).__init__(master, **widget_args)
		if layout.method is not None:
			layout.inline(self)


class cSpinbox(Spinbox, widgetBase): ##Spinbox overrideen from rTkOverrides
	_widgetBase__widget_type = rtktypes.strget
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
		super(cSpinbox, self).__init__(master, **widget_args)
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
		super(cDate, self).__init__(master, **kwargs)
		
	def _create_entries(self, **kwargs):
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		if layout.method is not None:
			layout.inline(self)


class cText(Text, widgetBase):
	_widgetBase__widget_type = rtktypes.multiget
	def __init__(self, master=None, **kwargs):
		self.var = kwargs['textvariable'] = kwargs.pop("textvariable", StringVar())
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		super(cText, self).__init__(master, **widget_args)
		if layout.method is not None:
			layout.inline(self)
	def get(self, *args): return widgetBase.get(self, *args)
	def set(self, *args): return widgetBase.set(self, *args)
	def insert(self, *args): return widgetBase.insert(self, *args)
	def delete(self, *args): return widgetBase.delete(self, *args)



class cScrollbar(Scrollbar, widgetBase):
	_widgetBase__widget_type = rtktypes.noget
	def __init__(self, master, **kwargs):
		super(cScrollbar, self).__init__(master, **kwargs)