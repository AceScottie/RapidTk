#tkinter overrides
from rapidTk.tkoverride import Misc
#tkinter imports
from tkinter import StringVar, IntVar, Event, INSERT, END, Toplevel
from tkinter import TOP, LEFT, RIGHT, BOTTOM, CENTER, X, Y, BOTH, SOLID
from tkinter import N, E, S, W, NW, NE, SE, SW, NSEW
from tkinter import VERTICAL, HORIZONTAL 
from tkinter.simpledialog import askstring, askinteger
##additional imports
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps
import re
from itertools import count
from datetime import datetime, date
from collections.abc import Callable
from dateutil.relativedelta import relativedelta
from math import sin, cos, pi
import win32gui
import win32con
import win32api

#rtk imports
from rapidTk.__main__ import PackProcess, GridProcess, rapidTk
from rapidTk.cWidgets import cEntry, cButton, cFrame, cLabel, cCanvas, cTreeview, cCheckbutton, cScrolledText, cMenu, cSpinbox, cOptionMenu, cScrollbar
from rapidTk.rTkErrors import *
from rapidTk.rTkUtils import coord, widgetBase, widgetBase_override, simpledate, cache
from rapidTk.rTkUtils import time_it, inline_layout
from rapidTk.rTkManagers import _WindowManager
from rapidTk.rTkTheme import _ThemeManager
import rapidTk.types as rtktypes
try:
	import tkcalendar
	from rapidTk.rTkCalendar.rTkCalendar import DateEntry, cDateEntry, reDateEntry
except:
	raise DateEntryNotFoundError
	class DateEntry:
		def __init__(self, master, **kwargs):
			raise DateEntryNotFoundError
	class cDateEntry:
		def __init__(self, master, **kwargs):
			raise DateEntryNotFoundError
	class reDateEntry:
		def __init__(self, master, **kwargs):
			raise DateEntryNotFoundError


class autoEntry(cEntry, widgetBase):
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)	
		self.bt = None
		self.aw = None

		##custom kwargs
		self.options =  kwargs.pop('auto', [])
		self.len = kwargs.pop('len', 3)
		#assertValue(f'{self.len} >= 1', "len must be greater than 1")
		self.anchor = kwargs.pop('anchor', "center")
		self.autobg = kwargs.pop('autobg', '#DDDDDD')
		self.autofg = kwargs.pop('autofg', '#000000')
		self.hovertext = kwargs.pop('hovertext', '#BBBBBB')
		self.hovercolor = kwargs.pop('hovercolor', '#000000')
		self.cursor_color = kwargs.pop('cursor_color', '#000000')
		self.strict = kwargs.pop('strict', 0) in [1, '1', True]
		self.autoshow = kwargs.pop('autoshow', 0) in [1, '1', True]


		self.bg = kwargs['background'] = kwargs['bg'] = kwargs.get('bg', kwargs.get('background', '#AAFFAA'))
		self.fg = kwargs['foreground'] = kwargs['fg'] = kwargs.pop('fg', kwargs.pop('foreground','#000000'))

		kwargs['insertbackground'] = kwargs.pop('insertbackground', self.cursor_color)
		kwargs['textvariable'] = kwargs.pop('textvariable', StringVar())
		self.sv = kwargs['textvariable']

		cEntry.__init__(*(self, master), **kwargs)

		self.aw = cCanvas(self.winfo_toplevel(), bg="white", borderwidth=2, relief="raised")
		if isinstance(self.get_root(), rapidTk):
			self.get_root().sm.add_widget(self.aw)
		self.bind('<Button-2>', self._full)
		self.bind('<F1>', self._full)
		if self.autoshow:
			self.bind('<Button-1>', self._full)
			self.bind('<FocusIn>', self._full)
		self.bind('<FocusOut>', self._close_overlay)
		self.winfo_toplevel().bind_all('<Button-1>', self._close_overlay)
		self.sv.trace("w", lambda name, index, mode, e=Event(): self._autocomplete(e))

	#def __click_to_close(self, event):
	#	self.get_root().unbind_all('<Button-1>')
	#	self._close_overlay(event)
	def _autocomplete(self, event):
		if self.winfo_toplevel().focus_get() != self:
			return
		self.aw.update()
		intxt = self.get()[0]
		valid = []
		if len(intxt) >= self.len:
			for opt in self.options:
				if self.strict:
					if(opt[0:len(intxt)].lower() == intxt.lower()):
						valid.append(opt)
				else:
					print(opt)
					if intxt.lower() in opt.lower():
						valid.append(opt)
			if len(valid) > 0:
				xpos = self.winfo_rootx() - self.winfo_toplevel().winfo_rootx()
				ypos = self.winfo_rooty() - self.winfo_toplevel().winfo_rooty() + self.winfo_height()
				if self.bt != None and self.bt.winfo_exists():
					self._re_options(valid)
				else:
					self._overlay(valid, coord(xpos,ypos))
			else:
				self._close_overlay()
		else:
			self._close_overlay()
	def _re_options(self, options):
		self.bt.delete(*self.bt.get_children())
		self.bt.update()
		for o in range(len(options)):
			self.bt.insert(parent='', index='end', iid=o, text='', values=[options[o]])
	def _autoshow(self, event):
		if self.get() != "":
			self._autocomplete(event)
		else:
			self._full(event)
	def _full(self, event):
		if not self.aw.winfo_ismapped():
			xpos = self.winfo_rootx() - self.winfo_toplevel().winfo_rootx()
			ypos = self.winfo_rooty() - self.winfo_toplevel().winfo_rooty() + self.winfo_height()
			self._overlay(self.options, coord(xpos,ypos))
	def _overlay(self, options, pos):
		if self.aw.winfo_ismapped():
			self._close_overlay()	
		self.aw.configure(width=self.winfo_width(), height=100)
		self.aw.pack_propagate(False)
		self.aw.place(x=pos.x, y=pos.y)
		if isinstance(self.get_root(), rapidTk):
			self.get_root().sm.add_widget(self.aw)
		self.bt = cTreeview(self.aw, bg=self.autobg, fg=self.autofg, side=LEFT)
		vsb = Scrollbar(self.aw, orient="vertical",command=self.bt.yview)
		self.bt.configure(yscrollcommand=vsb.set)
		self.bt['show'] = ''
		vsb.pack(side=RIGHT, fill=BOTH)
		cols=['options']
		self.bt.set_cols(cols)
		self.bt.column('options',anchor=self.anchor, width=self.winfo_width()-15)
		self.bt.tag_configure('focus', background=self.hovercolor, foreground=self.hovertext)
		self.bt.bind("<Motion>", self._highlight_row)
		self.bt.bind("<Button-1>", self._complete)
		for o in range(len(options)):
			self.bt.insert(parent='', index='end', iid=o, text='', values=[options[o]])
	def _highlight_row(self, event):
		if self.bt != None:
			iid = self.bt.identify_row(event.y)
			for x in self.bt.get_children():
				if x != iid:
					self.bt.item(x, tags='')
				else:
					self.bt.item(x, tags='focus')
	def _complete(self, event):
		tree = event.widget
		iid = tree.identify_row(event.y)
		text = tree.item(iid)['values'][0]
		self.delete(0, END)
		self.insert(0, text)
		self._close_overlay()
	def _close_overlay(self, event=None):
		if self.aw != None:
			self.aw.place_forget()
			for child in self.aw.winfo_children():
				child.destroy()
			self.bt = None
	def destroy(self):
		self._close_overlay()
		super().destroy()
	def isvalid(self):
		return self.sv.get() in self.options
	def get(self):
		return self.sv.get(), self.isvalid()
	def __del__(self):
		self._close_overlay()
		#super().destroy()
