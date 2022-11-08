from objects import cEntry, cOptionMenu
from utils import master
import re


class ValidatingEntry(cEntry, master): ##used for MaxLengthEntry
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
class MaxLengthEntry(ValidatingEntry, master): ##entry with a max length flag
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

class reEntry(cEntry, master):
	def __init__(self, master, **kwargs):
		super(reEntry, self).__init__(master)
		self.stvar = StringVar()
		self.regex = ""
		kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		if 'text' in kw_wid.keys():
			self.stvar.set(kw_wid['text'])
			del kw_wid['text']
		if 're' in kw_wid.keys():
			self.regex = kw_wid['re']
			del kw_wid['re']
		else:
			self.regex = '.*'
		kw_wid['textvariable'] = self.stvar
		
		self.configure(kw_wid)
		self.bg = self.cget('background')
		self.fg = self.cget('foreground')
		if len(kw_pak) != 0:
			self.pack(kw_pak)
	def insert(self, pos, end, text=""):
		super().insert(pos, end, text)
		self._isvalid()
	def get(self):
		return super().get(), self._isvalid()
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

class reOptionMenu(cOptionMenu):
	def __init__(self, master, **kwargs):
		super(reOptionMenu, self).__init__(master, **kwargs)
		self.bg = self.cget('background')
		self.fg = self.cget('foreground')
		self.var.trace('w', self._isvalid)

	def _isvalid(self, a=None, b=None, c=None, e=None):
		if super().get() in [str(x) for x in self.options]:
			self.configure(bg=self.bg, fg=self.fg)
			return True
		else:
			self.configure(bg="red", fg="white")
			return False
	def get(self):
		return self.get(), self._isvalid()