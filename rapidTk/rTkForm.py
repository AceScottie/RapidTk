from tkinter import TOP, LEFT, RIGHT, BOTTOM, X, Y, BOTH
from tkinter import Event, INSERT
import re
from .cWidgets import cEntry, cButton, cFrame, cLabel, cCanvas, cTreeview, cCheckbutton, cScrolledText, cMenu, cSpinbox, cOptionMenu, cScale
from .reWidgets import reEntry, reCombobox, reOptionMenu, reautoEntry, reScrolledText
try:
	import tkcalendar
	from .rTkCalendar.rTkCalendar import DateEntry, cDateEntry, reDateEntry
except:
	raise DateEntryNotFoundException
	class DateEntry:
		def __init__(self, master, **kwargs):
			raise DateEntryNotFoundException
	class cDateEntry:
		def __init__(self, master, **kwargs):
			raise DateEntryNotFoundException
	class reDateEntry:
		def __init__(self, master, **kwargs):
			raise DateEntryNotFoundException
class qForm:
	def __init__(self):
		self.questions = {}
	def __create_section(self, holder, objects, configuration, frames, pp):
		for sec, obj in objects.items():
			section = pp.add(cFrame(holder), side=TOP, fill=BOTH, expand=1)
			pp.add(cLabel(section, text=sec, anchor="center"), side=TOP, fill=X)
			self.__create_option(section, obj, configuration, frames, pp)
	def __create_option(self, section, obj, configuration, frames, pp):
		for ob_name, opts in obj.items():
			f = pp.add(cFrame(section, **configuration), **frames)
			name  = opts.pop('name')
			self.questions[name] = {"label":pp.add(cLabel(f, text=opts.pop('label'), width=opts.pop('textwidth'), anchor="e"), side=LEFT), "object":None, "validation":None, "bg":None, 'fg':None}
			insert = opts.pop('text', None)
			p_opts = opts.pop("p_opts", {})
			if "validation" in opts:
				self.questions[name]['validation'] = opts.pop('validation', None)
			self.__create_element(name, ob_name, opts, insert, f, p_opts, pp)
	def __create_element(self, name, ob_name, opts, insert, f, p_opts, pp): ##TODO: shorten this.
		match ob_name[:-2]:
			case "Entry":
				self.questions[name]["object"] = pp.add(reEntry(f, **opts), side=RIGHT, **p_opts)
				try:
					if insert != None:
						self.questions[name]['object'].insert(INSERT, insert)
				except:
					print("Exception: %s Entry %s"%(name, insert))
			case "autoEntry":
				self.questions[name]["object"] = pp.add(reautoEntry(f, **opts), side=RIGHT, **p_opts)
				try:
					if insert != None:
						self.questions[name]['object'].insert(INSERT, insert)
				except:
					print("Exception: %s autoEntry %s"%(name, insert))
			case "Label":
				opts['text'] = insert
				self.questions[name]["object"] = pp.add(cLabel(f, **opts), side=RIGHT, **p_opts)
			case "DateEntry":
				self.questions[name]["object"] = pp.add(reDateEntry(f, **opts), side=RIGHT, **p_opts)
				try:
					if insert != None:
						self.questions[name]['object'].insert(INSERT, insert)
				except:
					print("Exception: %s DateEntry %s"%(name, insert))
			case "Checkbutton":
				self.questions[name]["object"] = pp.add(cCheckbutton(f, **opts), side=RIGHT, **p_opts)
				try:
					if insert != None:
						self.questions[name]['object'].set(int(insert))
				except:
					print("Exception: %s Checkbutton %s"%(name, insert))
			case "ScrollText":
				self.questions[name]["object"] = pp.add(cScrolledText(f, **opts), side=RIGHT, **p_opts) ##TODO: create reScrolledText
				try:
					if insert != None:
						self.questions[name]['object'].insert(INSERT, insert)
				except:
					print("Exception: %s ScrollText %s"%(name, insert))
			case "Option":
				self.questions[name]["object"] = pp.add(cOptionMenu(f, **opts), side=RIGHT, **p_opts)
				try:
					if insert != None:
						self.questions[name]['object'].set(insert)
				except:
					print("Exception: %s Option %s"%(name, insert))
			case "Combobox":
				self.questions[name]["object"] = pp.add(reCombobox(f, **opts), side=RIGHT, **p_opts)
				try:
					if insert != None:
						self.questions[name]['object'].set(insert)
				except:
					print("Exception: %s Combobox %s"%(name, insert))
			case "Scale":
				self.questions[name]["object"] = pp.add(cScale(f, **opts), side=RIGHT, **p_opts)
				try:
					if insert != None:
						self.questions[name]['object'].set(insert)
				except:
					print("Exception: %s Scale %s"%(name, insert))
					raise
			case _:
				raise ValueError(f"{ob_name[:-2]} is not part of this form")
	def create_questions(self, holder, objects, configuration={}, frames={} , layout_manager=None):
		if layout_manager is None:
			pp = PackProcess()
		else:
			pp = layout_manager
		self.__create_section(holder, objects, configuration, frames, pp)
		if layout_manager is None:
			pp.pack()
	def results(self):
		results = {}
		for k, v in self.questions.items():
			try:
				results[k] = v['object'].get()
			except:
				raise
		return results
	def validate(self):
		validation_valid = True
		for k, v in self.questions.items():
			value = v['object'].get()
			if isinstance(value, tuple):
				return value[1]
				value = value[0]
			if v['validation'] is not None and str(type(v['object'])) != "<class 'rTk.objects.autoEntry'>":
				pattern = re.compile(v['validation'], re.IGNORECASE)
				valid = pattern.match(str(value))
				print(f"validation {str(value)} -> {v['validation']} {valid}")
				if not valid:
					v['object'].configure(bg="red")
					validation_valid = False
				else:
					if v['object'].cget('background') == "red":
						if str(type(v['object'])) != "<class 'rTk.objects_ext.autoEntry'>":
							v['object'].configure(bg=v['object'].winfo_toplevel().option_get('background', '.') or '#FFFFFF', fg=v['object'].winfo_toplevel().option_get('foreground', '.') or '#000000')
						else:
							v['object'].configure(bg=v['object'].bg, fg=v['object'].fg)
			elif str(type(v['object'])) == "<class 'rTk.objects_ext.autoEntry'>":
				if value not in v['object'].auto:
					v['object'].configure(bg="red")
					validation_valid = False
				else:
					v['object'].configure(bg=v['object'].bg, fg=v['object'].fg)
		return validation_valid
	def update(self, question, value):
		self.questions[question]['object'].set(value)
	def get(self, option):
		return self.questions[option].get()