class iButton(cButton, widgetBase):
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		image = kw_wid['image']
		width = kw_wid['width']
		hm = kw_wid['hovermode']
		hi = kw_wid['hoverimage']
		cm = kw_wid['clickmode']
		ci = kw_wid['clickimage']
		del kwargs['image']
		del kwargs['width']
		cButton.__init__(*(self, master), **kwargs)
		self.configure(image=self.get_image(image, width))
		if len(kw_pak) != 0:
			self.pack(kw_pak)
	def _hover(self):
		pass
	def _click(self):
		pass
	def get_image(self, image, width):
		side = Image.open(".\\assets\\"+image+"_side.png")
		middle = Image.open(".\\assets\\"+image+"_mid.png")
		otherside = ImageOps.mirror(side)
		
		output = Image.new('RGBA', (width+side.size[0]*2, h), (0, 0, 0, 255))
		output.paste(side)
		output.paste(otherside, (output.size[0]-side.size[0], 0))
		left = output.size[0]-(side.size[0]*2)
		i = 0
		while left > 0:
			output.paste(middle, (side.size[0]+(middle.size[0]*i), 0))
			i += 1
			left -= middle.size[0]
		self.image = ImageTk.PhotoImage(output)
		return self.image ##TODO: complete image button for layouts
class scrollArea(cFrame, widgetBase):
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		#kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		self.scroll_v = None
		self.scroll_h = None
		self.h = kwargs.pop('h', 0)
		self.v = kwargs.pop('v', 0)
		
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		super(scrollArea, self).__init__(master, **widget_args)
		
		self.sCanvas = cCanvas(self, side=TOP, fill=BOTH, expand=1)
		if isinstance(self.get_root(), rapidTk):
			self.get_root().sm.add_widget(self.sCanvas)
		self.sFrame = cFrame(self.sCanvas, side=LEFT, fill=BOTH, expand=1)
		self.cw = self.sCanvas.create_window((0, 0), window=self.sFrame, anchor=NW)
		if self.h in [1, "1", True]:
			self.scroll_h = cScrollbar(master, orient=VERTICAL, command=self.sCanvas.yview)
			self.sCanvas.configure(yscrollcommand=self.scroll_h.set)
			self.scroll_h.pack(side=RIGHT, fill=Y)
		if self.v in [1, "1", True]:
			self.scroll_v = cScrollbar(master, orient=HORIZONTAL, command=self.sCanvas.xview)
			self.sCanvas.config(xscrollcommand=self.scroll_v.set)
			self.scroll_v.pack(side=BOTTOM, fill=X)
		self.sFrame.bind("<Configure>", self._update_scrollregion)
		self.sCanvas.bind('<Configure>', self._FrameWidth)
		
		if layout.method is not None:
			layout.inline(self)
	def _update_scrollregion(self, event):
		self.sCanvas.configure(scrollregion=self.sCanvas.bbox("all"))
	def _FrameWidth(self, event):
		if self.v == 1 and event.width > self.sFrame.winfo_width():
			self.sCanvas.itemconfig(self.cw, width=event.width-4)
		elif self.v == 0:
			self.sCanvas.itemconfig(self.cw, width=event.width)
		if self.h == 1 and event.height > self.sFrame.winfo_height():
			self.sCanvas.itemconfig(self.cw, height=event.height-4)
		elif self.h == 0:
			self.sCanvas.itemconfig(self.cw, height=event.height)
