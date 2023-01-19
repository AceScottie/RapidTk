from .__main__ import *
from .rTkUtils import *
from .cWidgets import *
from .cWidgets_extended import *
from .reWidgets import *
from .rTkForm import qForm
from .matchart import Chart
from .flags import *
from .language import localization
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
