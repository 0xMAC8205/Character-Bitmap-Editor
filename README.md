# Character-Bitmap-Editor
A Character ROM Editor for the LS7 Computer, written in Python 3


# Overview
![alt text](https://github.com/0xMAC8205/Character-Bitmap-Editor/assets/55045978/85435fa2-8c8e-4169-ae5d-2cc9a46e5995)

Being written in Python, this editor is multi-platform.
It's inspired by this program: https://www.min.at/prinz/o/software/pixelfont,
since it's only available on Windows :(

# Exporting
The Program supports, exporting to an Assambler Include
(for the people whom may desire),
a C byte array or just a raw binary file (recommended).

The Converted binary file, will be 2k or 4k in size
(Depending on, if 8x8 or 8x16 mode is used)

# Customisation

You can customise the Editor. For example the
Draw Field size, Displaying a Grid, Allowing Cursor Dragging

You can configure your color theme in ($*RUNPATH*)/assets/settings/theme.txt,
or inject your custom add-ons.
(These changes only apply when opening another instance / restarting)

# Interfacing

**Matrix**:
  
You Select the Character to modify, just by clicking the Box or you can cursor around the matrix.
Here => Settings "Cursor Wrapping" might be helpfull

**Draw Field**:
  
You can hold the mousebutton and drag the cursor to draw (depending if Cursor Draw is enabled)

# .bmf file type
'.bmf' literally stands for 'Bit Map File'.
It holds the drawn characterset as raw bytes.

Different from the "Raw Bytes" output file,
by having a small info header at the start,
but almost identical. (But **Not** Compatible)

# Dependencies
* python3
* tkinter
* functools

# Known issues
* Drawn content getting applied, when exiting current cell
* Tooltips are buggy, with multiple instances open
* 8x16 Character exports don't work currently
* UI missalignment in MacOS
* Slow in MacOS (maybe Tkinter's fault)
