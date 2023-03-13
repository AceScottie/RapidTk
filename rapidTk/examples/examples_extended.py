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


def example_tabs():
	"""
	rapidTk has a tab manager built in.
	A Tab is a unpackeaged Canvas that has 0 width and 0 height which can be easily switched between using the TabManager to keep track.
	Tabs are not returned as Widgets but as simple UIDs.
	You can use the `tabs` attribute of the TabManager to get the widgets which are stored as a list.
	"""
	root = rapidTk()
	tabs = [None, None, None, None] ##defalt list to use later
	tabFrame = cFrame(root, side=TOP, fill=X)

	baseholder = cFrame(root, side=TOP, fill=BOTH, expand=1)
	##Create the Tab references
	tabs[0] = root.tm.new(cCanvas(baseholder), name="Home") ##`name` is an optional kwarg used to reference the tab when direct relations cannot be maintained.
	tabs[1] = root.tm.new(cCanvas(baseholder), name="About")
	tabs[2] = root.tm.new(cCanvas(baseholder), name="Contact")
	tabs[3] = root.tm.new(cCanvas(baseholder), name="Settings")
	
	print(root.tm.tabs)##shows the list of created tabs with their UIDs

	##switch to the selected tab
	root.tm.switch(Event(), tabs[0])

	#create the buttons to switch between tabs
	for t in tabs:
		cButton(tabFrame, text=root.tm.name(t), command=lambda e=Event(), tab=t:root.tm.switch(e, tab), side=LEFT)

	## add some content to each tab.
	t1 = cFrame(root.tm.tab(tabs[0]), bg="red", side=TOP, fill=BOTH, expand=1)
	cEntry(t1, value="Some Text", side=TOP)
	cButton(t1, text="Hello", side=BOTTOM)

	##each tab is independant so if you want to automatically show the content you can pack/grid/place it before opening the tab and its state will be saved.
	t2 = cFrame(root.tm.tab(tabs[1]), bg="green", side=TOP, fill=BOTH, expand=1)
	for i in range(10):
		cButton(t2, text=str(i), side=TOP)

	## if you cannot pass the tab widget to a function then you can recall it back using the optional `name`.
	## the tab uid then can be found using the root.tm.get_by_name(`name`) method.
	## as all widgets have the `get_root` method it can be further expanded by `widget.get_root().tm.tab(widget.get_root().tm.get_by_name(`name`))`
	## this gets the root of a widget, gets the tab name and then gets the tab widget by using that to reference the uid.
	t3 = cFrame(root.tm.tab(root.tm.get_by_name("Contact")), bg="blue", side=TOP, fill=BOTH, expand=1)
	cScrolledText(t3, side=TOP)

	t4 = cFrame(root.tm.tab(tabs[3]), bg="orange", width=30, height=30, side=TOP, fill=BOTH, expand=1)
	root.mainloop()

def example_scroll_manager():
	"""
	The rapidTk scrollmanager should automatically take care of any rapidTk scroll object nativly and enable mouse wheel operations on them all.
	However cusome scrollbars can be added and pushed into the ScrollManager.
	
	`root.sm.add_widget(myCanvas)` 
	this will put the widget myCanvas into the scroll manager, binding it with the Enter, Leave and Mousewheel bindings
	and handeling transitions between child and parent widget.

	as you can see from the example below, all cWidgets should nativly handel scrolling.
	This is still a WIP feature and it may be updated for edge case detection and multi-child/parent switching.
	Note: It has issues with child scrollbars which makes duplicate on-scroll events, i am looking to fix this soon.
	"""

	##taken from example_tabs with slight modifacation for cleaner code.
	root = rapidTk()
	root.geometry("800x600")
	tabs = [None, None, None, None]
	tabFrame = cFrame(root, side=TOP, fill=X, borderwidth=3, relief="groove")
	baseholder = cFrame(root, side=TOP, fill=BOTH, expand=1)
	tabs[0] = root.tm.new(cCanvas(baseholder), name="Home")
	tabs[1] = root.tm.new(cCanvas(baseholder), name="About")
	tabs[2] = root.tm.new(cCanvas(baseholder), name="Contact")
	tabs[3] = root.tm.new(cCanvas(baseholder), name="Settings")
	root.tm.switch(Event(), tabs[0])
	for t in tabs:
		cButton(tabFrame, text=root.tm.name(t), command=lambda e=Event(), tab=t:root.tm.switch(e, tab), padx=10, width=10, side=LEFT)
	##end of modified example_tabs.

	t1 = scrollArea(root.tm.tab(tabs[0]), bg="white", h=1, v=1, side=TOP, fill=BOTH, expand=1)
	#root.sm.add_widget(t1.sCanvas)
	print(type(t1.get_root()))

	exstr = "Hello\nWorld\nHow\nAre\nYou\nToday\n?"
	st = []
	for i in range(20):
		st.append(cScrolledText(t1.sFrame, height=3, value=exstr, side=TOP))
	a1 = cSpinbox(t1.sFrame, side=BOTTOM, values=exstr.split('\n'))
	t2 = scrollArea(root.tm.tab(tabs[1]), bg="white", h=1, v=1, side=TOP, fill=BOTH, expand=1)
	for i in range(30):
		cLabel(t2.sFrame, text=f"World {i}", side=TOP)
	
	t3 = scrollArea(root.tm.tab(tabs[2]), bg="white", h=1, v=1, side=TOP, fill=BOTH, expand=1)
	for i in range(30):
		cLabel(t3.sFrame, text=f"Left {i}", side=TOP)
	
	t4 = scrollArea(root.tm.tab(tabs[3]), bg="white", h=1, v=1, width=30, height=30, side=TOP, fill=BOTH, expand=1)
	for i in range(30):
		cLabel(t4.sFrame, text=f"Right {i}", side=TOP)
	
	
	root.mainloop()


if __name__ == "__main__":
	example_scroll_manager()
