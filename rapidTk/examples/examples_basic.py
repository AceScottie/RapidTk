import sys
from tkinter import Scrollbar, Event
from rapidTk import *

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
	pp.add(cButton(main, text="cButton"), side=TOP)
	myEntry = pp.add(cEntry(main, value="Some Default Text"), side=TOP, fill=X)
	pp.pack()
	root.mainloop()


def example_basic_objects2():
	"""
	cCanvas (WIP) is just a canvas widget with no special functions yet.

	cTreeview is an TreeView widget with automatic row-highligh, colour options and sort options.
	It can also be linked to a checkbox to hide data automatically, this is shown in the opts.var.trace method.

	cScrolledText() has a default value that can be set. It also has the same menu as cEntry with cut, copy, selectall and paste options

	cCheckbutton() has get() and set() methods which use the IntVar built into the class.

	cOptionMeny() has a defautl value, a list of valid options and a list of none valid options if needed.
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
	print(myMenu.sub_menus)
	print(myMenu.options)

	root.config(menu=myMenu) ##standard tkinter menu
	root.bind("<Button-3>", myMenu._do_popup) #bind to right click when widget clicked.
	

	root.mainloop()

def example_basic_radiobutton():
	"""
	@docstring

	"""
	root = rapidTk()
	root.geometry('320x150')
	main = cFrame(root, side=TOP, fill=BOTH, expand=1)

	context = {'Hello':1, 'World':2, 'Apple':3, 'Banana':4}
	myRadioButton = cRadiobutton(root, context=context, side=TOP)
	myRadioButton.var.trace('w', lambda a,b,c, e=Event(), v=myRadioButton: __get__stuff(e, a, b, c, v))
	
	myRadioButton['Hello'].configure(bg='#FF0000')
	myRadioButton.World.configure(bg='#00FF00')
		



	root.mainloop()

def __get__stuff(e, a, b, c, v):
	print(v.get())

if __name__ == "__main__":
	example_basic_radiobutton()