class movableWindow(cCanvas, widgetBase):
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		self.motion = False
		self.bg = kwargs.pop('bg', kwargs.pop('background', None))
		self.fg = kwargs.pop('fg', kwargs.pop('foreground', None))
		if self.bg is None:
			x = master.get_root().option_get('background', '.')
			self.bg = x if x != '' else '#FFFFFF'
		if self.fg is None:
			x = master.get_root().option_get('foreground', '.')
			self.bg = x if x != '' else '#000000'
		self.width = kwargs['width'] = kwargs.get('width', 400)
		self.height = kwargs['height'] = kwargs.get('height', 400)
		self.title = kwargs.pop('title', False)
		self._cmd = kwargs.pop('command', None)
		kwargs['borderwidth'] = kwargs.get('borderwidth', 1)
		kwargs['relief'] = kwargs.get('relief', "groove")
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		cCanvas.__init__(*(self, master), **widget_args)
		self.root = self.get_root()
		self.wm = self.get_root().wm
		self.pid = self.root.uid.new()
		self.posx=0
		self.posy=0
		self.binds = {}
		self.rootbind = None
		self.popped = None
		self.widgets = {}
		self.manager = None
		if self.wm:
			self.wm.add_pid(self.pid, self)
		self._create()
	def _create(self):
		self.pack_propagate(False)
		self.place(x=self.root.winfo_width()/2-(self.width/2), y=(self.root.winfo_height()/2)-(self.height/4))
		self.top = cFrame(self, borderwidth=1, relief="raised", side=TOP, fill=X)
		self.body= cFrame(self, borderwidth=2, relief="ridge", side=TOP, fill=BOTH, expand=1)
		if self.title:
			move = cLabel(self.top, text=self.title, fg=self.fg, justify=CENTER, font=("Helvetica", 10), cursor="fleur", side=LEFT, fill=X, expand=1)
		else:
			move = cLabel(self.top, text="", justify=CENTER, font=("Helvetica", 10), cursor="fleur", side=LEFT, fill=X, expand=1)
		self.close = cButton(self.top, text="X", relief="raised", width=2, borderwidth=1, fg=self.fg, side=RIGHT, command=self._close)
		self.minimize = cButton(self.top, text="🗕", relief="raised", width=2, borderwidth=1, fg=self.fg, side=RIGHT, command=self._minimize)
		#popout = cButton(self.top, text="⇱", relief="raised", width=2, borderwidth=1, fg=self.fg, side=RIGHT, command=self._popout)
		self.binds["<Button-1>"] = move.bind("<Button-1>", self._click)
		self.binds["<B1-Motion>"] = move.bind("<B1-Motion>", self._move)
		self.binds["<ButtonRelease-1>"] = move.bind("<ButtonRelease-1>", self._drop)
		self.rootbind = self.root.bind("<Configure>", self._drop)
	def _click(self, event):
		Misc.lift(self)
	def _move(self, event):
		if(self.root.winfo_pointerx() != "??" and self.root.winfo_pointery() != "??"):
			self.posx, self.posy = self._calc_move(self.root.winfo_pointerx(), self.root.winfo_rootx(), self.winfo_width(), self.root.winfo_pointery(), self.root.winfo_rooty())
			self.place(x=self.posx, y=self.posy)
			#self.update()
	@cache
	def _calc_move(self, rx, rrx, w, ry, rry):
		return (rx-rrx-w/2), ry-rry-10
	def _drop(self, event):
		if self.winfo_x() + self.winfo_width() > self.root.winfo_width():
			self.place(x=self.root.winfo_width()-self.winfo_width())
			self.posx = self.root.winfo_width()-self.winfo_width()
		elif self.winfo_x() < 0:
			self.place(x=0)
			self.posx = 0
		if self.winfo_y() + self.winfo_height() > self.root.winfo_height():
			self.place(y=self.root.winfo_height()-self.winfo_height())
			self.posy = self.root.winfo_height()-self.winfo_height()
		elif self.winfo_y() < 0:
			self.place(y=10)
			self.posy = 10
	def _clone_widget(self, widget, master=None):
		##src: https://stackoverflow.com/questions/46505982/is-there-a-way-to-clone-a-tkinter-widget/69538200#69538200
		parent = master if master else widget.master
		cls = widget.__class__
		print(cls)
		cfg = {key: widget.cget(key) for key in widget.configure()}
		if 'textvariable' in cfg: ##dirty fix #1 variables get translated to objects so this gets the current variable and reassigns it to the new widget
			if isinstance(widget, cCheckbutton): ##dirty fix #2: checkbuttons have a text and var variables for the label text and the item.
				cfg['textvariable'] = widget.text
			else:
				cfg['textvariable'] = widget.var
		if 'variable' in cfg:
			cfg['variable'] = widget.var
		cloned = cls(parent, **cfg)
		if not isinstance(widget, cDateEntry): ##dirty fix #4: cDateEntry has a bunch of custom only kword children which are created automatically.
			for child in widget.winfo_children():
				print(type(child))
				child_cloned = self._clone_widget(child, master=cloned)
				try:##dirty fix #3 right click menus are not packed so these fail and error. mayby replace else with elif on pack case
					if child.grid_info():
						grid_info = {k: v for k, v in child.grid_info().items() if k not in {'in'}}
						child_cloned.grid(**grid_info)
					elif child.place_info():
						place_info = {k: v for k, v in child.place_info().items() if k not in {'in'}}
						child_cloned.place(**place_info)
					else:
						pack_info = {k: v for k, v in child.pack_info().items() if k not in {'in'}}
						child_cloned.pack(**pack_info)
				except:
					pass
		return cloned
	def _popout(self, register=None): ##pop out to a new toplevel window
		##register = relative path of widgets from body
		## when cloning check if relative path matches and if so switch widget from relative dict to new path 
		## use global popped attr to return the popped widget stuff maybe ? maybe add a create method here to keep the widgets inside this class
		self.popped = Toplevel()
		self.popped.geometry(f"{self.height}x{self.width}+{self.root.winfo_x()+int(self.posx)}+{self.root.winfo_y()+int(self.posy)}")
		self._clone_widget(self.body, self.popped).pack(side=TOP, fill=BOTH, expand=1)
		self._close()

	def set_manager(self, manager):
		self.pp = manager
	def create(widget, master, kw, lay):
		if self.pp is None:
			raise Exception("Process manager is reqired for this, use widget.set_manager(type) type:PackProcess, GridProcess, PlaceProcess. (do not include ()!)")
		p = self.pp.add(widget(master, **kw), **lay)
		self.widgets[str(p)] = p
	def process(self):
		self.pp.process()

	def _minimize(self):
		if self.wm:
			pos = self.wm._get_deactive_space()+1
			self.wm._set_inactive(self.pid)
		else:
			pos = 0
		self.body.pack_forget()
		self.configure(height=25)
		##place in bottom corner stacking with others
		##TODO: add object width to wm and offset for other windows
		self.place(x=0, y=self.root.winfo_height()-(pos*25))
		self.minimize.configure(text="🗖", command=self._maximize)
	def _maximize(self):
		if self.wm:
			self.wm._set_active(self.pid)
			Misc.lift(self)
		self.body.pack(side=TOP, fill=BOTH, expand=1)
		self.configure(height=self.height)
		self.place(x=self.posx, y=self.posy)
		self.minimize.configure(text="🗕", command=self._minimize)
	def _close(self):
		if self.wm and self.pid in self.wm.pids:
			self.wm.remove(self.pid)
		#for k, v in self.binds.items(): ##this causes an error. Something with the way unbind doesnt delete the tcl entry so it is attempted to be removed twice
		#	self.unbind(k, v)
		self.root.unbind('<Configure>', self.rootbind)
		self.destroy()
	def __del__(self):
		self._close()
