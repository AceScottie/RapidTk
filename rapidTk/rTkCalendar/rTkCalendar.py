from overrides import override
from tkcalendar import DateEntry
from tkinter import StringVar
import re
from datetime import datetime, date

from ..flags import __ttk_enabled__
from ..rTkTheme import _ThemeManager
from ..rTkUtils import widgetBase, _UniqueIdentifiers

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
		self._myid = _UniqueIdentifiers().new()
		self.style = self.get_root().thm.style
		kwargs['textvariable'] = self.stvar = kwargs.pop('textvariable', StringVar())
		kwargs['date_pattern'] = kwargs.pop('date_pattern', "dd/mm/yyyy")
		self.stvar.set(kwargs.pop('text', "01/01/1970"))
		kwargs['style'] =  self._mystyle_name = kwargs.pop('style', f'{self._myid}.DateEntry')
		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		super(cDateEntry, self).__init__(master, **widget_args)
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
	def __setattr__(self, at, val):
		if at in ["bg", "background"]:
			self.style.configure(self._mystyle_name,  fieldbackground=val)
		elif at in ["fg", "foreground"]:
			self.style.configure(self._mystyle_name,  foreground=val)
		else:
			super().__setattr__(at, val)

class reDateEntry(cDateEntry, widgetBase): ## TODO: move most of this code to cDateEntry for autoStyle and stuff
	def __init__(self, master, **kwargs):
		self.regex = ""
		self.min = None
		self.max = None
		
		
		#kw_wid, kw_pak, kw_style = pack_opts(**kwargs)
		if 'fieldbackground' in kw_wid:
			self.style.configure(self._mystyle_name, fieldbackground=kw_wid['fieldbackground'])
			self.bg = kw_wid['fieldbackground']
			del kw_wid['fieldbackground']
		else:
			self.bg = self.style.lookup(self._mystyle_name, "fieldbackground")
		if 'foreground' in kw_wid:
			self.style.configure(self._mystyle_name, fieldbackground=kw_wid['foreground'])
			self.fg = kw_wid['foreground']
			del kw_wid['foreground']
		else:
			self.bg = self.style.lookup(self._mystyle_name, "foreground")
		if 'text' in kw_wid.keys():
			self.stvar.set(kw_wid['text'])
			del kw_wid['text']
		else:
			self.stvar.set('01/01/1970')
		if 're' in kw_wid.keys():
			self.regex = kw_wid['re']
			del kw_wid['re']
		else:
			self.regex = '.*'
		if 'min' in kw_wid.keys():
			self.min = kw_wid['min']
			del kw_wid['min']
		if 'max' in kw_wid.keys():
			self.max = kw_wid['max']
			del kw_wid['max']

		layout = inline_layout(**kwargs)
		widget_args = layout.filter()
		super(reDateEntry, self).__init__(master, **widget_args)

		kw_wid['textvariable'] = self.stvar
		self.configure(kw_wid)
		self.style.configure(self._mystyle_name, fieldbackground=self.bg, foreground=self.fg)
		self.update()
		self.update_idletasks()
		if len(kw_pak) != 0:
			self.pack(kw_pak)
	def insert(self, pos, date="01/01/1970"):
		super().insert(pos, date)
		self._isvalid()
	def get(self):
		return self.stvar.get(), self._isvalid()
	def _isvalid(self):
		try:
			if self.stvar.get() not in ['', None]:
				match = re.match(self.regex, self.stvar.get())
				if not match or self.parse_date(self.stvar.get()) > datetime.now().date():
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
