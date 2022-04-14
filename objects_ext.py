from tkinter import StringVar, IntVar, Event, INSERT, END 
from tkinter import TOP, LEFT, RIGHT, BOTTOM, CENTER, X, Y, BOTH
from tkinter import N, E, S, W, NW, NE, SE, SW
from tkinter import Scrollbar, VERTICAL, HORIZONTAL 


from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps
import re

from .rapidTk import PackProcess
from .objects import cEntry, cButton, cFrame, cLabel, cCanvas, cTreeview, cCheckbutton, cScrolledText, cDateEntry
from .errors import *
from .utils import coord
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
class autoEntry(cEntry):
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)	
		self.bt = None
		kw_wid, kw_pak = pack_opts(**kwargs)
		self.options = kw_wid['auto']
		if 'len' in kwargs:
			self.len = kwargs['len']
			del kwargs['len']
		else:
			self.len = 3
		if 'anchor' in kwargs:
			self.anchor = kwargs['anchor']
			del kwargs['anchor']
		else:
			self.anchor = "center"
		self.strict = False
		self.autoshow = False
		self.bg = '#AAFFAA'
		self.fg = '#000000'
		self.autobg = '#DDDDDD'
		self.autofg = '#000000'
		self.hovertext = '#BBBBBB'
		self.hovercolor = '#000000'
		if 'strict' in kwargs:
			if kwargs['strict'] in [1, '1', True]:
				self.strict = True
			del kwargs['strict']
		if 'autoshow' in kwargs:
			if kwargs['autoshow'] in [1, '1', True]:
				self.autoshow = True
			del kwargs['autoshow']
		del kwargs['auto']
		if 'bg' not in kw_wid.keys() and 'background' not in kw_wid.keys():
			kwargs['bg'] = self.bg
		else:
			self.bg = kwargs['bg']
		if 'fg' not in kw_wid.keys() and 'foreground' not in kw_wid.keys():
			kwargs['fg'] = self.fg
		else:
			self.fg = kwargs['fg']
		if 'hovertext' in kwargs:
			self.hovercolor = kwargs['hovertext']
			del kwargs['hovertext']
		if 'hovercolour' in kwargs:
			self.hovercolor = kwargs['hovercolour']
			del kwargs['hovercolour']
		if 'autobg' in kwargs:
			self.autobg = kwargs['autobg']
			del kwargs['autobg']
		if 'autofg' in kwargs:
			self.autofg = kwargs['autofg']
			del kwargs['autofg']
		self.sv = StringVar()
		kwargs['textvariable'] = self.sv
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
		intxt = self.get()
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
		self.bt = cTreeview(self.aw, width=self.winfo_width()-15, bg=self.autobg, fg=self.autofg, side=LEFT)
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
	def get(self):
		return self.sv.get()
	def __del__(self):
		self._close_overlay()
		super().destroy()
