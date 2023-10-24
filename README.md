# Character-Bitmap-Editor
A Character ROM Editor for the LS7 Computer, written in Python 3


# Overview
![alt text](https://github.com/0xMAC8205/Character-Bitmap-Editor/assets/55045978/413ec10d-cec2-4d39-969c-e04246f455e8)

Being written in Python, this editor is multi-platform.
It's based on this program: https://www.min.at/prinz/o/software/pixelfont

# .bmf file type
'.bmf' literally stands for 'Bit Map File'.
It holds the drawn characterset as raw bytes.

Different from the "Raw Bytes" output file,
by having a small info header at the start,
but almost identical.

# Exporting
The Program supports, exporting to an Assambler Include
(for the people whom may desire),
a C byte array or just a raw binary file.

The Converted binary file, will be 2k or 4k in size
(Depending on, if 8x8 or 8x16 mode is used)

# Dependencies
> python3

> tkinter

# Known issues
* Drawn content getting applied, when exiting current cell
* Tooltips are buggy, with multiple instances open
* 8x16 Character exports don't work currently
* UI missalignment in MacOS
* Slow in MacOS (maybe Tkinter's fault)
