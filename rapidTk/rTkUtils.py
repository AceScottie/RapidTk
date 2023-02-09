import sys
from uuid import uuid4
from threading import Timer
if sys.platform == 'win32':
	from win32clipboard import OpenClipboard, EmptyClipboard, SetClipboardText, GetClipboardData, CloseClipboard
	from win32con import CF_TEXT, CF_UNICODETEXT
from functools import wraps, singledispatchmethod
from datetime import datetime
from time import perf_counter
from .rTkErrors import *
import logging

def time_it(func):
	def wrapper(*args, **kwargs):
		start = perf_counter()
		fn = func
		rs = fn(*args, **kwargs)
		t = perf_counter()-start
		logging.getLogger('rapidTk').rtkverbose(f'Timer for <{fn.__qualname__}.{fn.__name__}> finished in {t:0.9f}')
		return rs
	return wrapper

class _UniqueIdentifiers(list):
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

class clipboard(object):
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

class SingletonMeta(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]


class widgetBase:
	@time_it
	def __init__(self, master, **kwargs):
		self.master = master
	@time_it
	def get_root(self):
		return self.master.get_root()
	@time_it
	def get_master(self):
		return self.master
	@time_it
	def get_self(self):
		return self
	@time_it
	def get(self, index=None, end=None) -> str:
		ctype = str(type(self))[:-2].split(".")[-1]
		if ctype in ["cLabel", "cButton"]:
			if index in ['', None] and end in ['', None]:
				return self.cget("text")
			else:
				return self.__getter(self.cget('text'), index, end)
		elif ctype in ["cEntry", "cScrolledText", "reEntry", "MaxLengthEntry", "ValidatingEntry"]:
			if index in ['', None] and end in ['', None]:
				return self.var.get()
			else:
				return self.__getter(self.var.get(), index, end)
		elif ctype in ["cCheckbutton"]:
			return self.var.get()
		elif ctype in ["cTreeview"]:
			return "This requires cusom get() method"
		else:
			raise Exception(f'{type(self)} : {ctype} has no get() method')
	@time_it
	def set(self, index=0, text=""):
		ctype = str(type(self))[:-2].split(".")[-1]
		if ctype in ["cLabel", "cButton"]:
			if index in ['', None, 0]:
				self.configure(text=text)
			else:
				o_text = self.__getter(self.cget('text'), 0, index) or ''
				self.configure(text=o_text+text)
			self.update()
		elif ctype in ["cEntry", "cScrolledText", "reEntry", "MaxLengthEntry", "ValidatingEntry"]:
			if index in ['', None, 0]:
				return self.var.set(text)
			else:
				o_text = self.__getter(self.var.get(), 0, index)
				self.var.set(o_text+text)
		#elif ctype in ["cCheckbutton"]:
		#	return self.var.get()
		#elif ctype in ["cTreeview"]:
		#	return "This requires cusom get() method"
		else:
			raise Exception(f'{type(self)} : {ctype} has no set() method')
	@time_it
	def __getter(self, text, index, end) -> str:
		if end in ['end', '', None]:
			end = None
		index = 0 if not index else index
		return text[int(index):int(end) if end else None]


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
		self.valid = True
		self.__global_options = ["in", "anchor", "ipady", "ipadx", "padx", "pady"]
		self.__pack_add = ["anchor", "ipadx", "ipady","padx", "pady", "in"]
		self.__grid_add = ["ipadx", "ipady", "padx", "pady", "in"]
		self.__place_add = ["anchor", "in"]
		self.method_opts = {}
		if self.kwargs.get('method', None) is not None:
			self.method = kwargs.pop('method')
		else:
			self.method = self.__detect_method(**self.kwargs)
			if self.method is not None:
				valid_args = self.filter(**self.kwargs)
				self.valid = self.__validate(**valid_args)
	def __detect_method(self, **kwargs):
		method = None
		for k, v in kwargs.items():
			if k not in self.__global_options:
				method = self.__detect_layout(k)
				if method != None:
					return method
	def __validate(self, **kwargs):
		for k, v in kwargs.items():
			if k not in self.__global_options:
				v = self.__validate_method(k)
				if not v:
					self.method = False
					raise ValueError(f"{k} keyword exists in multiple managers")
					return v
	def __validate_method(self, k):
		methods = ['pack', 'place', 'grid']
		methods.remove(self.method)
		notin = self.__layout_keys[methods[0]] + self.__layout_keys[methods[1]]
		kws_all = self.__layout_keys['pack'] + notin
		if k in kws_all+self.__global_options:
			return k in self.__layout_keys[self.method] and k not in notin
		else:
			return True
	def __detect_layout(self, k):
		mth = None
		mth= 'pack' if k in self.__layout_keys['pack'] and k not in self.__layout_keys['grid']+self.__layout_keys['place'] else None
		if mth is not None:
			return mth
		mth = 'grid' if k in self.__layout_keys['grid'] and k not in self.__layout_keys['pack']+self.__layout_keys['place']  else None
		if mth is not None:
			return mth
		mth = 'place' if k in self.__layout_keys['place'] and k not in self.__layout_keys['grid']+self.__layout_keys['grid']  else None
		if mth is not None:
			return mth
	@property
	def __layout_keys(self):
		return {
		'pack':["after","before","expand","fill","padx","pady","side"],
		'grid':["column","columnspan","ipadx","ipady","padx","pady","row","rowspan","sticky"],
		'place':["bordermode","height","relheight","relwidth","relx","rely","width","x","y"]
		}
	@property
	def __all(self):
		return list(set(self.__layout_keys['pack']+self.__layout_keys['grid']+self.__layout_keys['place']))
	def __pack(self, widget, **kwargs):
		widget.pack(**kwargs)
	def __grid(self, widget, **kwargs):
		widget.grid(**kwargs)
	def __place(self, widget, **kwargs):
		widget.place(**kwargs)
	def filter(self, **kwargs):
		non_opts = {}
		for key, value in self.kwargs.items():
			if key in self.__all:
				self.method_opts[key] = value
			else:
				non_opts[key] = value
		return non_opts
	def inline(self, widget):
		#logging.getLogger('rapidTk').rtkverbose(f'adding inline widget {widget=}')
		self.methods[self.method](widget, **self.method_opts)

class RepeatedTimer(object):
	def __init__(self, interval, function, *args, **kwargs):
		self._timer		= None
		self.interval	= interval
		self.function	= function
		self.args		= args
		self.kwargs		= kwargs
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

	
