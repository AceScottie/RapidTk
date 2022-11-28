class TemplateException(Exception):
	def __init__(self, message):
		super().__init__(message)
class TaskIdExistsError(TemplateException):
	def __init__(self):
		pass
class TaskIdNotExistsError(TemplateException):
	def __init__(self):
		pass
class duiplicateIDError(TemplateException):
	def __init__(self):
		message = "Value already exists as UID"
		super().__init__(message)
class duiplicateIDError(TemplateException):
	def __init__(self):
		message = "Tab with this id has not been created"
		super().__init__(message)
class PlatformError(TemplateException):
	def __init__(self):
		message = "This module does not work on this platform"
		super().__init__(message)
class DateEntryNotFoundException(TemplateException):
	def __init__(self):
		message = "tkcalendar module not found.\nPlease install tkcalendar module to use DateEntry widgets."
		super().__init__(message)
class KeywordError(TemplateException):
	def __init__(self, keyword):
		message = f"There was an unexpected keyword presented {keyword}"
		super().__init__(message)
class MenuContexError(TemplateException):
	def __init__(self):
		message = "context should be a {type}|{name}:command dictionary pair"
		super().__init__(message)
class RadioContexError(TemplateException):
	def __init__(self):
		message = "Contex should be a {label}:{value} dictionary pair"
		super().__init__()
		