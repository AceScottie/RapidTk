from tkinter import Tk
import tkinter.ttk as ttk
from .errors import *
from .utils import coord, _UniqueIdentifiers
from .manage import _ScrollManager, _WindowManager, _PopupManager, _TabManager
from .theme import _ThemeManager
from .flags import __ttk_enabled__
class rapidTk(Tk):
	def __init__(self, with_managers=True, with_ttk=False):
		#if with_ttk:
		#	flags.__ttk_enabled__ = True
		self.origin = [coord(0, 0), coord(0, 0)]
		self._schedule_tasks = {}
		self._tasks = []
		self.uid = _UniqueIdentifiers()
		Tk.__init__(self)
		if with_managers:
			self.sm = _ScrollManager(self)	
			self.thm = _ThemeManager(self)
			self.thm.set_style("breeze")
			self.pop = _PopupManager(self)
			self.tm = _TabManager(self)
			self.wm = _WindowManager(self)
		else:
			self.sm = None
			self.thm = None
			self.pop = None
			self.tm = None
			self.wm = None
		self.after(1, self._schedule)
		self.bind('<F12>',self._fullscreen)
	def _schedule(self):
		for s in self._schedule_tasks.items():
			s['task']()
	def add_schedule_taks(self, tid, task):
		if tid not in self._schedule_tasks.keys(): 
			self._schedule_tasks.append({'id':tid, 'task':task})
			return tid
		else:
			raise TaskIdExistsError
	def del_schedule_taks(self, tid):
		if tid in self._schedule_tasks.keys(): 
			del self._schedule_tasks[tid]
		else:
			raise TaskIdNotExistsError
	def process_task(self, task):
		self.tasks.append(task)
	def _do_taks(self):
		for t in self._tasks:
			t()
	def taksid(self):
		return 123456789 ##change to random number generator
	def _fullscreen(self, event):
		if self.origin[0].vec2() == (0, 0) and self.origin[1].vec2() == (0, 0):
			self.fullscreen(True)
		else:
			self.fullscreen(False)
	def fullscreen(self, b):#
		if isinstance(b, bool):
			if b:
				self._set_full()
			else:
				self._set_restore()
		else:
			raise ValueError
	def _set_full(self):
		self.origin = [coord(self.winfo_width(), self.winfo_height()), coord(self.winfo_x(), self.winfo_y())]
		self.overrideredirect(True)
		self.geometry("%sx%s+0+0"%(self.winfo_screenwidth(), self.winfo_screenheight()))
	def _set_restore(self):
		self.overrideredirect(False)
		self.geometry("%sx%s+%s+%s"%(self.origin[0].x, self.origin[0].y, self.origin[1].x, self.origin[1].y))
		self.origin = [coord(0, 0),coord(0, 0)]
	def get_root(self):
		print('this is root')
		return self

class PackProcess:
	def __init__(self):
		self.widgets = []
	def add(self, widget, side=None, expand=0, fill=None):
		self.widgets.append({"widget":widget, "side":side, "expand":expand, "fill":fill})
		return widget
	def pack(self):
		for element in self.widgets:
			element['widget'].pack(side=element['side'], fill=element['fill'], expand=element['expand'])

