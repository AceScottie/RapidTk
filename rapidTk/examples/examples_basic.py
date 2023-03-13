import sys
from tkinter import Scrollbar, Event

from rapidTk import *
import logging
rtklog = logging.getLogger('rapidTk')
rtklog.setLevel(0)

"""
rapdTk Log Levels:
|   1| Standard User Logging (meant for user code)
|   9| Dedug Logging
|  19| Information Logging
|  29| Warning Logs
|  39| Error Logs
|  49| Critical Logs
|  99| Verbose Logs (all logs, all timers, all function calls)
| 100| Unit Logs (used for unit testing to assert True if test succees)
"""


def example_basic_objects():
	"""
	To create a rapidTk instance use the rapidTk() method which overwires the Tk() method and returns the Tk() method.
	As it returns the Tk() method all commands on root are still valid if they are valid on a Tk() object.
	rTk only uses Pack() methods over grid() and place(). grid() may be added in the future however place() will not be supported due to bad design useage.

	PackProcess() is a class that lets you create all objecst in the correct order and the pack them in that order later.
	to use, initilise the class and use the add() method to add widgets to the list and finally call the pack() method.
	add() acceps all standard .pack() options and returns the widget unlike the original pack() method.
	e.g. myFrame = pp.add(cFrame(root), side=TOP) #accepts rapidTk Widgets
		 myFrame2 = pp.add(Frame(root), side=TOP) #accepts Tkinter Widgets

	c(Widget) is a class that overwites the original widget while keeping the widget accessible.
	There may be addition options avaibleble in the cWidget however all original options are kept too keep it as compatible as possible.
	All cWidgets, reWidgets and extended Widgets will have the methods of get_self(), get_parent() and get_root().
	These methods will return the Widget, the widgets parent or the root Widget.

	cLabel has 2 additional methods of get() and set() which get and set the text option.

	cEntry() has an addition option of value which automatically sets up a StringVar textvariable and sets that to the value.
	It also creates a popup rightclick menu for cut, copy, select all and paste.

	"""
	root = rapidTk()
	pp = PackProcess()
	main = pp.add(cFrame(root), side=TOP, fill=BOTH, expand=1)
	pp.add(cLabel(main, text="This is a basic rapidTk Label."), side=TOP, fill=X)
	pp.add(cButton(main, text="This is an Example Button"), side=TOP)
	pp.add(cEntry(main, value="Some Default Text"), side=TOP, fill=X)
	pp.pack()
	root.mainloop()


def example_basic_objects2():
	"""
	cCanvas (WIP) is just a canvas widget with no special functions yet.

	cTreeview is an TreeView widget with automatic row-highligh, colour options and sort options.
	It can also be linked to a checkbox to hide data automatically, this is shown in the opts.var.trace method.

	cScrolledText() has a default value that can be set. It also has the same menu as cEntry with cut, copy, selectall and paste options

	cCheckbutton() has get() and set() methods which use the IntVar built into the class.

	cOptionMenu() has a defautl value, a list of valid options and a list of none valid options if needed.
	If the default value is part of the options it will not duplicate it in the options.
	non_valid is just a safe way to remove options over time without adjusting code. This can be used if options is gathered from an external source.

	"""
	root = rapidTk()
	pp = PackProcess()
	
	cv = pp.add(cCanvas(root), side=TOP, fill=BOTH, expand=1)
	##example TreeView
	treeFrame = pp.add(cFrame(cv), side=TOP, fill=X, expand=1)
	myTree = pp.add(cTreeview(treeFrame), side=LEFT, fill=X)
	vsb = pp.add(Scrollbar(treeFrame, orient="vertical",command=myTree.yview), side=LEFT, fill=Y) 
	myTree.configure(yscrollcommand=vsb.set)
	myTree.set_cols(['Test1', 'Test2'])
	for i in range(0, 30, 2):
		rc = myTree.insert(values=[str(i), str(i+1)])
		if i%3 == 0 and i != 0:
			myTree.detached_data.append(rc)

	myText = pp.add(cScrolledText(cv, value="This is a test Value\nWith Multiple\nLines"), side=TOP)
	f2 = pp.add(cFrame(cv), side=TOP, fill=BOTH, expand=1)
	myCheck = pp.add(cCheckbutton(f2), side=TOP)
	myOptions = pp.add(cOptionMenu(f2, default='Hello', options=['Hello', 'World', 'How', 'are', 'you', '?'], non_valid=['are']), side=TOP)
	
	myCheck.var.trace('w', lambda a, b, c, e=Event(), v=myCheck:myTree.hide(a, b, c, e, v))
	pp.pack()
	root.mainloop()