class ImageLabel(cLabel, widgetBase):
	def __init__(self, master, **kwargs):
		super(ImageLabel, self).__init__(master)
	def load(self, im, bg="white"):
		if isinstance(im, str):
			im = Image.open(im)
		self.loc = 0
		self.frames = []
		try:
			for i in count(1):
				self.frames.append(ImageTk.PhotoImage(im.copy()))
				im.seek(i)
		except EOFError:
			pass
		try:
			self.delay = im.info['duration']
		except:
			self.delay = 100
		if len(self.frames) == 1:
			self.config(image=self.frames[0], bg=bg)
		else:
			try:
				self._next_frame()
			except:
				pass
	def unload(self):
		self.config(image=None)
		self.frames = None
	def _next_frame(self):
		if self.frames:
			self.loc += 1
			self.loc %= len(self.frames)
			try:
				self.config(image=self.frames[self.loc])
				self.get_root().after(self.delay, self._next_frame)
			except:
				pass
class Tooltip(cLabel, widgetBase):
	def __init__(self, master,**kwargs):
		self.master = master
		self.waittime = kwargs.pop('waittime', 400)
		self.wraplength = kwargs.pop('wraplength', 250)
		self.pad = kwargs.pop('pad', (5, 3, 5, 3))
		kwargs["text"] = kwargs.get('text', "")
		kwargs["wraplength"] = kwargs.get('wraplength', 400)
		kwargs["background"] = kwargs.get('bg', '#FFFFEA')
		kwargs["foreground"] = kwargs.get('fg', '#000000')
		kwargs["relief"] = kwargs.get('relief', SOLID)
		kwargs["borderwidth"] = kwargs.get('borderwidth', 0)
		kwargs["fg"] = kwargs.get('fg', '#000000')
		kwargs["fg"] = kwargs.get('fg', '#000000')
		self.kwargs = kwargs
		super(Tooltip, self).__init__(master, **kwargs)
		self.master.bind("<Enter>", self.onEnter)
		self.master.bind("<Leave>", self.onLeave)
		self.master.bind("<ButtonPress>", self.onLeave)
		
		self.id = None
		self.tw = None
	def onEnter(self, event=None):
		self.schedule()
		pass
	def onLeave(self, event=None):
		self.unschedule()
		self.hide()
	def schedule(self):
		self.unschedule()
		self.id = self.master.after(self.waittime, self.show)
	def unschedule(self):
		id_ = self.id
		self.id = None
		if id_:
			self.after_cancel(id_)
	def show(self):
		def tip_pos_calculator(widget, label,*,tip_delta=(10, 5), pad=(5, 3, 5, 3)):
			w = widget
			s_width, s_height = w.winfo_screenwidth(), w.winfo_screenheight()
			width, height = (pad[0] + label.winfo_reqwidth() + pad[2],pad[1] + label.winfo_reqheight() + pad[3])
			mouse_x, mouse_y = w.winfo_pointerxy()
			x1, y1 = mouse_x + tip_delta[0], mouse_y + tip_delta[1]
			x2, y2 = x1 + width, y1 + height
			x_delta = x2 - s_width
			if x_delta < 0:
				x_delta = 0
			y_delta = y2 - s_height
			if y_delta < 0:
				y_delta = 0
			offscreen = (x_delta, y_delta) != (0, 0)
			if offscreen:
				if x_delta:
					x1 = mouse_x - tip_delta[0] - width
				if y_delta:
					y1 = mouse_y - tip_delta[1] - height
			offscreen_again = y1 < 0
			if offscreen_again:
				y1 = 0
			return x1, y1
		pad = self.pad
		self.tw = Toplevel(self)
		self.tw.wm_overrideredirect(True)
		win = cFrame(self.tw,background=self.bg,borderwidth=0)
		label = cLabel(win,**self.kwargs)
		label.grid(padx=(pad[0], pad[2]),pady=(pad[1], pad[3]),sticky=NSEW)
		win.grid()
		x, y = tip_pos_calculator(self, label)
		self.tw.wm_geometry("+%d+%d" % (x, y))
	def hide(self):
		if self.tw:
			self.tw.destroy()
		self.tw = None
