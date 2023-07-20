import sys, re
from uuid import uuid4
from threading import Timer
import platform
if platform.system() == 'Windows':
	from win32clipboard import OpenClipboard, EmptyClipboard, SetClipboardText, GetClipboardData, CloseClipboard
	from win32con import CF_TEXT, CF_UNICODETEXT
elif platform.system() == "Linux":
	pass

elif platform.system() == "macOS":
	import subprocess

from functools import wraps, singledispatchmethod
from datetime import datetime
from time import perf_counter
from rapidTk.rTkErrors import *
import rapidTk.types as rtktypes
import rapidTk.assets.constants as constants
import logging

def _text_split_index(index='1.0', text="", end='end'):
	#linestart > figure how to handle this?
	print(index, text, end)
	if end in ['end', 0, 'end-1c', None]:
		end = 0
	if index in [None, '1.0', 0]:
		index = 0
	line = int(float(index))
	column = int(float(index)*10)%10
	print(line, column, end)


class SingletonMeta(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]

def time_it(func):
	def wrapper(*args, **kwargs):
		start = perf_counter()
		fn = func
		rs = fn(*args, **kwargs)
		t = perf_counter()-start
		logging.getLogger('rapidTk').rtkverbose(f'Timer for <{fn.__qualname__}.{fn.__name__}> finished in {t:0.9f}')
		return rs
	return wrapper

class _UniqueIdentifiers(list, metaclass=SingletonMeta):
	def __init__(self):
		super().__init__(self)
	def __getslice__(self,i,j):
		return UniqueIdentifiers(super().__getslice__(self, i, j))
	def __add__(self, item):
		return UniqueIdentifiers(super().__add__(self,item))
	def __mul__(self,other):
		return UniqueIdentifiers(super().__mul__(self,other))
	def __getitem__(self, item):
		result = super().__getitem__(self, item)
		if type(item) is slice:
			return UniqueIdentifiers(result)
		else:
			return result
	def append(self, item):
		if item not in self:
			super().append(item)
		else:
			raise duiplicateIDError
	def new(self):
		uid = uuid4()
		while uid in self:
			uid = uuid4()
		self.append(uid)
		return uid

class coord(object):
	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z
	def vec2(self):
		return (self.x, self.y)
	def vec3(self):
		return (self.x, self.y, self.z)
	def translate(self, x=0, y=0, z=0):
		self.x += x
		self.y += y
		self.z += z
		return self.vec3()
	def set(self, x=None, y=None, z=None):
		if x != None:
			self.x = x
		if y != None:
			self.y = y
		if z != None:
			self.z = z
		return self.vec3()

class clipboard_WIN(object):
	def __new__(self):
		if sys.platform != "win32":
			raise PlatformError
		return object.__new__(self)
	@staticmethod
	def copy(text):
		try:
			OpenClipboard() 
			EmptyClipboard()
			SetClipboardText(text, CF_UNICODETEXT) # set clipboard data
			CloseClipboard()
			return True
		except:
			return False
	@staticmethod
	def paste():
		try:
			OpenClipboard()
			data = GetClipboardData(CF_UNICODETEXT)
			CloseClipboard()
			return data
		except:
			return ""
class clipboard_LINUX(object):
	def __new__(self):
		if sys.platform != "win32":
			raise PlatformError
		return object.__new__(self)
	@staticmethod
	def copy(text):
		try:
			OpenClipboard() 
			EmptyClipboard()
			SetClipboardText(text, CF_UNICODETEXT) # set clipboard data
			CloseClipboard()
			return True
		except:
			return False
	@staticmethod
	def paste():
		try:
			OpenClipboard()
			data = GetClipboardData(CF_UNICODETEXT)
			CloseClipboard()
			return data
		except:
			return ""
class clipboard_mac(object):
	def __new__(self):
		if sys.platform != "win32":
			raise PlatformError
		return object.__new__(self)
	@staticmethod
	def copy(text):
		try:
			subprocess.run("pbcopy", text=True, input=text)
			return True
		except:
			return False
	@staticmethod
	def paste():
		try:
			OpenClipboard()
			data = subprocess.run("pbpaste")
			CloseClipboard()
			return data
		except:
			return ""

