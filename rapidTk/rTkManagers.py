from tkinter import Event, TOP, LEFT, RIGHT, CENTER, BOTTOM, BOTH
from .rTkErrors import *
from .cWidgets import cCanvas
from .rTkUtils import SingletonMeta
from .flags import __scroll_manager__, __window_manager__, __popup_manager__, __tab_manager__

class _ScrollManager(object, metaclass=SingletonMeta):
	def __init__(self, root):
		__scroll_manager__ = True
		self.root = root
		self.collections = {}
		self.scrolls = {"0":None} #{id:scroll}
		self.triggers = {} #{id:trigger}
		self.default = "0"
		self.active_id = "0"
	def clear(self):
		try:
			self.scrolls[self.active_id].unbind("<MouseWheel>")
		except:
			pass
		for i in self.triggers:
			try:
				i.unbind('<Enter>')
				i.unbind('<Leave>')
			except:
				pass
		self.scrolls = {"0":None}
		self.triggers = {}
		self.default = "0"
		self.active_id = "0"
	def add_tab(self, tab):
		pass## add tab collection to collections
	def add_window(self, window):
		pass##add window/popup to collections
	def add_collection(self, scroll):
		pass## add item to collections based on current selected collection
	def switch(self, collection):
		pass##move between collections for when switching tab

	def add(self, scroll, trigger=None, default=None):
		uid = self.root.uid.new()
		if default:
			self.default = uid
		self.scrolls[uid] = scroll
		if trigger != None:
			self.triggers[uid] = trigger
		else:
			self.triggers[uid] = scroll
		self.triggers[uid].bind('<Enter>', lambda e=Event(), i=uid:self._entered(e, i))
		self.triggers[uid].bind('<Leave>', lambda e=Event(), i=uid:self._leave(e, i))
		return uid
	def _entered(self, event, uid):#
		if self.active_id != "0" and self.active_id in self.scrolls.keys():
			self.scrolls[self.active_id].unbind("<MouseWheel>")
		self.active_id = uid
		self.root.bind_all('<MouseWheel>', self._on_mousescroll)
	def _leave(self, event, uid):
		if uid in self.scrolls.keys():
			if uid == self.active_id:
				self.active_id = self.default
	def _unbind_all(self):
		pass ## remove all binds from all collections
	def _on_mousescroll(self, event):
		if self.active_id in self.scrolls.keys() and self.scrolls[self.active_id] is not None:
			self.scrolls[self.active_id].yview_scroll(int(-1 * (event.delta / 120)), "units")
			self.scrolls[self.active_id].update()
			self.root.update()
			self.root.update_idletasks()
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
		self.active_tab = None
	def new(self, holder):
		uid = self.root.uid.new()
		self.tabs[uid] = cCanvas(holder)
		return uid
	def switch(self, event=None, uid=None):
		self.root.sm.clear()
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

