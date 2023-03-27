public:: true

- inherits #TemplateException
- Description:
	- Calls the Exception with the type being TaskIdExistsError
- Usage:
	- used by #__main__ for cases where user tries to add a new schedule task with the same ID as an existing task.