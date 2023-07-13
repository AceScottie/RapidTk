import logging
from .cWidgets import cEntry, cLabel, cScrolledText, cOptionMenu, cCombobox
from .cWidgets_extended import autoEntry
from .rTkUtils import widgetBase
import rapidTk.types as rtktypes

from tkinter import StringVar
import re
##TODO: Add documentation for all of this

class vEntry(cEntry, widgetBase):
	def __init__(self, master, **kwargs):
		super(vEntry, self).__init__(master, **kwargs)
		logging.getLogger('rapidTk').rtkdebug(f"created vEntry {self} with args {kwargs}")
		self._buffer = kwargs.pop('value', "")
		self.var.trace("w", self.__callback)
	def __callback(self, *args):
		v = self.var.get()
		v2 = self.validate(v)
		if v2:
			self.var.set(v2)
		else:
			self.var.set(self._buffer)
	def validate(self, v):
		return v
class typedEntry(vEntry, widgetBase):
	def __init__(self, master, **kwargs):
		self.maxlength = kwargs.pop('max', None)
		self.vtype = kwargs.pop('type', None)
		
		super(typedEntry, self).__init__(master, **kwargs)
		logging.getLogger('rapidTk').rtkdebug(f"created typedEntry {self} with args {kwargs}")
	def __cast_int(v):
		try:
			x=int(v)
			return True
		except:
			return False
	def validate(self, v):
		_con = True
		if self.maxlength is not None and len(v) > self.maxlength:
			_con = False
		match self.vtype:
			case "int":
				if not isinstance(v, int):
					_con = False
			case "int/12":
				if not isinstance(v, int) and not 1 <= v <= 12:
					_con = False
			case "int/24":
				if not isinstance(v, int) and not 1 <= v <= 24:
					_con = False
			case "int/60":
				if not isinstance(v, int) and not 1 <= v <= 60:
					_con = False
			case "float":
				if not isinstance(v, float):
					_con = False
			case "str":
				pass

		if _con:
			return v
		return ""

class MaxLengthEntry(typedEntry, widgetBase): ##entry with a max length flag ##TODO: convert this to re-wiget
	def __init__(self, master, **kwargs):
		kwargs['max'] = kwargs.pop('maxlength', None)
		kwargs['type'] = kwargs.pop('valtype', None)
		super(typedEntry, self).__init__(master, **kwargs)


##TODO: conform all this to a standard set of methods.
class reEntry(cEntry, widgetBase):
	def __init__(self, master, value="", **kwargs):
		self.regex = kwargs.pop('re', '.*')
		kwargs['textvariable'], self.var = (kwargs.get('textvariable', StringVar()),)*2
		super(reEntry, self).__init__(master, **kwargs)
		self.bg = self.cget('background')
		self.fg = self.cget('foreground')
	def _isvalid(self):
		try:
			match = re.match(self.regex, self.var.get())
			if not match:
				self.configure(bg="red", fg="white")
				return False
			else:
				self.configure(bg=self.bg, fg=self.fg)
				return True
		except:
			raise
			return False
	#@override
	def insert(self, pos, text=""):
		super().insert(pos, text)
		self._isvalid()
	#@override
	def get(self):
		return super().get(), self._isvalid()
	def set(self, text=""):
		super().set(text)
		self._isvalid()
	

class reLabel(cLabel, widgetBase):
	def __init__(self, master, **kwargs):
		self.re = kwargs.pop('re')
		super(reLabel, self).__init__(master, **kwargs)
	def _isvalid(self):
		try:
			match = re.match(self.regex, self.cget('text'))
			if not match:
				self.configure(bg="red", fg="white")
				return False
			else:
				self.configure(bg=self.bg, fg=self.fg)
				return True
		except:
			raise
			return False
	def get(self):
		return self.cget('text'), self._isvalid()

	def set(self, text:str):
		self.configure(text=text)
class reOptionMenu(cOptionMenu, widgetBase):
	_widgetBase__widget_type = rtktypes.strget
	def __init__(self, master, **kwargs):
		self.nv_options = kwargs.pop('non_valid', [])
		super(reOptionMenu, self).__init__(master, **kwargs)
		self.bg = self.cget('background')
		self.fg = self.cget('foreground')
		self.var.trace('w', self._isvalid)

	def _isvalid(self, a=None, b=None, c=None, e=None):
		print("reOptionMeny")
		print(self.var.get(), [str(x) for x in self.options], self.nv_options)
		if self.var.get() in [str(x) for x in self.options] and self.var.get() not in self.nv_options:
			self.configure(bg=self.bg, fg=self.fg)
			return True
		else:
			self.configure(bg="red", fg="white")
			return False
	#@override
	def get(self):
		return self.var.get(), self._isvalid()
class reCombobox(cCombobox, widgetBase):
	def __init__(self, master, **kwargs):
		super(reCombobox, self).__init__(master, **kwargs)
		self.style.configure('Fail.TCombobox', fieldbackground='red', background='red', foreground='white')
		self.var.trace('w', self._isvalid)

	def _isvalid(self, a=None, b=None, c=None, e=None):
		#self.get_master().focus_set()
		self.selection_clear()
		if self.var.get() in [str(x) for x in self.values]:
			self.configure(style=f'{str(self.__repr__())}.Main.TCombobox')
			return True
		else:
			self.configure(style=f'{str(self.__repr__())}.Fail.TCombobox')
			return False
	#@override
	def get(self):
		return super().get(), self._isvalid()
		
class reautoEntry(autoEntry, widgetBase):
	def _isvalid(self):
		if self.sv.get() in self.options or self.sv.get() == '':
			self.configure(bg=self.bg, fg=self.fg)
			return True
		else:
			self.configure(bg="red", fg="white")
			return False
	#@override
	def get(self):
		return self.sv.get(), self._isvalid()


##TODO: complete __isvalid method
class reScrolledText(cScrolledText, widgetBase):
	def __init__(self, master, **kwargs):
		self.regex = kwargs.pop('re', '.*')
	def _isvalid(self):
		try:
			match = re.match(self.regex, self.stvar.get())
			if not match:
				self.configure(bg="red", fg="white")
				return False
			else:
				self.configure(bg=self.bg, fg=self.fg)
				return True
		except:
			raise
			return False
	#@override
	def get(self):
		return self.var.get(), self.__isvalid()
