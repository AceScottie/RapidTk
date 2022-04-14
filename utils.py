import sys
from .errors import *
from uuid import uuid4
if sys.platform == 'win32':
	from win32clipboard import OpenClipboard, EmptyClipboard, SetClipboardText, GetClipboardData, CloseClipboard
	from win32con import CF_TEXT, CF_UNICODETEXT

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