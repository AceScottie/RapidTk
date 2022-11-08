from .__main__ import *
from .utils import coord, clipboard
from .objects import *
from .objects_ext import *
from .matchart import Chart
from .flags import *
try:
	import tkcalendar
	from .tkCalendar_ext.calendar_ext import DateEntry, cDateEntry, reDateEntry
except:
	print("tkcalendar missing")
	raise
	class DateEntry:
		def __init__(self, master, **kwargs):
			raise DateEntryNotFoundException
	class cDateEntry:
		def __init__(self, master, **kwargs):
			raise DateEntryNotFoundException
	class reDateEntry:
		def __init__(self, master, **kwargs):
			raise DateEntryNotFoundException

#import types
#class rTk(types.ModuleType):
#	@property
#	def version(self):
#		version_info = (0, 0, 1)
#		return ".".join([str(x) for x in version_info])
#__all__ = ['.rapidTk.*', '.objects.*', '.utils.coord']
__version__ = "0.0.1"