class Calendar(cFrame, widgetBase):
	def __init__(self, master, **kwargs):
		self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		self.short_days = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
		self.months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
		self.short_months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
		self.date = kwargs.pop('date', simpledate.now())
		self.func = kwargs.pop('func', self.__ignore)
		super(Calendar, self).__init__(master, **kwargs)

		pp = PackProcess()
		t_frame = pp.add(cFrame(self), side=TOP, fill=X)
		self.c_frame = pp.add(cFrame(self), side=TOP, fill=X)
		pp.add(cButton(t_frame, text="<", command=self.previous_month), side=LEFT)
		self.month_l = pp.add(cLabel(t_frame, text=self.date.strftime("%B %Y"), borderwidth=1, relief='raised', height=2), side=LEFT, fill=X, expand=1)
		pp.add(cButton(t_frame, text=">", command=self.next_month), side=RIGHT)
		pp.pack()
		self.create_month_view(self.get_month(self.date), self.func)
		self.__buttons = {}
		context = {
		'Reset':self.reset,
		'Select Year':self.select_year,
		'Select Month':self.select_month,
		}
		self.menu = ContexMenu(self, context=context)
		self.month_l.bind("<Button-3>", self.menu._do_popup)
	def reset(self):
		self.specific_date(simpledate.now())
	def select_year(self):
		x = askinteger('Year Selection', 'Please input the year')
		self.specific_date(self.date.replace(year=x))
	def select_month(self):
		x = askstring('Month Selection', 'Please Enter the month').lower()
		if x in self.months:
			x = self.months.index(x)+1
		elif x in self.short_months:
			x = self.short_months.index(x)+1
		else:
			try:
				x = int(x)
			except:
				return
		self.specific_date(self.date.replace(month=int(x)))
	@staticmethod
	def pad(tx: str) -> str:
		return f'{tx if int(tx)>=10 else "0"+tx}'
	@cache
	def get_month(self, mdate: datetime) -> list:
		first = mdate.replace(day=1)
		last = mdate.replace(day=1,
								month=mdate.month+1 if mdate.month+1 < 13 else 1,
								year=mdate.year if mdate.month+1 < 13 else mdate.year+1
								) - relativedelta(days=1)
		weeks = list(range(1, last.day+1))
		for _ in range(first.weekday()): weeks.insert(0, 0) ##pad extra days at start of month
		month = [weeks[s:s+7] for s in range(0,len(weeks),7)] ##create the basic output from splitting weeks into segments
		for _ in range(7-len(month[-1])): month[-1].append(0) ##padd extra days at end of month
		for index1, w in enumerate(month):
			for index2, d in enumerate(w):
				month[index1][index2] = self.pad(str(d)) ##makes sure all numbers are strings of 2 digits.
		return month
	@classmethod
	def date(self) -> datetime:
		return self.date
	def set_date(self, d: datetime) -> datetime:
		self.date = d
		return self.date
	def specific_date(self, mdate:datetime):
		self.set_date(mdate)
		self.month_l.configure(text=self.date.strftime("%B %Y"))
		self.create_month_view(self.get_month(self.date), self.func)
	def next_month(self):
		self.set_date(
			self.date.replace(
				day=1,
				month=self.date.month+1 if self.date.month+1 < 13 else 1,
				year=self.date.year if self.date.month+1 < 13 else self.date.year+1,
				hour=0
				)
		)
		self.month_l.configure(text=self.date.strftime("%B %Y"))
		self.create_month_view(self.get_month(self.date), self.func)
	def previous_month(self):
		self.set_date(
			self.date.replace(
				day=1,
				month=self.date.month-1 if self.date.month > 1 else 12,
				year=self.date.year if self.date.month > 1 else self.date.year-1,
			)
		)
		self.month_l.configure(text=self.date.strftime("%B %Y"))
		self.create_month_view(self.get_month(self.date), self.func)
	def create_month_view(self, dates: list, func:Callable[[Event, str], None]):
		if len(dates) < 6:
			dates.append(['00']*7)
		dates = [item for sublist in dates for item in sublist]
		for child in self.c_frame.winfo_children():
			child.grid_forget()
			child.destroy()
		row = 1
		self.__buttons = {}
		
		gp = GridProcess()
		for index, day in enumerate(self.short_days):
			gp.add(cLabel(self.c_frame, text=day, width=5, height=2, borderwidth=1, relief='ridge'), row=0, column=index)
		for index, mdate in enumerate(dates):
			if index != 0 and index%7 == 0:
				row +=1
			self.__buttons[mdate] = gp.add(cButton(self.c_frame, 
												text=mdate if mdate != '00' else '',
												state='disabled' if mdate == '00' else 'normal',
												cursor='' if mdate == '00' else 'hand2',
												width=4,
												command=lambda e=Event(), d=mdate: func(e, d)
												), row=row, column=index%7)
		del self.__buttons['00']
		gp.grid()
	def __ignore(self, event, day):
		pass
