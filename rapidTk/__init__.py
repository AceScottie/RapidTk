from rapidTk.__main__ import *
from rapidTk.tkoverride import *
from rapidTk.rTkUtils import *
from rapidTk.rTkUtils import _UniqueIdentifiers
from rapidTk.cWidgets import *
from rapidTk.cWidgets_extended import *
from rapidTk.reWidgets import *
from rapidTk.rTkForm import qForm
from rapidTk.matchart import Chart
from rapidTk.flags import *
from rapidTk.language import localization
try:
	import tkcalendar
	from .rTkCalendar.rTkCalendar import DateEntry, cDateEntry, reDateEntry
except:
	class DateEntry:
		def __init__(self, master, **kwargs):
			raise DateEntryNotFoundException
	class cDateEntry:
		def __init__(self, master, **kwargs):
			raise DateEntryNotFoundException
	class reDateEntry:
		def __init__(self, master, **kwargs):
			raise DateEntryNotFoundException

from .rTkLogging import rTkLogger

import logging
logging.setLoggerClass(rTkLogger)

#import types
#class rTk(types.ModuleType):
#	@property
#	def version(self):
#		version_info = (0, 0, 5)
#		return ".".join([str(x) for x in version_info])
#__all__ = ['.rapidTk.*', '.cWidgets.*', '.rtkUtils.*']
__version__ = "0.5"