class iButton(cButton):
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak = pack_opts(**kwargs)
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
class scrollArea(cFrame):
	def __init__(self, master, **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak = pack_opts(**kwargs)
		self.h = 0
		self.v = 0
		self.scroll_v = None
		self.scroll_h = None
		if "h" in kw_wid.keys():
			self.h = kw_wid['h']
			del kw_wid['h']
		if "v" in kw_wid.keys():
			self.v = kw_wid['v']
			del kw_wid['v']
		cFrame.__init__(*(self, master), **kw_wid)
		self.sCanvas = cCanvas(self, side=TOP, fill=BOTH, expand=1)
		self.sFrame = cFrame(self.sCanvas)
		#self.vspacer = cCanvas(self.sFrame, width=1000, height=0, side=TOP)
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

class movableWindow(cCanvas):
	def __init__(self, master,  **kwargs):
		self.__dict__.update(kwargs)
		kw_wid, kw_pak = pack_opts(**kwargs)
		self.master = master
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
		self.root = self.winfo_toplevel()
	def create(self):
		self.pack_propagate(False)
		self.place(x=self.root.winfo_width()/2-(self.width/2), y=(self.root.winfo_height()/2)-(self.height/4))
		self.top = cFrame(self, borderwidth=1, relief="raised", side=TOP, fill=X)
		self.body= cFrame(self, borderwidth=2, relief="ridge", side=TOP, fill=BOTH, expand=1)
		if self.title:
			move = cLabel(self.top, text=self.title_text, fg=self.fg, justify=CENTER, font=("Helvetica", 10), cursor="fleur", side=LEFT, fill=X, expand=1)
		else:
			move = cLabel(self.top, text="", justify=CENTER, font=("Helvetica", 10), cursor="fleur", side=LEFT, fill=X, expand=1)
			#move = cFrame(self.top, cursor="fleur", fill=X, expand=1)
		close = cButton(self.top, text="X", relief="raised", borderwidth=1, fg=self.fg, side=RIGHT, command=self._close)
		move.bind("<B1-Motion>", self._move)
		move.bind("<ButtonRelease-1>", self._drop)
		self.root.bind("<Configure>", self._drop)
	def _move(self, event):
		if not self.motion:
			self.motion = True
			if(self.root.winfo_pointerx() != "??" and self.root.winfo_pointery() != "??"):
				self.place(x=(self.root.winfo_pointerx() - self.root.winfo_rootx()) - self.winfo_width()/2, y=self.root.winfo_pointery() - self.root.winfo_rooty()-10)
			self.update()
			self.motion = False
	def _drop(self, event):
		if self.winfo_x() + self.winfo_width() > self.root.winfo_width():
			self.place(x=self.root.winfo_width()-self.winfo_width())
		elif self.winfo_x() < 0:
			self.place(x=0)
		if self.winfo_y() + self.winfo_height() > self.root.winfo_height():
			self.place(y=self.root.winfo_height()-self.winfo_height())
		elif self.winfo_y() < 0:
			self.place(y=10)
	def _close(self):
		self.destroy()
class qForm:
	def __init__(self):
		self.questions = {}
	def create_questions(self, holder, objects, configuration):
		pp = PackProcess()
		for sec, obj in objects.items():
			section = pp.add(cFrame(holder, bg="blue"), side=TOP, fill=X)
			pp.add(cLabel(section, text=sec, anchor="center"), side=TOP, fill=X)
			for ob, opts in obj.items():
				f = pp.add(cFrame(section), side=TOP, fill=X)
				name  = opts['name']
				self.questions[name] = {"label":pp.add(cLabel(f, text=opts['label'], width=opts['textwidth'], anchor="e"), side=LEFT), "object":None, "validation":None, "bg":None, 'fg':None}
				insert = ""
				if "text" in opts:
					insert = opts['text']
					del opts['text']
				validation = None
				if "validation" in opts:
					self.questions[name]['validation'] = opts['validation']
					del opts['validation']
				del opts['label']
				del opts['name']
				del opts['textwidth']
				if ob[:-2] == "Entry":
					self.questions[name]["object"] = pp.add(cEntry(f, **opts), side=LEFT)
					try:
						self.questions[name]['object'].insert(INSERT, insert)
					except:
						print("%s Entry %s"%(name, insert))
				elif ob[:-2] == "autoEntry":
					self.questions[name]["object"] = pp.add(autoEntry(f, **opts), side=LEFT)
					try:
						self.questions[name]['object'].insert(INSERT, insert)
					except:
						print("%s autoEntry %s"%(name, insert))
				elif ob[:-2] == "Label":
					opts['text'] = insert
					self.questions[name]["object"] = pp.add(cLabel(f, **opts), side=LEFT)
				elif ob[:-2] == "DateEntry":
					self.questions[name]["object"] = pp.add(cDateEntry(f, **opts), side=LEFT)
					try:
						self.questions[name]['object'].insert(INSERT, insert)
					except:
						print("%s DateEntry %s"%(name, insert))
				elif ob[:-2] == "Checkbutton":
					self.questions[name]["object"] = pp.add(cCheckbutton(f, **opts), side=LEFT)
					try:
						self.questions[name]['object'].set(int(insert))
					except:
						print("%s Checkbutton %s"%(name, insert))
				elif ob[:-2] == "ScrollText":
					self.questions[name]["object"] = pp.add(cScrolledText(f, **opts), side=LEFT)
					try:
						self.questions[name]['object'].insert(INSERT, insert)
					except:
						print("%s ScrollText %s"%(name, insert))
		pp.pack()
	def results(self):
		results = {}
		for k, v in self.questions.items():
			try:
				results[k] = v['object'].get()
			except:
				print(k, v['object'])
				raise
		return results
	def validate(self):
		validation_valid = True
		for k, v in self.questions.items():
			value = v['object'].get()
			print(value)
			print(type(value))
			print(type(v['object']))
			if v['validation'] is not None and str(type(v['object'])) != "<class 'rTk.objects.autoEntry'>":
				print(k, v['validation'])
				pattern = re.compile(v['validation'], re.IGNORECASE)
				valid = pattern.match(str(value))
				if not valid:
					v['object'].configure(bg="red")
					validation_valid = False
				else:
					if v['object'].cget('background') == "red":
						if str(type(v['object'])) != "<class 'rTk.objects_ext.autoEntry'>":
							v['object'].configure(bg=v['object'].winfo_toplevel().option_get('background', '.'), fg=v['object'].winfo_toplevel().option_get('foreground', '.'))
						else:
							v['object'].configure(bg=v['object'].bg, fg=v['object'].fg)
					print(type(v['object']))
			elif str(type(v['object'])) == "<class 'rTk.objects_ext.autoEntry'>":
				print("testing autocomplete")
				print(value)
				print(v['object'].auto)
				if value not in v['object'].auto:
					v['object'].configure(bg="red")
					validation_valid = False
				else:
					v['object'].configure(bg=v['object'].bg, fg=v['object'].fg)
		return validation_valid
	def update(self, question, value):
		self.questions[question]['object'].set(value)