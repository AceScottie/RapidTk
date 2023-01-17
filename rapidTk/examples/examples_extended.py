from tkinter import *
from rapidTk import *
import logging

def example_TimePicker():
	"""
	DOC STRING
	"""
	root = rapidTk()
	root.geometry("500x500+300+300")
	f = cFrame(root, side=TOP, expand=1, fill=BOTH)
	cButton(f, text="test", side=TOP)

	f2 = cFrame(f, bg="red", side=TOP)
	
	b = TimePicker(f2)
	b.pack(side=TOP)

	cButton(f, text="test", side=TOP)
	root.mainloop()

def example_form_submit(event, form):
	valid = form.validate() ##checks if all validation regex matches and if so returns true (also sets colours to red on failed validations.)
	print(valid)
	if valid:
		data = form.results()
		for k, v in data.items():
			print("%s : %s "%(k,v))

def example_form():
	"""
	!WIP! 
	!-- This feature is highly experimental and is likly to change --!
	To make a form follow a standard format.
	item = widgettype + unique 2char (dict object must have a unique name) :str
	name = the code reference name. will eval to form.data()['form_name'] :str
	label = 'The form question text' : str
	textwidth = the width of the lable that contains the question text, use to allign questions. : int
	width = the width of the answer box. : int
	text = the default input for the question box.
	**kwargs = standard kwargs supported by the indervidual widgets.
	
	example format:
	options = {
	"Section_Title":{Item00:{"name":"item1", "label":"my question", "textwidth":10, "width":20, "text":"Default Answer"}}
	}

	example Label:
	"Basic Information":{"Labelfn":{"name":"fn", "label":"First Name:", "textwidth":15, "width":30, "text":"John Smith"}}
	example Entry:
	"Basic Information":{"Entrycn":{"name":"cn", "label":"County:", "textwidth":10, "width":30, "text":"The Shire"}}

	To add validation to any of the form componenets use the 'validation' keyword with a regex input

	example validation enabled Entry:
	"Random Numbers":{"Entryrn":{"name":"rn", "label":"Input Number:", "textwidth":10, "width":5, "text":"Not Valid", "validation":"^\\d*$"}}

	example additional options:
	"Random Numbers":{"ScrollTexthg":{"name":"hg", "label":"ScrollText with height", "textwidth":25, "width":30, "text":"Multi\nline\ninput", "height":3}}

	complete form:
	options = {
	"Basic Information":
		"Labelfn":{"name":"fn", "label":"First Name:", "textwidth":15, "width":30, "text":"John Smith"},
		"Entrycn":{"name":"cn", "label":"County:", "textwidth":10, "width":30, "text":"The Shire"},
		}
	"Random Numbers":
		"Entryrn":{"name":"rn", "label":"Input Number:", "textwidth":10, "width":5, "text":"Not Valid", "validation":"^\\d*$"}
		"ScrollTexthg":{"name":"hg", "label":"ScrollText with height", "textwidth":25, "width":30, "text":"Multi\nline\ninput", "height":3}
		}
	}

	"""

	root = rapidTk()
	root.geometry("400x800")
	scroll = scrollArea(root, h=1, side=TOP, fill=BOTH, expand=1)
	window = cFrame(scroll.sFrame, side=TOP, fill=BOTH, expand=1)
	holder = cFrame(window, height=root.winfo_height()+1, side=TOP, fill=BOTH)
	tw = 10
	ww = 60

	auto_options = ["apple", "banana", "pear", "apple pie", "banana pie"]
	options = {
	"Basic Information":{
		"Labelfn":{"name":"fn", "label":"First Name:", "textwidth":15, "width":30, "text":"John Smith"},
		"Entrycn":{"name":"cn", "label":"County:", "textwidth":10, "width":30, "text":"The Shire"}
		},
	"Random Numbers":{
		"Entryrn":{"name":"rn", "label":"Input Number:", "textwidth":10, "width":5, "text":"Not Valid", "validation":"^\\d*$"},
		"ScrollTexthg":{"name":"hg", "label":"ScrollText with height", "textwidth":25, "width":30, "text":"Multi\nline\ninput", "height":3}
		}
	}
	form = qForm()
	form.create_questions(holder, options, {"config":"confgiration"})
	submit = cButton(holder, text="Confirm", command=lambda e=Event(), f=form:example_form_submit(e, f), side=BOTTOM)

	root.mainloop()

if __name__ == "__main__":
	example_form()
