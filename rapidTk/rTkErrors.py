import ctypes, inspect
class __get_traceback(int):
	def __call__(self):
		previous_frame = inspect.currentframe().f_back
		(filename,line_number,function_name,lines,index) = inspect.getframeinfo(previous_frame)
		tb = f"Traceback (most recent call last):\n  File {filename}, line {line_number}, in {function_name}\n\n  {'\n  '.join([item.replace('\t', '') for item in lines])}"
		return tb
rtk_traceback = __get_traceback()
class _ExceptionWindow(Exception):
	def __init__(self, message, tb):
		super().__init__(message)
		self.message, self.tb = message, tb
		self.show_message_box()
	def show_message_box(self):
		error_message = f"Exception: {self.message}\n{self.tb}"
		ctypes.windll.user32.MessageBoxW(0, error_message, "Error", 0x10)
		exit(1)
class GUIException:
	def __init__(self, message, tb):
		try:
			raise Exception(message)
		except Exception as err:
			raise _ExceptionWindow(message, tb)

# Example usage:
if __name__ == "__main__":
	raise GUIException("This is a normal exception",rtk_traceback())



class TemplateException(Exception):
	def __init__(self, message):
		super().__init__(message)
class TaskIdExistsError(TemplateException):
	def __init__(self):
		pass
class TaskIdNotExistsError(TemplateException):
	def __init__(self):
		pass
class DuiplicateValueError(TemplateException):
	def __init__(self):
		message = "Value already exists as UID"
		super().__init__(message)
class DuiplicateIdError(TemplateException):
	def __init__(self):
		message = "Tab with this id has not been created"
		super().__init__(message)
class PlatformError(TemplateException):
	def __init__(self):
		message = "This module does not work on this platform"
		super().__init__(message)
class DateEntryNotFoundError(TemplateException):
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
class assertValue:
	def __init__(self, condition, message):
		if not condition():
			print("running condition")
			raise ValueError(message)
class OptionNotPermitted(TemplateException):
	def __init__(self, message):
		super().__init__(f"Error Option Not Permitted: {message}")


