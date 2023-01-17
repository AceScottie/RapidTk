import sys
from uuid import uuid4
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
	def __init__(self, master):
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

def ui(method="pack"):
	return {
	'pack':["after","anchor","before","expand","fill","in","ipadx","ipady","padx","pady","side"],
	'grid':["column","columnspan","in","ipadx","ipady","padx","pady","row","rowspan","sticky"],
	'place':["anchor","bordermode","height","in","relheight","relwidth","relx","rely","width","x","y"]
	}[method]
	
