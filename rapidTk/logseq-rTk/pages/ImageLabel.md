public:: true

- inherits #cLabel #widegBase
- uses `PIL.Image`, `PIL.ImageTK`
- Description:
	- Creates a Label  to run an animated gif. Pass the gif file path to the load method along with the default background colour (for transparent gifs)
- {{renderer :todomaster}}
- TODO Refactor code to implement type hinting and custom kwargs
- methods:
	- `__init__`
	- `load`
	- `unload`
	- `_next_frame`
-