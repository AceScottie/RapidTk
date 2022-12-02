from .__main__ import *
from .rTkUtils import coord, clipboard
from .cWidgets import *
from .cWidgets_extended import *
from .reWidgets import *
from .matchart import Chart
from .flags import *
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
#		version_info = (0, 0, 1)
#		return ".".join([str(x) for x in version_info])
#__all__ = ['.rapidTk.*', '.objects.*', '.utils.coord']
__version__ = "0.3"
