# RapidTk
a wrapper for Tkinter to create objects faster

rapidTk is a simple and modifiable wrapper for the Tkinter GUI framework.

As Tkinter was one of the first things i learnt while using python i though it would make a good learning excersise into complex tasks and creating packages.

The goal of this project is to move away from the basic boxes of Tkinter and create some very complex objects in a simple and easy to use way while keeping the flexability of Tkinter widgets.

Every object will be a collection of Tkinter widgets with additional logic and features stacked over them.

e.g. autoEntry which provides a basic Entry widget with autocompletion options in a smooth and natrual way, or The WindowManager alongside moveable windows for creating and managing lots of grabbable canvas widgets.


Why not use a better framework like Qt or wx ? Because Tkinter is free for both personal and commercial use. Tkinter is basic which allows high expandability on its widgets, and its simple and easy to learn.

This project does not aim to be the best project in the world or even a concice package. Just a collection of objects that will work with or without eachother and make creating interfaces faster, smoother and much easier.

Feel free to add your own ideas, widgets, expansions and logic to this project.


Examples are in the rapidTk/examples/ directory.

example of basic start. Creates a Frame, a Label, a Button and an Entry, then packs them all.
```python
    root = rapidTk() ##replacment for root = Tk()
    pp = PackProcess() ## creates a process loop to pack objects
    main = pp.add(cFrame(root), side=TOP, fill=BOTH, expand=1) ## creates a basic cFrame (replacemnt Frame) and adds it to the process loop to pack.
    pp.add(cLabel(main, text="This is a basic rapidTk Label."), side=TOP, fill=X) ## creates a basic cLabel and adds it to the process loop to pack.
    pp.add(cButton(main, text="cButton"), side=TOP) ## crates a basic cButton and adds it to the process loop to pack.
    myEntry = pp.add(cEntry(main, value="Some Default Text"), side=TOP, fill=X) ## creates a basic cEntry and adds it to the process loop to pack.
    pp.pack() ## runs the process loop that loops through all added widgets and packs them all with the configured options.
    root.mainloop() ## calls mainloop on the normal Tk() object.
```