class widgetBase:
	@time_it
	def __init__(self, master, *args, **kwargs):
		super(widgetBase, self).__init__()
		self.master = master
		self.uid = _UniqueIdentifiers().new()
		if kwargs.pop('rtkwb_override', 0): ##overrides standard selection methods.
			self.bind('<Button-1>', self.__focus_shift)
			self.bind('<Button-2>', self.__focus_shift)
			self.bind('<Escape>', self.__focus_shift)
	@time_it
	def __focus_shift(self, event):
		print(f"wtype = {str(type(event.widget))}")
		if event.keysym == "Escape":
			self.get_root().focus_set()
		elif event.widget != self.get_root().focus_get():
			event.widget.focus_set()
	@time_it
	def get_root(self):
		return self.nametowidget('.')
		#return self.master.get_root()
	@time_it
	def get_master(self):
		return self.master
	@time_it
	def get_self(self):
		return self
	@time_it
	def rel(self, w):
		"""
		returns the path relative to inputted widget
		"""
		return str(self)[len(str(w)):]
	@time_it
	def get(self, index=None, end=None, **kwargs) -> str:
		"""
		Gets the text of a widget, either using the StringVar or cget('text') where applicable.
		"""
		match self.__widget_type:
			case rtktypes.noget:
				raise OptionNotPermitted(f'get() is not availble for {self}')
			case rtktypes.disget:
				if index in ['', None] and end in ['', None]:
					return self.cget("text")
				else:
					if not isinstance(index, int): index = 0 # set index to 0 if index is not an int
					if not isinstance(end, int): end = 0 ##set end to 0 if end is not an int
					value = self.cget("text")
					return value[index:end if end != 0 else len(value)+1] ##retuns the substring of value, if end is 0 then end is set to length of string.
			case rtktypes.singleget:
				if index is not None or end is not None: ##if index or end has been set.
					if not isinstance(index, int): index = 0 # set index to 0 if index is not an int
					if not isinstance(end, int): end = 0 ##set end to 0 if end is not an int
					value = self.var.get()
					return value[index:end if end != 0 else len(value)+1] ##retuns the substring of value, if end is 0 then end is set to length of string.
				else:
					return self.var.get()
			case rtktypes.multiget:
				if index is not None or end is not None: ##if index or end has been set.
					if index is None: index = '1.0' ##default index to start if None
					if end is None: end = 'end' ##defatult end to end if None
					pp_start = self.count('1.0', index)[0] # get the amout of characters between start and index
					pp_end = self.count(index, end)[0] ## get the amount of characters selected
					return self.var.get()[pp_start:self.count('1.0', end)[0]-pp_end] ## return value[start+index:end-amount]
				else:
					return self.var.get()#or return full StringVar result.
			case rtktypes.strget | rtktypes.intget | rtktypes.doubleget:
				if index is not None or end is not None:
					logging.getLogger('rapidTk').rtkwarning(f'{self} widget does not support index|end arguments.')
				return self.var.get()
			case rtktypes.treeget:
				return "This requires cusom get() method"
			case _:
				raise Exception(f'{type(self.__widget_type)} : {self} has no get() method')
	@time_it
	def set(self, index:int|str|float=None, text:str="", **kwargs):
		"""
		sets the text of a widget to the `text` value, replacing the current text starting at the `index` position
		"""
		if text == "" and index is not None: ##yet another dirty fix. TODO: find a way to take the first arg as text if only 1 arg was set.
			text = index
			index = None
		match self.__widget_type:
			case rtktypes.noget:
				raise OptionNotPermitted(f'set() is not availble for {self}')
			case rtktypes.disget:
				print("display get -> set")
			case rtktypes.singleget:
				if index is not None:
					try:
						if int(float(index)) > 0:
							original = self.get()
							logging.getLogger('rapidTk').rtklog(f'{self} is being set with {original[0:int(float(index))]+text} and index {index}')
							self.var.set(original[0:int(float(index))]+text)
						else:
							logging.getLogger('rapidTk').rtklog(f'{self} is being set with {text} and index {index}')
							self.var.set(text)
					except:
						if isinstance(index, str):
							try:
								original = self.get()
								try:
									index = self.index(index)
								except:
									if index == 'end':
										index = len(original)
									else:
										raise OptionNotPermitted("")
								original = self.get()
								logging.getLogger('rapidTk').rtklog(f'{self} is being set with {original[:index]+text} and index {index}')
								self.var.set(original[:index]+text)
							except:
								logging.getLogger('rapidTk').rtkerror(f"Index {index} cannot be used with {self} or is not supported")
						else:
							logging.getLogger('rapidTk').rtkerror(f"Unknown index {index}")
				else:
					logging.getLogger('rapidTk').rtklog(f'{self} is being set with {text} and index {index}')
					self.var.set(text)
			case rtktypes.multiget: ## TODO: WIP
				if index is not None:
					original = self.get()
					try: 
						index = self.count('1.0', self.index(index))[0]
					except:
						try:
							index = self.count('1.0', index)
						except:
							index = 0
					logging.getLogger('rapidTk').rtklog(f'{self} is being set with {original[0:index]+text} and index {index}')
					self.var.set(original[0:index]+text)
				else:
					logging.getLogger('rapidTk').rtklog(f'{self} is being set with {text} and index {index}')
					self.var.set(f"{text}")
			case rtktypes.strget | rtktypes.intget | rtktypes.doubleget:
				if index is not None:
					logging.getLogger('rapidTk').rtkwarning(f'{self} widget does not support index|end arguments.')
				self.var.set(text)
	def insert(self, index=0, text="", **kwargs):
		"""
		sets the text of a widget to the `text` value, replacing the current text starting at the `index` position
		"""
		match self.__widget_type:
			case rtktypes.noget:
				raise OptionNotPermitted(f'insert() is not availble for {self}')
			case rtktypes.singleget:
				try:
					float(index)
				except:
					return
				if int(float(index)) > 0:
					original = self.get()
					self.var.set(original[0:int(float(index))]+text+original[int(float(index)):])
				else:
					self.var.set(text)
			case rtktypes.multiget:## TODO: WIP
				if index not in [0, '1.0']:
					original = self.get()
					try: 
						index = self.count('1.0', float(index))[0]
					except:
						index = self.count('1.0', index)
					self.var.set(original[0:index]+text+original[index:])
				else:
					self.var.set(f"{text}")

	def delete(self, index=None, end=None, **kwargs):
		"""
		deletes the text between `index` position and `end` position if not None, otherwise deletes the 
		"""
		ctype = self.__widget_type
		match self.__widget_type:
			case rtktypes.noget:
				raise OptionNotPermitted(f'insert() is not availble for {self}')
			case rtktypes.singleget:
				try:
					float(index)
				except:
					return
				if int(float(index)) > 0:
					original = self.get()
					self.var.set(original[0:int(float(index))]+original[int(float(end)):])
				else:
					self.var.set("")
			case rtktypes.multiget:## TODO: WIP
				if index is not None or end is not None:
					original = self.get()
					try: 
						if index is None: index = '1.0' ##default index to start if None
						if end is None: end = 'end' ##defatult end to end if None
						index = self.count('1.0', index)[0] # get the amout of characters between start and index
						end = self.count(end, 'end')[0] ## get the amount of characters selected 
					except:
						index = self.count('1.0', index)
						end = len(original)
					self.var.set(original[0:index]+original[len(original)-end:])
				else:
					self.var.set(f"{text}")
			case rtktypes.strget | rtktypes.intget | rtktypes.doubleget:
				self.set()
	@time_it
	def clear(self, event=None):
		match self.__widget_type:
			case rtktypes.noget:
				raise OptionNotPermitted(f'insert() is not availble for {self}')
			case _:
				try:
					self.var.set('')
				except:
					self.var.set(0)

