from tkinter import Tk
import tkinter.ttk as ttk
from .rTkErrors import *
from .rTkUtils import coord, _UniqueIdentifiers
from .rTkManagers import _ScrollManager, _WindowManager, _PopupManager, _TabManager
from .rTkTheme import _ThemeManager

import logging

from .rTkUtils import time_it
class rapidTk(Tk):
	@time_it
	def __init__(self, with_managers=True, with_ttk=False):
		self.afters = {}
		self.quitter = False
		self.origin = [coord(0, 0), coord(0, 0)]
		self._schedule_tasks = {}
		self._tasks = []
		self.uid = _UniqueIdentifiers()
		Tk.__init__(self)
		self.sm = _ScrollManager(self)	
		self.thm = _ThemeManager(self)
		self.thm.set_theme("clam")
		self.pop = _PopupManager(self)
		self.tm = _TabManager(self)
		self.wm = _WindowManager(self)
		self.after(1, self._schedule)
		self.bind('<F12>',self._fullscreen)
	@time_it
	def _schedule(self):
		if not self.quitter:
			for s in self._schedule_tasks.items():
				if not self.quitter:
					s['task']()
	@time_it
	def add_schedule_taks(self, tid, task):
		if tid not in self._schedule_tasks.keys(): 
			self._schedule_tasks.append({'id':tid, 'task':task})
			return tid
		else:
			raise TaskIdExistsError
	@time_it
	def del_schedule_taks(self, tid):
		if tid in self._schedule_tasks.keys(): 
			del self._schedule_tasks[tid]
		else:
			raise TaskIdNotExistsError
	@time_it
	def process_task(self, task):
		self.tasks.append(task)
	@time_it
	def _do_taks(self):
		for t in self._tasks:
			t()
	@time_it
	def taksid(self):
		return 123456789 ##change to random number generator
	@time_it
	def _fullscreen(self, event):
		if self.origin[0].vec2() == (0, 0) and self.origin[1].vec2() == (0, 0):
			self.fullscreen(True)
		else:
			self.fullscreen(False)
	@time_it
	def fullscreen(self, b):#
		if isinstance(b, bool):
			if b:
				self._set_full()
			else:
				self._set_restore()
		else:
			raise ValueError
	@time_it
	def _set_full(self):
		self.origin = [coord(self.winfo_width(), self.winfo_height()), coord(self.winfo_x(), self.winfo_y())]
		self.overrideredirect(True)
		self.geometry("%sx%s+0+0"%(self.winfo_screenwidth(), self.winfo_screenheight()))
	@time_it
	def _set_restore(self):
		self.overrideredirect(False)
		self.geometry("%sx%s+%s+%s"%(self.origin[0].x, self.origin[0].y, self.origin[1].x, self.origin[1].y))
		self.origin = [coord(0, 0),coord(0, 0)]
	@time_it
	def destroy(self):
		for af in self.afters.keys():
			self.after_cancel(af)
		self.quitter = True
		self.wm.destroy()
		for af in self.afters.keys():
			self.after_cancel(af)
		self.update()
		self.update_idletasks()
		super().destroy()
	@time_it
	def after(self, time, func):
		if not self.quitter:
			uid = self.uid.new()
			self.afters[uid] = super().after(time, func)
	@time_it
	def get_root(self):
		return self

class PackProcess:
	@time_it
	def __init__(self):
		self.widgets = []
	@time_it
	def add(self, widget, side=None, expand=0, fill=None):
		self.widgets.append({"widget":widget, "side":side, "expand":expand, "fill":fill})
		return widget
	@time_it
	def pack(self):
		for element in self.widgets:
			element['widget'].pack(side=element['side'], fill=element['fill'], expand=element['expand'])

