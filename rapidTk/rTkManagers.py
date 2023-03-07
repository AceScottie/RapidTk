import logging
from queue import Queue
from tkinter import Event, TOP, LEFT, RIGHT, CENTER, BOTTOM, BOTH
from .rTkErrors import *
from .rTkUtils import SingletonMeta
from .flags import __scroll_manager__, __window_manager__, __popup_manager__, __tab_manager__

class _ScrollManager(object, metaclass=SingletonMeta):
	def __init__(self, root):
		__scroll_manager__ = True
		self._current = None
		self.q = Queue()
		self.q_o = Queue() ## not yet implemented
	def __set_current(self, event, widget, override):
		if self._current is not None:
			self.q.put(self._current)
			#self.q_o.put(self._current.override?) #not yet implemented
		self._current = widget
		if override is None:
			self._current.bind_all('<MouseWheel>', self._on_mousescroll)
		else:
			self._current.bind_all('<MouseWheel>', override)
	def __unset_current(self, event, widget):
		self._current.unbind_all('<MouseWheel>')
		if not self.q.empty():
			self._current = self.q.get()
			self._current.bind_all('<MouseWheel>', self._on_mousescroll) ## can not use overriden scroll commands yet!
		else:
			self._current = None
	def _on_mousescroll(self, event):
		self._current.yview_scroll(int(-1 * (event.delta / 120)), "units")
		self._current.update()
	def add_widget(self, widget, override=None):
		widget.bind('<Enter>', lambda e=Event(), w=widget, o=override: self.__set_current(e, w, o))
		widget.bind('<Leave>', lambda e=Event(), w=widget: self.__unset_current(e, w))








class _WindowManager(object, metaclass=SingletonMeta):
	def __init__(self, root):
		__window_manager__ = True
		self.root = root
		self.pids = {}
		self.active_window = None
		self.inactive_windows = [None]*10
	def add_pid(self, pid, window):
		self.pids[pid] = {'widget':window, 'active':1}
	
	def _set_active(self, pid):
		self.pids[pid]['active'] = 0
		if pid in self.inactive_windows:
			idx = self.inactive_windows.index(pid)
			self.inactive_windows[idx] = None

	def _set_inactive(self, pid):
		self.pids[pid]['active'] = 0
		idx = self.inactive_windows.index(None)
		self.inactive_windows[idx] = pid

	def _set_main(self, pid):
		self.active_window = pid

	def _get_deactive_space(self):
		return self.inactive_windows.index(None)

	def remove(self, pid): # removes object from manager
		if pid in self.inactive_windows:
			idx = self.inactive_windows.index(pid)
			self.inactive_windows[idx] = None
		del self.pids[pid]

	def destroy(self):#delets objects and removes from manager
		pids = list(self.pids.keys())
		for pid in pids:
			self.pids[pid]['widget']._close()

class _PopupManager(object, metaclass=SingletonMeta):
	def __init__(self, root):
		__popup_manager__ = True
		self.root = root
	def simple_popup(self, text):
		pass #use ctype popup
	def overlay_popup(self, holder):
		pass # use movable window
	def _manage_overlay(self):
		pass #handel closing and opening overlays




class _TabManager(object, metaclass=SingletonMeta):
	def __init__(self, root):
		__tab_manager__ = True
		self.root = root
		self.tabs = {}
		self.names = {}
		self.active_tab = None
	def new(self, widget, **kwargs):
		uid = self.root.uid.new()
		self.tabs[uid] = widget
		if "name" in kwargs and kwargs['name'] not in self.names:
			self.names[kwargs['name']] = uid
		return uid
	def get_by_name(self, name):
		if name in self.names:
			return self.names[name]
		else:
			logging.getLogger('rapidTk').rtkwarning(f'{name} is not in the list of tabs')
			return None
	def switch(self, event=None, uid=None):
		if uid != None:
			if self.active_tab != None:
				self.tabs[self.active_tab].pack_forget()
			self.active_tab = uid
			self.tabs[self.active_tab].pack(side=TOP, fill=BOTH, expand=1)
	def tab(self, uid):
		if uid in self.tabs.keys():
			return self.tabs[uid]
		else:
			raise TabNotFoundError
	def name(self, tab):
		for n, t in self.names.items():
			if t == tab:
				return n
		logging.getLogger('rapidTk').rtkwarning(f'{tab} is not in the list of tabs')
		return None

