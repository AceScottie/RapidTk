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