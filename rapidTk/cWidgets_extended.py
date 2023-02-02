from tkinter import StringVar, IntVar, Event, INSERT, END, Misc, Toplevel
from tkinter import TOP, LEFT, RIGHT, BOTTOM, CENTER, X, Y, BOTH, SOLID
from tkinter import N, E, S, W, NW, NE, SE, SW, NSEW
from tkinter import Scrollbar, VERTICAL, HORIZONTAL 
from tkinter.simpledialog import askstring, askinteger



from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps
import re
from itertools import count
from datetime import datetime, date
from collections.abc import Callable
from dateutil.relativedelta import relativedelta
from math import sin, cos, pi

from .flags import __ttk_enabled__, __window_manager__
from .__main__ import PackProcess, GridProcess
from .cWidgets import cEntry, cButton, cFrame, cLabel, cCanvas, cTreeview, cCheckbutton, cScrolledText, cMenu, cSpinbox, cOptionMenu
from .rTkErrors import *
from .rTkUtils import coord, widgetBase, simpledate, cache
from .rTkManagers import _WindowManager
from .rTkTheme import _ThemeManager

try:
	import tkcalendar
	from .rTkCalendar.rTkCalendar import DateEntry, cDateEntry, reDateEntry
except:
	raise DateEntryNotFoundException
	class DateEntry:
		def __init__(self, master, **kwargs):
			raise DateEntryNotFoundException
	class cDateEntry:
		def __init__(self, master, **kwargs):
			raise DateEntryNotFoundException
	class reDateEntry:
		def __init__(self, master, **kwargs):
			raise DateEntryNotFoundException




from functools import wraps
def memoize(func):
	cache = {}

	@wraps(func)
	def wrapper(*args, **kwargs):
		key = str(args) + str(kwargs)
		if key not in cache:
			cache[key] = func(*args, **kwargs)
		return cache[key]
	return wrapper
def pack_opts(**kwargs):
	pak = ["side", "expand", "fill"]
	if __ttk_enabled__:
		style = ['bg', 'height', 'borderwidth', 'fg', 'padx', 'pady', 'relief', 'selectcolor', 'anchor']
	else:
		style = []
	kw_wid = {}
	kw_pak = {}
	kw_style = {}
	for k, v in kwargs.items():
		if k in pak:
			kw_pak[k] = v
		elif k in style:
			kw_style[k] = v
		else:
			kw_wid[k] = v
	return kw_wid, kw_pak, kw_style