def example_no_PackProcess():
	"""
	PackProcess() is an optional extra, all cWidgets support inline packing and also the .pack() method.
	This can be extended to use .grid() and .place() if required.]
	The down side to inline packing is it creates and packs widgets 1 at a time making layouts be created in the order coded.
	"""
	root = rapidTk()
	main = cFrame(root, side=TOP, fill=BOTH, expand=1)
	cLabel(main, text="This is a basic rapidTk Label.", side=TOP, fill=X)
	cButton(main, text="cButton", side=TOP)
	myEntry = cEntry(main, value="Some Default Text").pack(side=TOP, fill=X) ##example using the standard .pack() method
	root.mainloop()


@time_it
def example_basic_logging_timed_widgets(pp, master, count): ##used as part of example_basic_logging()
	widgets = []
	for i in range(count):
		widgets.append(pp.add(cLabel(master, text=f'{i} :: {__name__}'), side=TOP))
	return widgets
@time_it
def example_basic_logging():
	"""
	rapidTk contains its own logging options.
	To enable logging simply call logging.getLogger('rapidTk').setLevel(level) with level > 0
	To disable logging set level to 0

	most logging will be handled internally by rapidTk, however a custom log method has been included to replace normal print() statements.
	to use simply get the logger and use the rtklog('message') method as shown in the below example.
	rapidTk also implements a performance timer wrapper to easlily identify how long widget creating is taking.
	add the @time_it wrapper to any function and set log level to 99 to start collecting timers.
	"""

	rtklogger = logging.getLogger('rapidTk') ##get the rapidTk logger
	rtklogger.setLevel(99) # sets log level to 99 for verbose logging.
	#rtklogger.setLevel(1) # sets log level to  1 for user logging

	#Create a basic window
	root = rapidTk()
	root.geometry('320x150')
	pp = PackProcess()
	main = pp.add(cFrame(root), side=TOP, fill=BOTH, expand=1)

	widgets = example_basic_logging_timed_widgets(pp, main, 100)
	#rtklogger.rtklog(widgets)

	rtklogger.rtklog('all widgets have been created, starting packing')
	pp.pack()
	rtklogger.rtklog('widgets have been packed | starting mainloop')
	root.mainloop()
	

def example_basic_menu():
	"""
	cMenu is a quick and efficent way to make simple menus.
	The only thing you need to provide is context on creation.
	context is a dictionary of {Menu(.submenu(s)).Label : command}
	example:
	context={"Menu.Submenu1.Submenu2.options":lambda m="test":print(m)}
	will create a main menu called "Menu" with a submenu called Submenu1 with a submenu called "Submenu2" with an option called "options"
	The "options" option will run the command when clicked.

	Note: subtree paths do not stack.
	"Menu.Submenu1.Submenu2" is not the same as "Submenu1.Submenu2".
	This will create 2 menus called "Menu" and "Submenu1"

	all submenus and options can be accessed though the cMenu.sub_menus and cMenu.options dictionarys.
	"""
	root = rapidTk()
	root.geometry('320x150')
	main = cFrame(root, side=TOP, fill=BOTH, expand=1)
	
	menu_context = {
	'File.Open': lambda m="Open":print(m),
	'File.System.Advanced.Close': lambda m="Close":print(m),
	'File.Quit': lambda m="Quit":print(m),
	'System.Kill': lambda m="Kill":print(m),
	'Exit': lambda m="Exit":print(m)
	}
	myMenu = cMenu(root, context=menu_context)
	log = logging.getLogger('rapidTk')
	log.rtklog(myMenu.sub_menus) ## this retuns a dictionary of 'contextname':widget for each menu item created from context
	log.rtklog(myMenu.options) ## TODO: add value for options ## This returns a dictionary of 'contextname':value for each item created with context.

	root.config(menu=myMenu) ##standard tkinter menu
	root.bind("<Button-3>", myMenu._do_popup) #bind to right click when widget clicked.
	root.mainloop()