class TimePicker(cFrame, widgetBase_override):
	def __init__(self, master, **kwargs):
		pp = PackProcess()
		self._acl = None
		self._atx = None
		self.split = "am"
		self.master = master
		self.tformat = kwargs.pop('format', 24)
		self.min_interval = kwargs.pop('interval', 5)
		tp_bg = kwargs.pop('tp_bg', '#010101')
		self.width = self.height = self.radious = rd = kwargs.pop('radious', 100)*2

		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		super(TimePicker, self).__init__(master, **kwargs)

		self.hours, self.minutes = StringVar(), StringVar()
		self.hours.set('00')
		self.minutes.set('00')
		holder_frame= pp.add(cFrame(self, bg="green"),side=TOP)
		def pad(item):return f"0{item}" if len(item) == 1 else item
		self.hourE = pp.add(cSpinbox(holder_frame, textvariable=self.hours, width=3, values=[pad(str(x)) for x in range(24)], wrap=0), side=LEFT)
		self._centre = pp.add(cLabel(holder_frame, text=":"), side=LEFT)
		self.minutesE = pp.add(cSpinbox(holder_frame, textvariable=self.minutes, width=3, values=[pad(str(x)) for x in range(60)], wrap=1), side=LEFT)

		#holder_frame.pack(side=TOP)
		##setup focus bindings
		self.hourE.bind("<FocusIn>", self.popup)
		self.hourE.bind("<FocusOut>", self.__focus_loss)
		self.minutesE.bind("<FocusIn>", self.popup)
		self.minutesE.bind("<FocusOut>", self.__focus_loss)

		
		self.radious /= 4
		self.radious -=1 ##fixes clipping
		assert self.tformat in [12, 24], "Time Format must be '12' or '24'"
		pp.pack()
		
		
		self.sub_can = cCanvas(self.get_root(), bg=tp_bg, width=self.width+5, height=self.height+5, highlightbackground="#010101", highlightthickness=0)
		self.sub_can.bind("<FocusIn>", self.popup)
		hwnd = self.sub_can.winfo_id()
		colorkey = win32api.RGB(1,1,1) #full black in COLORREF structure
		wnd_exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
		new_exstyle = wnd_exstyle | win32con.WS_EX_LAYERED
		win32gui.SetWindowLong(hwnd,win32con.GWL_EXSTYLE,new_exstyle)
		win32gui.SetLayeredWindowAttributes(hwnd, colorkey,255,win32con.LWA_COLORKEY)

		self.active_line = None
		self._main = self.create_center_circle(self.width/2, self.height/2, self.radious*2, fill="#DDDDDD", outline="#000", width=0)
		self.sub_can.tag_bind(self._main, "<Button-1>", self.popup)
		self.circle_numbers(self.width/2, self.height/2, self.radious*2-15, 10, [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'Helvetica 11 bold', "Hours")
		self.circle_numbers(self.width/2, self.height/2, self.radious+5,  10, list(range(0, 60, self.min_interval)), 'Helvetica 11 bold', "Minutes")
		self.am_pm_switch()
		self.center = self.create_center_circle(self.width/2, self.height/2, 5, fill="#DDDDDD", width=0)
		#self.update()
		#self.close(Event())

		if layout.method is not None:
			layout.inline(self)
	def __focus_loss(self, event):
		if self.get_root().focus_get() != self.sub_can:
			self.close(event)
		else:
			self.minutesE.focus_set()
	def _on_scroll(self, event, maxn=0):
		num = int(event.widget.get())
		event.widget.delete(0, END)
		if event.delta > 0 :
			if num >= maxn:
				event.widget.insert(0, '00')
			else:
				event.widget.insert(0, str(num+1).zfill(2))
		elif event.delta < 0:
			if num <= 0:
				event.widget.insert(0, str(maxn).zfill(2))
			else:
				event.widget.insert(0, str(num-1).zfill(2))	
	def am_pm_switch(self):
		ovall = 30
		ovalw = 40
		self.sub_can.create_oval(self.width/2-ovall, self.height/2+ovalw/4, self.width/2+ovall, self.height/2+ovalw, fill="#BBBBBB")
		sc, st = self.create_am()
		self.sub_can.tag_bind(sc, "<Button-1>", lambda e=Event(), a=sc, b=st:self._switcher(e, a, b))
		self.sub_can.tag_bind(st, "<Button-1>", lambda e=Event(), a=sc, b=st:self._switcher(e, a, b))
	def create_am(self):
		ovalr = 40
		am = self.create_center_circle(self.width/2-ovalr/1.75, self.height/2+ovalr/1.75, 12, fill='#0575DD', width=0)
		amtx = self.sub_can.create_text(self.width/2-ovalr/1.75, self.height/2+ovalr/1.75, font=('Helvetica 11 bold'), text="AM")
		self.split = "am"
		return am, amtx
	def create_pm(self):
		ovalr = 40
		pm = self.create_center_circle(self.width/2+ovalr/1.75, self.height/2+ovalr/1.75, 12, fill='#0575DD', width=0)
		pmtx = self.sub_can.create_text(self.width/2+ovalr/1.75, self.height/2+ovalr/1.75, font=('Helvetica 11 bold'), text="PM")
		self.split = "pm"
		return pm, pmtx
	def _switcher(self, event, sc, st):
		self.sub_can.delete(sc)
		self.sub_can.delete(st)
		if self.split == "am":
			sc, st = self.create_pm()
			self.sub_can.tag_bind(sc, "<Button-1>", lambda e=Event(), a=sc, b=st:self._switcher(e, a, b))
			self.sub_can.tag_bind(st, "<Button-1>", lambda e=Event(), a=sc, b=st:self._switcher(e, a, b))
		elif self.split == "pm":
			sc, st = self.create_am()
			self.sub_can.tag_bind(sc, "<Button-1>", lambda e=Event(), a=sc, b=st:self._switcher(e, a, b))
			self.sub_can.tag_bind(st, "<Button-1>", lambda e=Event(), a=sc, b=st:self._switcher(e, a, b))
	def create_center_circle(self, x, y, r, **kwargs):
		return self.sub_can.create_oval(x-r, y-r, x+r, y+r, **kwargs)
	def create_circle_arc(self, x, y, r, **kwargs):
		if "start" in kwargs and "end" in kwargs:
			kwargs["extent"] = kwargs["end"] - kwargs["start"]
			del kwargs["end"]
		return super().create_arc(x-r, y-r, x+r, y+r, **kwargs)
	def circle_numbers(self, x: int, y: int, r: int, cr:int, numbers: list, font: str, tp:str):
		_angle = 360/len(numbers)
		for i, n in enumerate(numbers):
			ax =  r * sin(pi * 2 * (360-_angle*i-180) / 360);
			ay = r * cos(pi * 2 * (360-_angle*i-180) / 360);
			tag = f'{tp}:{str(n)}'
			cl = self.create_center_circle(x+ax, y+ay, cr, fill="#DDDDDD", outline="#000", width=0, tag=tag)
			tx = self.sub_can.create_text(x+ax, y+ay, text=str(n).zfill(2), fill="black", font=(font), tag='tx'+tag )
			self.sub_can.tag_bind(f'tx{tp}:{str(n)}', '<Enter>', lambda e=Event(), cl=cl, tx=tx, c=(x+ax, y+ay), t=tag, s=True: self._hover(e, cl, tx, c, s, t))
			#self.sub_can.tag_bind(f'tx{tp}:{str(n)}', '<Leave>', lambda e=Event(), cl=cl, tx=tx, c=(x+ax, y+ay), t=tag, s=False: self._left(e, cl, tx, c, s, t))
			self.sub_can.tag_bind(f'{tp}:{str(n)}', '<Button-1>', lambda e=Event(), c=cl, s=tx, n=n, t=tp,: self._set_number(e, c, s, n, t))
			self.sub_can.tag_bind(f'tx{tp}:{str(n)}', '<Button-1>', lambda e=Event(), c=cl, s=tx, n=n, t=tp,: self._set_number(e, c, s, n, t))
	def _hover(self, event, cl, tx,  coords, state, tag):
		if self.active_line:
			self.sub_can.delete(self.active_line)
			self.sub_can.itemconfigure(self._acl, fill='#DDDDDD')
			self.sub_can.itemconfigure(self._atx, fill="black")
		self._acl = cl
		self._atx = tx
		self.sub_can.itemconfigure(cl, fill='#0797FF')
		self.sub_can.itemconfigure(tx, fill="white")

		self.sub_can.itemconfigure(self.center, fill='#0797FF')
		dx = (1 - 0.8) * self.width/2 + 0.8 * coords[0]
		dy = (1 - 0.8) * self.height/2 + 0.8 * coords[1]
		self.active_line = self.sub_can.create_line(self.width/2, self.height/2, dx, dy, fill="#0797FF", width=2, tag=None) ##create new line
		self.sub_can.tag_lower(self.active_line)
		self.sub_can.tag_lower(self._main)
	def _left(self, event, cl, tx, coords, state, tag):
		if self.active_line is None: ##if there is no line
			return
		self.sub_can.itemconfigure(cl, fill='#DDDDDD')
		self.sub_can.itemconfigure(tx, fill="black")
		self.sub_can.itemconfigure(self.center, fill='#DDDDDD')
		self.sub_can.delete(self.active_line)
		self.active_line = None
	def _set_number(self, event, cl, tx, number, tp):
		if tp == "Hours":
			if self.split == "pm":
				number = (number+12)%24
			self.hours.set(str(number).zfill(2))
			self.minutesE.focus()
		elif tp == "Minutes":
			self.minutes.set(str(number).zfill(2))
			self.close(event)
			self.master.focus()
	def get(self):
		return self.hours.get(), self.minutes.get()
	def popup(self, event):
		xpos = self._centre.winfo_rootx() - self.winfo_toplevel().winfo_rootx()
		ypos = self._centre.winfo_rooty() - self.winfo_toplevel().winfo_rooty() + self._centre.winfo_height()
		width = self._centre.winfo_width()/2
		self.sub_can.place(x=xpos-(self.width/2)+width, y=ypos)
	def close(self, event):
		self.sub_can.place_forget()

class ContexMenu(cMenu, widgetBase):
	_widgetBase__widget_type = rtktypes.noget
	@time_it
	def __init__(self, master, **kwargs):
		context = kwargs.pop('context', None) # get context builder or None
		if not isinstance(context, dict):
			raise MenuContexError 
		super(ContexMenu, self).__init__(master, tearoff=0)
		print(type(self))
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
							self.sub_menus[sub_name[1:]] = cMenu(self.sub_menus[old_name] if old_name in self.sub_menus else self, tearoff=0)
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