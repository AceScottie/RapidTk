import logging
from queue import Queue
from tkinter import Event, TOP, LEFT, RIGHT, CENTER, BOTTOM, BOTH
from .rTkErrors import *
from .rTkUtils import SingletonMeta

class _ScrollManager(object, metaclass=SingletonMeta):
	def __init__(self, root):
		self._current = None ##the current scrollable widget
		self._current_o = None ##the current overriden scroll command
		self.q = Queue() ##widget queue
		self.q_o = Queue() ##override queue
	def __set_current(self, event, widget, override):
		if self._current is not None: ##if there is a current widget which has not triggered <Leave>
			self.q.put(self._current) ##put the widget in the queue
			self.q_o.put(self._current_o) ##put its override in the queue
		self._current = widget ## set the new widget as current
		self._current_o = override ##set its override to the current override
		if self._current_o is None: ##if not overriden
			self._current.bind_all('<MouseWheel>', self._on_mousescroll)
		else: ## run bind to the overridden command
			self._current.bind_all('<MouseWheel>', override)
	def __unset_current(self, event, widget):
		try: ##this sometimes fails, needs to be fixed at some point.
			self._current.unbind_all('<MouseWheel>')
		except:
			pass
		if not self.q.empty(): ##if there are widgets in the queue that have not been left with <Leave> event.
			self._current = self.q.get() ##get the widget from the queue
			override = self.q_o.get() ##with its override (function or None)
			if override is None: ##if not overridden run the standard mousescroll binding
				self._current.bind_all('<MouseWheel>', self._on_mousescroll)
			else: ##bind the mouse scroll to the overriden function
				self._current.bind_all('<MouseWheel>', override)
		else: ##if the queue is empty then default everything
			self._current = None
			self._current_o = None
	def _on_mousescroll(self, event): ##default mousescroll command
		self._current.yview_scroll(int(-1 * (event.delta / 120)), "units")
		self._current.update()
	def add_widget(self, widget, override=None): ##adds the standard binding to scrollable widgets.
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
		self.tabs[widget.uid] = widget
		if "name" in kwargs and kwargs['name'] not in self.names:
			self.names[kwargs['name']] = widget.uid
		return widget.uid
	def get_by_name(self, name):
		if name in self.names:
			return self.names[name]
		else:
			logging.getLogger('rapidTk').rtkwarning(f'{name} is not in the list of tabs')
			return None
	def switch(self, event=None, uid=None):
		print(f"switching {uid=}")
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