class autoEntry(cEntry, widgetBase):
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)	
		self.bt = None
		self.aw = None

		##custom kwargs
		self.options =  kwargs.pop('auto', [])
		self.len = kwargs.pop('len', 3)
		assertValue(f'{self.len} >= 1', "len must be greater than 1")
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

		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		cEntry.__init__(*(self, master), **kwargs)
		self.aw = cCanvas(self.winfo_toplevel(), bg="white", borderwidth=2, relief="raised")
		self.bind('<Button-2>', self._full)
		self.bind('<F1>', self._full)
		if self.autoshow:
			self.bind('<Button-1>', self._full)
			self.bind('<FocusIn>', self._full)
		self.bind('<FocusOut>', self._close_overlay)
		self.winfo_toplevel().bind_all('<Button-1>', self._close_overlay)
		self.sv.trace("w", lambda name, index, mode, e=Event(): self._autocomplete(e))
		if len(kw_pak) != 0:
			self.pack(kw_pak)

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
		xpos = self.winfo_rootx() - self.winfo_toplevel().winfo_rootx()
		ypos = self.winfo_rooty() - self.winfo_toplevel().winfo_rooty() + self.winfo_height()
		self._overlay(self.options, coord(xpos,ypos))
	def _overlay(self, options, pos):
		if self.aw.winfo_ismapped():
			self._close_overlay()	
		self.aw.configure(width=self.winfo_width(), height=100)
		self.aw.pack_propagate(False)
		self.aw.place(x=pos.x, y=pos.y)
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
		super().destroy()
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
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		self.scroll_v = None
		self.scroll_h = None
		self.h = kwargs.pop('h', 0)
		self.v = kwargs.pop('v', 0)
		
		cFrame.__init__(*(self, master), **kw_wid)
		
		self.sCanvas = cCanvas(self, side=TOP, fill=BOTH, expand=1)
		self.sFrame = cFrame(self.sCanvas, side=LEFT, fill=BOTH, expand=1)
		self.cw = self.sCanvas.create_window((0, 0), window=self.sFrame, anchor=NW)
		if self.h in [1, "1", True]:
			self.scroll_h = Scrollbar(master, orient=VERTICAL, command=self.sCanvas.yview)
			self.sCanvas.configure(yscrollcommand=self.scroll_h.set)
			self.scroll_h.pack(side=RIGHT, fill=Y)
		if self.v in [1, "1", True]:
			self.scroll_v = Scrollbar(master, orient=HORIZONTAL, command=self.sCanvas.xview)
			self.sCanvas.config(xscrollcommand=self.scroll_v.set)
			self.scroll_v.pack(side=BOTTOM, fill=X)
		self.sFrame.bind("<Configure>", self._update_scrollregion)
		self.sCanvas.bind('<Configure>', self._FrameWidth)
		
		if len(kw_pak) != 0:
			self.pack(kw_pak)
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
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		self.motion = False

		if 'width' not in kw_wid:
			kw_wid['width'] = 400
		if 'height' not in kw_wid:
			kw_wid['height'] = 400
		if 'bg' not in kw_wid:
			self.bg="#FFFFFF"
		else:
			self.bg = kw_wid['bg']
		if 'fg' not in kw_wid:
			self.fg="#000000"
		else:
			self.fg = kw_wid['fg']
			del kw_wid['fg']
		self.width = kw_wid['width']
		self.height = kw_wid['height']
		if 'title' in kw_wid:
			self.title = True
			self.title_text = kw_wid['title']
			del kw_wid['title']
		else:
			self.title = False
		kw_wid['borderwidth'] = 1
		kw_wid['relief'] = "groove"
		cCanvas.__init__(*(self, master), **kw_wid)
		self.wm = self.get_root().wm
		self.root = self.winfo_toplevel()
		self.pid = self.root.uid.new()
		self.posx=0
		self.posy=0
		self.binds = {}
		self.rootbind = None
		if self.wm:
			self.wm.add_pid(self.pid, self)
		self._create()
	def _create(self):
		self.pack_propagate(False)
		self.place(x=self.root.winfo_width()/2-(self.width/2), y=(self.root.winfo_height()/2)-(self.height/4))
		self.top = cFrame(self, borderwidth=1, relief="raised", side=TOP, fill=X)
		self.body= cFrame(self, borderwidth=2, relief="ridge", side=TOP, fill=BOTH, expand=1)
		if self.title:
			move = cLabel(self.top, text=self.title_text, fg=self.fg, justify=CENTER, font=("Helvetica", 10), cursor="fleur", side=LEFT, fill=X, expand=1)
		else:
			move = cLabel(self.top, text="", justify=CENTER, font=("Helvetica", 10), cursor="fleur", side=LEFT, fill=X, expand=1)
		self.close = cButton(self.top, text="X", relief="raised", borderwidth=1, fg=self.fg, side=RIGHT, command=self._close)
		self.minimize = cButton(self.top, text="🗕", relief="raised", borderwidth=1, fg=self.fg, side=RIGHT, command=self._minimize)
		popout = cButton(self.top, text="⇱", relief="raised", borderwidth=1, fg=self.fg, side=RIGHT, command=self._popout)
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
	@memoize
	def _calc_move(self, rx, rrx, w, ry, rry):
		x=(rx-rrx-w/2)
		y=ry-rry-10
		return x, y
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
	def _popout(self): ##pop out to a new toplevel window
		pass
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
class Tooltip:
	def __init__(self, widget,*,bg='#FFFFEA',fg='#000000',pad=(5, 3, 5, 3),text='widget info',waittime=400,wraplength=250):
		self.waittime = waittime
		self.wraplength = wraplength
		self.widget = widget
		self.text = text
		self.widget.bind("<Enter>", self.onEnter)
		self.widget.bind("<Leave>", self.onLeave)
		self.widget.bind("<ButtonPress>", self.onLeave)
		self.bg = bg
		self.fg = fg 
		self.pad = pad
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
		self.id = self.widget.after(self.waittime, self.show)
	def unschedule(self):
		id_ = self.id
		self.id = None
		if id_:
			self.widget.after_cancel(id_)
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
		widget = self.widget
		self.tw = Toplevel(widget)
		self.tw.wm_overrideredirect(True)
		win = cFrame(self.tw,background=self.bg,borderwidth=0)
		label = cLabel(win,text=self.text,justify=LEFT,background=self.bg, foreground=self.fg, relief=SOLID,borderwidth=0,wraplength=self.wraplength)
		label.grid(padx=(pad[0], pad[2]),pady=(pad[1], pad[3]),sticky=NSEW)
		win.grid()
		x, y = tip_pos_calculator(widget, label)
		self.tw.wm_geometry("+%d+%d" % (x, y))
	def hide(self):
		tw = self.tw
		if tw:
			tw.destroy()
		self.tw = None
		