def example_get_runner(event, options, start, end, widgets, out): ##used as part of example_get()
	out.configure(text=widgets[options.get()].get(start.get(), end.get()))
def example_get():
	"""
	cWidgets that have text values support the get() method.
	get(start, end) or get() are both valid options for all widgets that support the get() method.
	!This overwrites the standard tk get() method. 

	"""
	root = rapidTk(log_level=0)
	pp = PackProcess()
	main = pp.add(cFrame(root), side=TOP, fill=BOTH, expand=1)

	config = pp.add(cFrame(main, borderwidth=3, relief='raised'), side=TOP, fill=BOTH, expand=1)
	holder = pp.add(cFrame(main, borderwidth=3, relief='groove'), side=TOP, fill=BOTH, expand=1)
	w={}
	w['cLabel'] = pp.add(cLabel(holder, text="This is a basic rapidTk Label."), side=TOP, fill=X)
	w['cButton'] = pp.add(cButton(holder, text="This is an Example Button"), side=TOP)
	w['cEntry'] = pp.add(cEntry(holder, value="Some Default Text"), side=TOP, fill=X)

	options = pp.add(cOptionMenu(config, options=['cLabel', 'cButton', 'cEntry']), side=LEFT, fill=X)
	start = pp.add(cEntry(config, value=""), side=LEFT, fill=X)
	start.set(None, "Some Text")
	end = pp.add(cEntry(config, value=""), side=LEFT, fill=X)

	output = pp.add(cLabel(holder, text="This will be the output"), side=TOP)
	pp.add(cButton(config, text="Check Output", command=lambda e=Event, o=options, s=start, ed=end, w=w, out=output: example_get_runner(e, o, s, ed, w, out)), side=TOP)

	
	pp.pack()
	root.mainloop()
def example_set_runner(event, options, index, inp, widgets, out): ##used as part of example_set()
	widgets[options.get()].set(index.get(), inp.get())
def example_basic_set():
	"""
	!WIP! This feature is currently a WIP and only works for cButton, cLable, cEntry, cScrolledText and their subclasses (e.g. reEntry, ImageLabel, iButton)
	As with get() all widgets with text values will support the set() method.
	set(index, text) and set(text) are both valid options.
	set(index, text) will get the origial text valie and append the text from the index position (this will remove any additional text beyond index+text length)
	set(text) will clear the current text and replace it with the specified text

	!This overwrites the tkinter set() method.
	"""
	root = rapidTk(log_level=0)
	pp = PackProcess()
	main = pp.add(cFrame(root), side=TOP, fill=BOTH, expand=1)

	config = pp.add(cFrame(main, borderwidth=3, relief='raised'), side=TOP, fill=BOTH, expand=1)
	holder = pp.add(cFrame(main, borderwidth=3, relief='groove'), side=TOP, fill=BOTH, expand=1)
	w={}
	w['cLabel'] = pp.add(cLabel(holder, text="This is a basic rapidTk Label."), side=TOP, fill=X)
	w['cButton'] = pp.add(cButton(holder, text="This is an Example Button", cursor='@../assets/cur.cur'), side=TOP)
	w['cEntry'] = pp.add(cEntry(holder, value="Some Default Text"), side=TOP, fill=X)

	options = pp.add(cOptionMenu(config, options=['cLabel', 'cButton', 'cEntry']), side=LEFT, fill=X)
	ind = pp.add(cEntry(config, value=""), side=LEFT, fill=X)
	set_input = pp.add(cEntry(config, value=""), side=LEFT, fill=X)
	set_input.set(None, "Some Text")

	output = pp.add(cLabel(holder, text="This will be the output"), side=TOP)
	pp.add(cButton(config, text="Set text", command=lambda e=Event, o=options, i=ind, inp=set_input, w=w, out=output: example_set_runner(e, o, i, inp, w, out)), side=TOP)

	
	pp.pack()
	root.mainloop()

def switch_language(e:Event, _l:localization, b:cButton, lb:cLabel): ##used as part of example_basic_language
	_l.set_local('fr') ##sets the local language strings present in fr.xml
	lb.configure(text=_l.example.hello) ##changes the string to the new fr.xml -> resource.example.hello string
	b.configure(text=_l.example.changeLanguage) ##changes the string to the new fr.xml -> resource.example.changeLanguage string


