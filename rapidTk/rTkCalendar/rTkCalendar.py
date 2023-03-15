from overrides import override
from tkcalendar import DateEntry
from tkinter import StringVar
import re
from datetime import datetime, date

from ..flags import __ttk_enabled__
from ..rTkTheme import _ThemeManager
from ..rTkUtils import widgetBase, _UniqueIdentifiers, inline_layout

class DateEntry(DateEntry, widgetBase):
	@override
	def _validate_date(self):
		"""Date entry validation: only dates in locale '%x' format are accepted."""
		try:
			date = self.parse_date(super().get())
			self._date = self._calendar.check_date_range(date)
			if self._date != date:
				self._set_text(self.format_date(self._date))
				return False
			else:
				return True
		except (ValueError, IndexError):
			self._set_text(self.format_date(self._date))
			return False
	@override
	def _set_text(self, txt):
		"""Insert text in the entry."""
		if 'readonly' in self.state():
			readonly = True
			self.state(('!readonly',))
		else:
			readonly = False
		super().delete(0, 'end')
		super().insert(0, txt)
		if readonly:
			self.state(('readonly',))
	@override
	def drop_down(self):
		"""Display or withdraw the drop-down calendar depending on its current state."""
		if self._calendar.winfo_ismapped():
			self._top_cal.withdraw()
		else:
			self._validate_date()
			date = self.parse_date(super().get())
			x = self.winfo_rootx()
			y = self.winfo_rooty() + self.winfo_height()
			if self.winfo_toplevel().attributes('-topmost'):
				self._top_cal.attributes('-topmost', True)
			else:
				self._top_cal.attributes('-topmost', False)
			self._top_cal.geometry('+%i+%i' % (x, y))
			self._top_cal.deiconify()
			self._calendar.focus_set()
			self._calendar.selection_set(date)
	@override
	def get_date(self):
		"""Return the content of the DateEntry as a datetime.date instance."""
		self._validate_date()
		return self.parse_date(super().get())

class cDateEntry(DateEntry, widgetBase):
	def __init__(self, master, **kwargs):
		#widgetBase.__init__(self, master)
		self._myid = _UniqueIdentifiers().new()
		kwargs['textvariable'] = self.var = kwargs.pop('textvariable', StringVar())
		kwargs['date_pattern'] = kwargs.pop('date_pattern', "dd/mm/yyyy")
		self.var.set(kwargs.pop('text', "01/01/1970"))
		self._mystyle_name = kwargs.pop('style', f'{self._myid}.DateEntry')
		self.bg = kwargs.pop('fieldbackground', None)
		self.fg = kwargs.pop('foreground', None)
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		super(cDateEntry, self).__init__(master, **widget_args)
		self.style = self.get_root().thm.style
		if self.bg is None: self.bg = self.style.lookup(self._mystyle_name, "fieldbackground")
		if self.bg is None: self.bg = self.style.lookup(self._mystyle_name, "foreground")
		if layout.method is not None:
			layout.inline(self)

	def detele(ind=0, end='end'):
		super().insert(0, '')
	def insert(self, ind=0, data=''):
		try:
			if isinstance(data, datetime) or isinstance(data, date):
				super().insert(ind, data.strftime("%d/%m/%Y"))
			else:
				super().insert(ind, data)
		except:
			super().insert(ind, data)
	#def __setattr__(self, at, val):
	#	if at in ["bg", "background"]:
	#		self.style.configure(self._mystyle_name,  fieldbackground=val)
	#	elif at in ["fg", "foreground"]:
	#		self.style.configure(self._mystyle_name,  foreground=val)
	#	else:
	#		super().__setattr__(at, val)

class reDateEntry(cDateEntry, widgetBase): ## TODO: move most of this code to cDateEntry for autoStyle and stuff
	def __init__(self, master, **kwargs):
		self.regex = kwargs.pop('re', '.*')
		self.min = kwargs.pop('min', '01/01,01')
		self.min = kwargs.pop('min', '31/12/5000')

		super(reDateEntry, self).__init__(master, **kwargs)
		self.style.configure(self._mystyle_name, fieldbackground=self.bg, foreground=self.fg)


	def insert(self, pos, date="01/01/1970"):
		super().insert(pos, date)
		self._isvalid()
	def get(self):
		return self.var.get(), self._isvalid()
	def _isvalid(self):
		try:
			if self.var.get() not in ['', None]:
				match = re.match(self.regex, self.var.get())
				if not match or self.parse_date(self.var.get()) > datetime.now().date():
					self.style.configure(self._mystyle_name, fieldbackground="red", foreground="white")
					return False
				else:
					self.style.configure(self._mystyle_name, fieldbackground=self.bg, foreground=self.fg)
					return True
			else:
				return False
		except:
			raise
			return False
