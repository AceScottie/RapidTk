public:: true

- inherits #cButton #widegBase
- uses `PIL.Image`, `PIL.ImageTK`
- Description:
	- The iButton is a method to create scalable buttons.
	  Provide an image with `margin`px left section and the rest as the middle section
	  The widget with take the left secion, middle section and mirrored left section and make it `width`px wide
	  It can be updated and text can be displayed using sandard #cButton text kword
	  can pass `hovered` and `clicked` kwords as image paths to add on_hover and on_click events to the button however these must be the same size image as the original
- kword: image ->
- kword: margin ->
- kword: hovered ->
- kword: clicked ->
- Methods:
	- `__init__`
	- `_hover`
	- `_click`
	- TODO `get_image` replace this code