class widgetBase_override(widgetBase):
	"""
	overrides the mouse bindings to prevent issues of focus loss when focus loss is expected.
	"""
	def __init__(self, master, *args, **kwargs):
		self.master = master
		self.uid = _UniqueIdentifiers().new()
		kwargs['rtkwb_override'] = 1
		super(widgetBase_override, self).__init__(master)


def cache(func):
	cached = {}
	@wraps(func)
	def wrapper(*args, **kwargs):
		key = str(args) + str(kwargs)
		if key not in cached:
			cached[key] = func(*args, **kwargs)
			logging.getLogger('rapidTk').rtkverbose(f'Adding to cache {args}, {kwargs}')
		else:
			logging.getLogger('rapidTk').rtkverbose(f'Using cache {args}, {kwargs}')
		return cached[key]
	return wrapper
class simpledate(datetime):
	def simplify(self, **kwargs):
		[kwargs.pop(key, None) for key in ['hour', 'minute', 'second', 'microsecond']]
		return super().replace(**kwargs, hour=0, minute=0, second=0, microsecond=0)
	def replace(self, **kwargs):
		return self.simplify(**kwargs)      
	@classmethod
	def now(cls, tz=None):
		return super().now(tz=tz).simplify()

##use init: inline_layout(**kwargs)
##use get: inline_layout.filter() -> kwargs that are not part of layout method.
##use set: inline_layout.inline(widget) -> lay out the widget (pack, grid or place)
class inline_layout: ##TODO: fix this unholy mess and make it actuall readable!!!
	def __init__(self, **kwargs):
		self.kwargs = kwargs
		self.method = None
		self.methods = {'pack':self.__pack, 'place':self.__place, 'grid':self.__grid}
		self.valid_args = {}
		self.method_opts = {}
		self.method = self.kwargs.pop('method', None)
		if self.method is None:
			self.method = self.__detect_method(**self.kwargs)
			#if self.method is not None:
			#   valid_args = self.filter(**self.kwargs)
	def __detect_method(self, **kwargs):
		method = None
		for k, v in kwargs.items():
			if k not in constants._global_layout:
				method = self.__detect_layout(k)
				if method != None:
					return method
	def __detect_layout(self, k):
		mth = None
		if k in constants._pack_add and k not in constants._global_layout:
			return 'pack'
		elif k in constants._grid_add and k not in constants._global_layout:
			return 'grid'
		elif k in constants._place_add and k not in constants._global_layout:
			return 'place'
		else:
			return None
	@property
	def __all(self):
		return list(set(constants._pack_add+constants._grid_add+constants._place_add))
	def __pack(self, widget, **kwargs):
		widget.pack(**kwargs)
	def __grid(self, widget, **kwargs):
		widget.grid(**kwargs)
	def __place(self, widget, **kwargs):
		widget.place(**kwargs)
	def filter(self, **kwargs):
		for key, value in self.kwargs.items():
			if key in self.__all+constants._global_layout:
				if key == "ysize":## yet another dirty fix. at this point i should just re-wright the layout methods.
					self.method_opts['height'] = value
				elif key == "xsize":
					self.method_opts['width'] = value
				else:
					self.method_opts[key] = value
			else:
				self.valid_args[key] = value
		return self.valid_args
	def inline(self, widget):
		logging.getLogger('rapidTk').rtkverbose(f'adding inline widget {widget=}')
		self.methods[self.method](widget, **self.method_opts)