class Calendar(cFrame):
	def __init__(self, master, **kwargs):
		self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		self.short_days = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
		self.months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
		self.short_months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
		self.master = master
		self.date = kwargs.pop('date', simpledate.now())
		self.func = kwargs.pop('func', self.__ignore)
		super(Calendar, self).__init__(self.master)
		self.configure(**kwargs)
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
		self.menu = cMenu(self, context=context)
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
		
class TimePicker(cCanvas, widgetBase):
	def __init__(self, master, **kwargs):
		pp = PackProcess()
		self.split = "am"
		self.master = master
		self.tformat = kwargs.pop('format', 24)
		self.hours, self.minutes = StringVar(), StringVar()
		self.hours.set('00')
		self.minutes.set('00')
		holder_frame= pp.add(cFrame(master),side=TOP)
		self.hourE = pp.add(cSpinbox(holder_frame, textvariable = self.hours, width=3, values=tuple(list(range(24)))),side=LEFT)
		pp.add(cLabel(holder_frame, text=":"), side=LEFT)
		self.minutesE = pp.add(cSpinbox(holder_frame, textvariable=self.minutes, width=3, values=tuple(list(range(60)))),side=LEFT)
		self.minutesE.bind("<MouseWheel>", lambda e=Event(), m=59: self._on_scroll(e, maxn=m))
		self.hourE.bind("<MouseWheel>", lambda e=Event(), m=23: self._on_scroll(e, maxn=m))
		holder_frame.pack(side=TOP)
		##setup focus bindings
		self.hourE.bind("<FocusIn>", self.popup)
		self.hourE.bind("<FocusOut>", self.close)
		self.minutesE.bind("<FocusIn>", self.popup)
		self.minutesE.bind("<FocusOut>", self.close)

		self.width, self.height, self.radious = kwargs['width'], kwargs['height'], rd = (kwargs.pop('radious', 100)*2, )*3
		self.radious /= 4
		self.radious -=1 ##fixes clipping
		assert self.tformat in [12, 24], "Time Format must be '12' or '24'"

		super(TimePicker, self).__init__(master, **kwargs)
		self.active_line = None
		self.create_center_circle(self.width/2, self.height/2, self.radious*2, fill="#DDDDDD", outline="#000", width=0)
		self.circle_numbers(self.width/2, self.height/2, self.radious*2-15, 10, [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'Helvetica 11 bold', "Hours")
		self.circle_numbers(self.width/2, self.height/2, self.radious+5,  10, [0, 15, 30, 45], 'Helvetica 11 bold', "Minutes")
		
		self.am_pm_switch()


		self.center = self.create_center_circle(self.width/2, self.height/2, 5, fill="#DDDDDD", width=0)
		pp.pack()

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
		self.create_oval(self.width/2-ovall, self.height/2+ovalw/4, self.width/2+ovall, self.height/2+ovalw, fill="#BBBBBB")
		sc, st = self.create_am()
		self.tag_bind(sc, "<Button-1>", lambda e=Event(), a=sc, b=st:self._switcher(e, a, b))
		self.tag_bind(st, "<Button-1>", lambda e=Event(), a=sc, b=st:self._switcher(e, a, b))
	def create_am(self):
		ovalr = 40
		am = self.create_center_circle(self.width/2-ovalr/1.75, self.height/2+ovalr/1.75, 20, fill='#0575DD', width=0)
		amtx = self.create_text(self.width/2-ovalr/1.75, self.height/2+ovalr/1.75, font=('Helvetica 11 bold'), text="AM")
		self.split = "am"
		return am, amtx

	def create_pm(self):
		ovalr = 40
		pm = self.create_center_circle(self.width/2+ovalr/1.75, self.height/2+ovalr/1.75, 20, fill='#0575DD', width=0)
		pmtx = self.create_text(self.width/2+ovalr/1.75, self.height/2+ovalr/1.75, font=('Helvetica 11 bold'), text="PM")
		self.split = "pm"
		return pm, pmtx

	def _switcher(self, event, sc, st):
		self.delete(sc)
		self.delete(st)
		if self.split == "am":
			sc, st = self.create_pm()
			self.tag_bind(sc, "<Button-1>", lambda e=Event(), a=sc, b=st:self._switcher(e, a, b))
			self.tag_bind(st, "<Button-1>", lambda e=Event(), a=sc, b=st:self._switcher(e, a, b))
		elif self.split == "pm":
			sc, st = self.create_am()
			self.tag_bind(sc, "<Button-1>", lambda e=Event(), a=sc, b=st:self._switcher(e, a, b))
			self.tag_bind(st, "<Button-1>", lambda e=Event(), a=sc, b=st:self._switcher(e, a, b))


	def create_center_circle(self, x, y, r, **kwargs):
		return super().create_oval(x-r, y-r, x+r, y+r, **kwargs)
	
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
			tx = self.create_text(x+ax, y+ay, text=str(n).zfill(2), fill="black", font=(font), tag='tx'+tag )
			self.tag_bind(f'tx{tp}:{str(n)}', '<Enter>', lambda e=Event(), cl=cl, tx=tx, c=(x+ax, y+ay), t=tag, s=True: self._hover(e, cl, tx, c, s, t))
			self.tag_bind(f'tx{tp}:{str(n)}', '<Leave>', lambda e=Event(), cl=cl, tx=tx, c=(x+ax, y+ay), t=tag, s=False: self._left(e, cl, tx, c, s, t))
			self.tag_bind(f'{tp}:{str(n)}', '<Button-1>', lambda e=Event(), c=cl, s=tx, n=n, t=tp,: self._set_number(e, c, s, n, t))
			self.tag_bind(f'tx{tp}:{str(n)}', '<Button-1>', lambda e=Event(), c=cl, s=tx, n=n, t=tp,: self._set_number(e, c, s, n, t))

	def _hover(self, event, cl, tx,  coords, state, tag):
		if self.active_line:
			return
		self.itemconfigure(cl, fill='#0797FF')
		self.itemconfigure(tx, fill="white")
		self.itemconfigure(self.center, fill='#0797FF')
		dx = (1 - 0.8) * self.width/2 + 0.8 * coords[0]
		dy = (1 - 0.8) * self.height/2 + 0.8 * coords[1]
		self.active_line = self.create_line(self.width/2, self.height/2, dx, dy, fill="#0797FF", width=2, tag=None) ##create new line
	def _left(self, event, cl, tx, coords, state, tag):
		if self.active_line is None: ##if there is no line
			return
		self.itemconfigure(cl, fill='#DDDDDD')
		self.itemconfigure(tx, fill="black")
		self.itemconfigure(self.center, fill='#DDDDDD')
		self.delete(self.active_line)
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
		self.pack(side=TOP)
	def close(self, event):
		self.pack_forget()