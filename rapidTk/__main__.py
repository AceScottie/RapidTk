import logging

from tkinter import Tk

from .rTkErrors import *
from .rTkUtils import coord, _UniqueIdentifiers
from .rTkManagers import _ScrollManager, _WindowManager, _PopupManager, _TabManager
from .rTkTheme import _ThemeManager



from .rTkUtils import time_it



class rapidTk(Tk):
	@time_it
	def __init__(self, with_managers=True, with_ttk=False, log_level=0):
		self.log = logging.getLogger('rapidTk')
		if isinstance(log_level, int) and log_level > 0:
			self.log.setLevel(log_level)
		elif not isinstance(log_level, int):
			raise Exception(f'log_level requires an interger value not type {type(log_level)}')
		
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

	@time_it
	def clear(self, widget=None):
		w=self
		if widget:
			w=widget
		for _c in w.winfo_children():
			_c.destroy()

	@time_it
	def center_root(self, width=300, height=300, min_height=600, min_width=1200):
		if width < min_width: width = min_width
		if height < min_height: height = min_height
		ws = self.winfo_screenwidth()
		hs = self.winfo_screenheight()
		posx, posy = int((ws/2) - (width/2)), int((hs/2) - (height/2))
		self.geometry(f"{width}x{height}+{posx}+{posy}")
		self.minsize(height=min_height, width=min_width)
		self.update()
		self.update_idletasks()
	@time_it
	def window_scale(self, percent:int) -> tuple[int, int]:
		return int((self.winfo_screenwidth()/100)*percent), int((self.winfo_screenheight()/100)*percent)
		

class __processor:
	@time_it
	def __init__(self, method="pack"):
		self.methods = {"pack":None, "place":None, "grid":None}
		self.method = method
		self.widgets = []
		self.pack = self.place = self.grid = self.process
	@time_it
	def add(self, widget, **kwargs):
		self.widgets.append({"widget":widget, "options":kwargs})
		return widget
	def process(self):
		m = self.methods[self.method]
		for element in self.widgets:
			print(element["options"])
			##Dirty fix
			if self.method == "pack":
				element['widget'].pack(**element["options"])
			elif self.method == "grid":
				element['widget'].grid(**element["options"])
			elif self.method == "place":
				element['widget'].place(**element["options"])

class PackProcess(__processor):
	def __init__(self):
		super().__init__(method="pack")
class GridProcess(__processor):
	def __init__(self):
		super().__init__(method="grid")
class PlaceProcess(__processor):
	def __init__(self):
		super().__init__(method="place")