def example_baisc_language():
	"""
	A global language string subsystem.
	This allows you to configure xml files (format found in assets/local/) and create a sequence of strings.
	having multiple xml files allows the user to switch between different string definitions or languages by calling the set_local() method with the filename of the xml.

	it is recommended to set the call on a global scope and use _l or similar to access it throughout your code.

	this can also be used to replace long string values into simple dot notated refrences making code look cleaner.
	"""
	_l = localization(lang='en_gb', localpath='../assets/local/') ## initilise the string resources using the en_gb.xml file found in the ../assets/local/ path.
	
	root = rapidTk()
	lb = cLabel(root, text=_l.example.hello, side=TOP) ## use the string found in en_gb.xml -> resrouces.example.hello 
	change = cButton(root, text=_l.example.changeLanguage, side=TOP) ## use the string found in en_gb.xml -> resrouces.example.changeLanguage 
	change.configure(command=lambda e=Event(), _l=_l, lb=lb, b=change:switch_language(e, _l, b, lb)) 
	root.mainloop()

def uuid_printer(event, widget):
	print(f"This button has the UUID: {widget.uuid}")
def uuid_print_all(event, widget):
	print(widget.get_root().uid)
def example_uuids():
	"""
	All basic widgets in rapidTk have a Unique Identifier which is stored in the metaclass _UniqueIdentifiers()
	You can generate a new uuid by calling `uuid = _UniqueIdentifiers().new()
	Also you can add your own unique identifieds with `_UniqueIdentifiers().append('[UniqueIdentifier]')`
	Attemping to manually add an existing identifier will raise a duiplicateIDError
	You can see all used UUIDs by calling get_root().uid on any widget to get a list of UUIDs
	"""
	root = rapidTk()
	pp = PackProcess()
	main = pp.add(cFrame(root), side=TOP, fill=BOTH, expand=1)
	b1 = pp.add(cButton(main, text="Button 1"), side=TOP, fill=X)
	b2 = pp.add(cButton(main, text="Button 2"), side=TOP)
	b3 = pp.add(cButton(main, text="Button 3"), side=TOP, fill=X)

	b4 = pp.add(cButton(main, text="Print all UUID"), side=TOP, fill=X)

	b1.configure(command=lambda e=Event(), w=b1:uuid_printer(e, w))
	b2.configure(command=lambda e=Event(), w=b2:uuid_printer(e, w))
	b3.configure(command=lambda e=Event(), w=b3:uuid_printer(e, w))
	b4.configure(command=lambda e=Event(), w=b3:uuid_print_all(e, w))
	pp.pack()
	root.mainloop()

def example_spinbox_trigger(event, widget):
	print(f"current: {widget.get()}, next:{widget.next()}, previous:{widget.previous()}")
def example_spinbox_callback(widget, direction:bool):
	print(f"value={widget.get()}")
	print(f"stringvar={widget.var.get()}")
	print(f"{direction=}")
def example_spinbox():
	"""
	cSpinbox is modified version of the overridden Spinbox (see rTkOverrides).
	It automatically binds the mousewheel if root is an instance of rapidTk.
	It automatically sets the `command` keyword to perform the same action as the mousewheel (which can be overriden by the user).
	It automatically handels wrapping if the `wrap` keyword is set to 1 or True.
	The 'callback' keyword acceps a function with widget and direction args which will be called after a (scroll/button) event is performed.
	"""
	root = rapidTk()
	sp1 = cSpinbox(root, values=[str(x) for x in range(10)], wrap=1, callback=example_spinbox_callback, side=TOP)
	sp1.bind('<Return>', lambda e=Event(), w=sp1: example_spinbox_trigger(e, w))
	root.mainloop()
	"""
	The overriden Spinbox has a few additional methods.
	next(wrap:bool) -> returns the next item in the values (if not wrap and item is last index returns last index item).
	previous(wrap:bool) -> returns the previous item in the values (if not wrap and item is 0th index returns 0th index item).
	spin(direction:bool) -> configures the Spinbox to the next/previous item based on the input direction (True:up, False:down)
	configure(**kwargs) -> calls the configure() method of the super class. if one of the keywords is `values` sets the attribute values to the keyword `values`
	"""


if __name__ == "__main__":
	example_spinbox()