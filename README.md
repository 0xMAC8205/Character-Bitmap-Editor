# Character-Bitmap-Editor
A Character ROM Editor written in Python 3


# Overview
![alt text](https://github.com/0xMAC8205/Character-Bitmap-Editor/assets/55045978/85435fa2-8c8e-4169-ae5d-2cc9a46e5995)

Being written in python, this editor is multi-platform.
It's inspired by this program: https://www.min.at/prinz/o/software/pixelfont,
since it's only available on Windows :(

# Exporting
The program supports, exporting to an assambler include
(for the people whom may desire),
a C byte array or just a raw binary file (recommended).

The converted binary file, will be 2k or 4k in size
(Depending on, if 8x8 or 8x16 mode is used)

# Customisation

You can customise the editor. For example the
draw field size, displaying a grid, allowing cursor dragging

You can configure your color theme in $*RUNPATH*/assets/settings/theme.txt,
or inject your custom add-ons.
This file is sourced at applicatinon startup as a normal python script.
(These changes only apply when opening another instance / restarting)

# Interfacing

**Matrix**:
  
You select the character to modify, just by clicking the box or you can cursor around the matrix.
Here => settings "cursor wrapping" might be helpfull

**Draw Field**:
  
You can hold the mousebutton and drag the cursor to draw (depending if cursor drag is enabled)

# .bmf file type
The editor saves it's editable files in the .bmf format.

'.bmf' literally stands for 'Bit Map File'. (I'm not good at naming things)
It holds the drawn characterset as raw bytes.

Different from the "Raw Bytes" output file,
by having a small info header at the start,
but almost identical. (But **Not** Compatible)

# Dependencies
* python3
* tkinter library
* functools library

# Known issues
* Drawn content getting applied, when exiting current cell
* Tooltips are buggy, with multiple instances open
* 8x16 Character exports don't work currently (may deprecate soon)
* UI missalignment and slow performance in MacOS (propably Tkinter's fault)

# ToDo
* Custom export formats (present in /assets/custom_formats, but not implemented)
