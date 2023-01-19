from .cWidgets import cEntry, cOptionMenu, cCombobox, cScrolledText
from .cWidgets_extended import autoEntry
from .rTkUtils import widgetBase
from .flags import __ttk_enabled__

from tkinter import StringVar
import re
##TODO: Add documentation for all of this

class ValidatingEntry(cEntry, widgetBase): ##used for MaxLengthEntry
	def __init__(self, master, value="", **kw):
		#apply(Entry.__init__, (self, master), kw)
		cEntry.__init__(*(self, master), **kw)
		self.__value = value
		self.__variable = StringVar()
		self.__variable.set(value)
		self.__variable.trace("w", self.__callback)
		self.config(textvariable=self.__variable)
	def __callback(self, *dummy):
		value = self.__variable.get()
		newvalue = self.validate(value)
		if newvalue is None:
			self.__variable.set(self.__value)
		elif newvalue != value:
			self.__value = newvalue
			self.__variable.set(newvalue)
		else:
			self.__value = value
	def validate(self, value):
		# override: return value, new value, or None if invalid
		return value
class MaxLengthEntry(ValidatingEntry, widgetBase): ##entry with a max length flag ##TODO: convert this to re-wiget
	def __init__(self, master, value="", maxlength=None, valtype=None, **kw):
		self.maxlength = maxlength
		self.valtype = valtype
		#apply(ValidatingEntry.__init__, (self, master), kw)
		ValidatingEntry.__init__(*(self, master), **kw)
	def validate(self, value):
		if self.maxlength is None or len(value) <= self.maxlength:
			if self.valtype != None:
				if self.valtype == "int":
					try:
						x=int(value)
						return value
					except:
						return ""
				elif self.valtype == "int/hour":
					try:
						x=int(value)
						if x < 24:
							return value
						else:
							return ""
					except:
						return ""
				elif self.valtype == "int/minute":
					try:
						x=int(value)
						if x < 60:
							return value
						else:
							return ""
					except:
						return ""
				elif self.valtype == "int/currency":
					try:
						#x = float(value)
						if len(value.split(".")) == 2:
							if len(value.split(".")[1]) > 2:
								return value[:-1]
							else:
								return value
						elif len(value.split(".")) > 2:
							return ""
						else:
							return value
					except:
						return ""
				elif self.valtype == "str":
					try:
						x=int(value)
						return value
					except:
						return ""
				else:
					return ""
				
			else:
				return None
		return None # new value too long

##TODO: conform all this to a standard set of methods.
class reEntry(cEntry, widgetBase):
	def __init__(self, master, value="", **kwargs):
		self.regex = kwargs.pop('re', '.*')
		kwargs['textvariable'], self.var = (kwargs.get('textvariable', StringVar()),)*2
		super(reEntry, self).__init__(master, **kwargs)
		self.bg = self.cget('background')
		self.fg = self.cget('foreground')
	def __isvalid(self):
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
		self.__isvalid()
	#@override
	def get(self):
		return super().get(), self.__isvalid()
	
from .cWidgets import cEntry, cButton, cFrame, cLabel, cCanvas, cTreeview, cCheckbutton, cScrolledText, cMenu, cSpinbox, cOptionMenu

class reOptionMenu(cOptionMenu, widgetBase):
	def __init__(self, master, **kwargs):
		super(reOptionMenu, self).__init__(master, **kwargs)
		self.bg = self.cget('background')
		self.fg = self.cget('foreground')
		self.var.trace('w', self.__isvalid)
	def __isvalid(self, a=None, b=None, c=None, e=None):
		if super().get() in [str(x) for x in self.options]:
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
	def __isvalid(self):
		if self.sv.get() in self.options:
			self.configure(bg=self.bg, fg=self.fg)
			return True
		else:
			self.configure(bg="red", fg="white")
			return False
	#@override
	def get(self):
		return self.sv.get(), self.isvalid()


##TODO: complete __isvalid method
class reScrolledText(cScrolledText, widgetBase):
	def __init__(self, master, **kwargs):
		self.regex = kwargs.pop('re', '.*')
	def __isvalid(self):
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