class RepeatedTimer(object):
	def __init__(self, interval, function, *args, **kwargs):
		self._timer     = None
		self.interval   = interval
		self.function   = function
		self.args       = args
		self.kwargs     = kwargs
		self.is_running = False
		self.start()

	def _run(self):
		self.is_running = False
		self.start()
		self.function(*self.args, **self.kwargs)

	def start(self):
		if not self.is_running:
			self._timer = Timer(self.interval, self._run)
			self._timer.start()
			self.is_running = True

	def stop(self):
		self._timer.cancel()
		self.is_running = False

	

class illigalUnicode:
	def __init__(self):
		_illegal_unichrs = [(0x00, 0x08), (0x0B, 0x0C), (0x0E, 0x1F), 
							(0x7F, 0x84), (0x86, 0x9F), 
							(0xFDD0, 0xFDDF), (0xFFFE, 0xFFFF)] 
		if sys.maxunicode >= 0x10000:  # not narrow build 
			_illegal_unichrs.extend([(0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF), 
									 (0x3FFFE, 0x3FFFF), (0x4FFFE, 0x4FFFF), 
									 (0x5FFFE, 0x5FFFF), (0x6FFFE, 0x6FFFF), 
									 (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF), 
									 (0x9FFFE, 0x9FFFF), (0xAFFFE, 0xAFFFF), 
									 (0xBFFFE, 0xBFFFF), (0xCFFFE, 0xCFFFF), 
									 (0xDFFFE, 0xDFFFF), (0xEFFFE, 0xEFFFF), 
									 (0xFFFFE, 0xFFFFF), (0x10FFFE, 0x10FFFF)]) 

		_illegal_ranges = [fr"{chr(low)}-{chr(high)}"for (low, high) in _illegal_unichrs]
		self._illegal_xml_chars_RE = re.compile(f"[{''.join(_illegal_ranges)}]")
	def test(self, char):
		return self._illegal_xml_chars_RE.sub('', char)
class cloneTree(dict):
	def __init__(self):
		self.__relpath = ""
		super(cloneTree, self).__init__()
	@property
	def relpath(self):return self.__relpath
	@relpath.setter
	def relpath(self, path):self.__relpath = path
	def get_rel(self, base, widget):return widget[len(str(base)):]
	def __setitem__(self, at, val):super().__setitem__(at[len(str(self.__relpath)):], val)
	def __getitem__(self, at):return super().__getitem__(at)
	def clear(self):
		self = {}


class iList(dict):
	def __init__(self, lst:list=[]):
		super(iList, self).__init__()
		self._i = 0
		for l in lst:
			self.append(l)
			self._i +=1
	def _inc(self):
		self._i += 1
	def append(self, item):
		self[self._i] = item
		self._inc()

	def __setitem__(self, index, item):
		#self.set(index, item)
		super().__setitem__(index, item)

	def insert(self, index, item):
		#super().insert(index, str(item))
		if index in self:
			raise Exception(f"index {index} is already in use. Please use the set() method to overwrite")
		self[index] = item
	def set(self, index, item):
		self[index] = item

	#def __getitem__(self, index):
	#	return self[index]

	def get(self):
		l = max(list(self.keys()))+1
		tmp = [None]*l
		for k, v in self.items():
			tmp[k] = v
		return tmp

	def index(self, item):
		for k, v in self:
			if v == item:
				return k

	def extend(self, other):
		raise Exception("extend(other) Not implemented with iList")

	def __contains__(self, item):
		print("in", item)
		
	def __iter__(self):
		rows = self.get()
		for r in rows:
			yield r

if __name__ == "__main__":
	l = iList()
	for i in range(6):
		l.append(["tmp", "tmp2"])
	print("test")
	for x in l:
		print(x)
	