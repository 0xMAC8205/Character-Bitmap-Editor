from functools import partial
import tkinter as tk
import tkinter.filedialog as file
import tkinter.messagebox as messagebox
import os

InfoText = """Character Generator v.b.3
build on May 16th, 2023
by Gabriel Weingardt

Feel free to modify ;)
github.com/0xMAC8205

Known issues:
>  Draw Box Applying when
   selecting a Character box"""

ToDo = """
- Correct 8x16 Char Export
"""


class Main(tk.Tk):
    def __init__(self, mode, carry_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.exit_protocol)
        self.Path = os.path.abspath(os.path.dirname(__file__)).replace("\\", "/") + "/assets"

        self.Mode = mode
        self.X_Select = 0
        self.Y_Select = 0

        self.BrushVar = tk.IntVar()
        self.Size = tk.IntVar()
        self.Grid = tk.IntVar()
        self.Drag = tk.IntVar()
        self.Wrap = tk.IntVar()
        self.Hint = tk.IntVar()
        self.Tooltip = tk.IntVar()
        self.ProjectSize = tk.IntVar()
        self.BrushVar.set(2)
        self.ProjectSize.set(0)

        self.background = "#FFFFFF"
        self.foreground = "#000000"
        self.draw_off = "#FFFFFF"
        self.draw_on = "#000000"
        self.font = "Arial 12 bold"

        self.Copy = [0 for _ in range(16)]

        self.X_Text = []
        self.Y_Text = []

        self.File_Formats = []

        self.CurrentFile = ""

        try:
            self.Preset = open(self.Path + "/settings/settings", "rb")

            self.Size.set(int.from_bytes(self.Preset.read(1), "big"))
            self.Grid.set(int.from_bytes(self.Preset.read(1), "big"))
            self.Drag.set(int.from_bytes(self.Preset.read(1), "big"))
            self.Wrap.set(int.from_bytes(self.Preset.read(1), "big"))
            self.Hint.set(int.from_bytes(self.Preset.read(1), "big"))

            self.Preset.close()

            for i in os.listdir(self.Path + "/custom_formats"):
                if len(i) > 3 and not i[0] == ".":
                    self.File_Formats.append(i)

            self.Format = open(self.Path + "/settings/theme.txt", "r")
            self.import_code(self.Format.read().splitlines())
            self.Format.close()

        except Exception as e:
            print("Error in Reading Settings:\n", e)
            open(self.Path + "/settings/settings", "w").close()

            self.BrushVar.set(2)
            self.Size.set(16)
            self.Grid.set(1)
            self.Drag.set(1)
            self.Wrap.set(0)
            self.Hint.set(0)

            open(self.Path + "/settings/theme.txt", "w").close()

        self.config(bg=self.background)

        self.Matrix = []
        self.Characters = {}

        self.UpperFrame = tk.Frame(master=self, bg=self.background)
        self.UpperFrame.pack(side="top", fill="both", expand=0)
        self.Frame = tk.Frame(master=self, bg=self.background)
        self.Frame.pack(side="bottom", fill="y", expand=0)
        self.LowerFrame = tk.Frame(master=self.Frame, bg=self.background)
        self.LowerFrame.pack(side="bottom")
        self.InfoBox = tk.Frame(master=self.Frame, bg=self.background)
        self.InfoBox.pack(side="bottom")

        self.Options = tk.LabelFrame(master=self.LowerFrame, bg=self.background, fg=self.foreground,
                                     text="Options:", font=self.font,)
        self.Options.pack(side="right", anchor="s", expand=0, fill="y")
        self.DrawFrame = tk.Frame(master=self.LowerFrame, bg=self.background)
        self.DrawFrame.pack(side="right", anchor="s", expand=0, fill="y")
        self.Toolbox = tk.LabelFrame(master=self.LowerFrame, bg=self.background, fg=self.foreground,
                                     text="Brush:", font=self.font)
        self.Toolbox.pack(side="right", anchor="s", expand=0, fill="y")

        self.CurrentCoord = tk.Label(master=self.InfoBox, text="Char: 0 | 0x00", bg=self.background,
                                     foreground=self.foreground, font=self.font)
        self.CurrentCoord.pack()

        self.Draw = DrawBox(master=self.DrawFrame, bg=self.background, size=self.Size.get(), mode=self.Mode,
                            background=self.draw_off, foreground=self.draw_on)
        self.Draw.pack()

        # Brush Options

        self.Brush_White = tk.Radiobutton(master=self.Toolbox, variable=self.BrushVar, value=0, text="White",
                                          background=self.background, foreground=self.foreground,
                                          indicatoron=False, command=self.update_brush, font=self.font)
        self.Brush_Black = tk.Radiobutton(master=self.Toolbox, variable=self.BrushVar, value=1, text="Black",
                                          background=self.background, foreground=self.foreground,
                                          indicatoron=False, command=self.update_brush, font=self.font)
        self.Brush_Invert = tk.Radiobutton(master=self.Toolbox, variable=self.BrushVar, value=2, text="Invert",
                                           background=self.background, foreground=self.foreground,
                                           indicatoron=False, command=self.update_brush, font=self.font)
        self.Brush_Invert.pack(side="top", expand=1, fill="both")
        self.Brush_Black.pack(side="top", expand=1, fill="both")
        self.Brush_White.pack(side="top", expand=1, fill="both")

        # Options

        self.Invert_Button = tk.Button(master=self.Options, text="Invert", command=self.Draw.invert_screen,
                                       background=self.background, foreground=self.foreground, font=self.font)
        self.Clear_Button = tk.Button(master=self.Options, text="Clear", command=self.Draw.clear_screen,
                                      background=self.background, foreground=self.foreground, font=self.font)
        self.Apply_Button = tk.Button(master=self.Options, text="Apply", command=self.apply,
                                      background=self.background, foreground=self.foreground, font=self.font)
        self.Clear_Button.pack(side="top", expand=1, fill="both")
        self.Invert_Button.pack(side="top", expand=1, fill="both")
        self.Apply_Button.pack(side="bottom", expand=1, fill="both")

        self.Menu = tk.Menu(self)
        self.Menu_File = tk.Menu(self.Menu, tearoff=False)
        self.Menu_Options = tk.Menu(self.Menu, tearoff=False)
        self.Menu_Settings = tk.Menu(self.Menu, tearoff=False)
        self.Menu_Export = tk.Menu(self.Menu_File, tearoff=False)
        self.Menu_Help = tk.Menu(self.Menu, tearoff=False)

        self.Menu_File.add_command(label="New Window", accelerator="Control+N",
                                   command=lambda: self.start_project(False))
        self.Menu_File.add_command(label="New Project", accelerator="Shift+N",
                                   command=lambda: self.start_project(True))
        self.Menu_File.add_separator()
        self.Menu_File.add_command(label="Open Project", accelerator="Control+O", command=self.open)
        self.Menu_File.add_command(label="Save Project", accelerator="Control+S", command=self.save)
        self.Menu_File.add_command(label="Save Project As", accelerator="Control+Shift+S", command=self.save_as)
        self.Menu_File.add_separator()
        self.Menu_File.add_cascade(label="Export", menu=self.Menu_Export)
        self.Menu_File.add_separator()
        self.Menu_File.add_command(label="Close", accelerator="Control+Q", command=self.exit_protocol)

        self.Menu_Export.add_command(label="Assembler", accelerator="Control+E", command=lambda: self.export("asm"))
        self.Menu_Export.add_command(label="C Include", accelerator="Control+Shift+E", command=lambda: self.export("c"))
        self.Menu_Export.add_command(label="Raw Bytes", command=lambda: self.export("out"))

        """
        if len(self.File_Formats) > 0:
            self.Menu_Export.add_separator()
        for i in self.File_Formats:
            if len(i) > 3:
                self.Menu_Export.add_command(label=i.split(".")[0],
                                             command=partial(self.export, "custom", type_carry=i))
        """

        self.Menu_Options.add_command(label="Copy", accelerator="Control+C", command=self.copy)
        self.Menu_Options.add_command(label="Paste", accelerator="Control+V", command=self.paste)
        self.Menu_Options.add_separator()
        self.Menu_Options.add_command(label="Clear", command=self.Draw.clear_screen, accelerator="Control+X")
        self.Menu_Options.add_command(label="Invert", command=self.Draw.invert_screen, accelerator="Control+Y")
        self.Menu_Options.add_command(label="Apply", command=self.apply, accelerator="Control+A")

        self.Menu_Settings.add_checkbutton(label="Big Canvas", variable=self.Size, onvalue=32, offvalue=16,
                                           command=self.update_draw, accelerator="Control+Plus")
        self.Menu_Settings.add_checkbutton(label="Grid", variable=self.Grid, onvalue=1, offvalue=0,
                                           command=self.update_draw, accelerator="Control+G")
        self.Menu_Settings.add_checkbutton(label="Cursor Dragging", variable=self.Drag, onvalue=1, offvalue=0,
                                           command=self.update_draw)
        self.Menu_Settings.add_separator()
        self.Menu_Settings.add_checkbutton(label="Coordinate Hints", variable=self.Hint,
                                           onvalue=1, offvalue=0, command=self.update_draw)
        self.Menu_Settings.add_checkbutton(label="Cursor Wrapping", variable=self.Wrap,
                                           onvalue=1, offvalue=0)

        self.Menu_Help.add_command(label="Creating a Theme",
                                   command=lambda: FileViewer(self.Path + "/create_theme.txt"))
        # self.Menu_Help.add_command(label="Creating Custom Formats",
        #                            command=lambda: FileViewer(self.Path + "/format_help.txt"))
        # self.Menu_Help.add_command(label="Importing Custom Formats",
        #                            command=lambda: FileViewer(self.Path + "/create_format.txt"))
        self.Menu_Help.add_separator()
        self.Menu_Help.add_checkbutton(label="What is this?", variable=self.Tooltip)
        self.Menu_Help.add_command(label="About", command=self.about_menu)

        self.Menu.add_cascade(label="File", menu=self.Menu_File)
        self.Menu.add_cascade(label="Options", menu=self.Menu_Options)
        self.Menu.add_cascade(label="Settings", menu=self.Menu_Settings)
        self.Menu.add_cascade(label="Help", menu=self.Menu_Help)

        self["menu"] = self.Menu

        self.bind("<Left>", self.cursor)
        self.bind("<Right>", self.cursor)
        self.bind("<Up>", self.cursor)
        self.bind("<Down>", self.cursor)
        self.bind("<a>", self.cursor)
        self.bind("<d>", self.cursor)
        self.bind("<w>", self.cursor)
        self.bind("<s>", self.cursor)

        self.bind("<Return>", lambda _: self.apply())
        self.bind("<Control-a>", lambda _: self.apply())
        self.bind("<Control-y>", self.Draw.invert_screen)
        self.bind("<Control-x>", self.Draw.clear_screen)
        self.bind("<Control-g>", self.show_grid)

        self.bind("<Control-q>", self.exit_protocol)
        self.bind("<Control-o>", self.open)
        self.bind("<Control-s>", self.save)
        self.bind("<Control-Shift-s>", self.save_as)
        self.bind("<Control-n>", lambda _: self.start_project(False))
        self.bind("<Shift-n>", lambda _: self.start_project(True))
        self.bind("<Control-e>", lambda _: self.export("asm"))
        self.bind("<Control-Shift-E>", lambda _: self.export("c"))

        self.bind("<Control-plus>", self.extend_draw)
        self.bind("<Control-c>", self.copy)
        self.bind("<Control-v>", self.paste)

        ToolTip(self.Brush_White, "White Brush.\nDraws white on selected field")
        ToolTip(self.Brush_Black, "Black Brush.\nDraws black on selected field")
        ToolTip(self.Brush_Invert, "Inverted Brush.\nInverts the selected field")
        ToolTip(self.Invert_Button, "Invert Button.\nInverts the entire draw field")
        ToolTip(self.Clear_Button, "Clear Button.\nClears the entire draw field")
        ToolTip(self.Apply_Button, "Apply Button.\nSets the selected character \nto the edited character")
        ToolTip(self.CurrentCoord, "Coordinate Label.\nShows the index of selected \ncharacter in Decimal and Hex")
        ToolTip(self.DrawFrame, "Draw field.\nHere you can edit\nthe selected character")
        ToolTip(self.UpperFrame, "Character list.\nHere you select one of\n256 characters to edit")

        self.build_matrix()
        self.Draw.update_screen()
        self.update_draw()
        self.update_brush()

        if carry_file:
            self.open(in_file=carry_file)

    def exit_protocol(self, event=None):
        try:
            self.check_save_status()
            self.Preset = open(self.Path + "/settings/settings", "wb")
            self.Preset.write(self.Size.get().to_bytes(1, "big"))
            self.Preset.write(self.Grid.get().to_bytes(1, "big"))
            self.Preset.write(self.Drag.get().to_bytes(1, "big"))
            self.Preset.write(self.Wrap.get().to_bytes(1, "big"))
            self.Preset.write(self.Hint.get().to_bytes(1, "big"))

            self.Preset.close()
        except Exception as e:
            messagebox.showerror("Error", "Error while saving local settings:\n{0}".format(e))

        self.destroy()

    def save(self, event=None):
        if self.CurrentFile == "":
            name_raw = file.asksaveasfilename(confirmoverwrite=True, defaultextension=".bmf",  title="Save As",
                                              filetypes=(("BitMap File", '*.bmf'), ("Text File", "*.txt"),
                                                         ("All Files", "*.*")))
            name = open(name_raw, "wb")
        else:
            name = open(self.CurrentFile, "wb")

        if name:
            name.write(int(self.Mode).to_bytes(1, "big"))

            for y in range(16):
                for x in range(16):
                    for y_ in range(16):
                        bin_value = ""
                        for x_ in range(8):
                            bin_value += str(self.Matrix[y][x].Pixels[x_][y_])
                        name.write(int(bin_value, 2).to_bytes(1, "big"))

            self.CurrentFile = name.name
            self.modified(False)
            name.close()

    def save_as(self, event=None):
        self.CurrentFile = ""
        self.save()

    def open(self, event=None, in_file=None):
        self.check_save_status()

        if in_file:
            read = open(in_file, "rb")
        else:
            read_raw = file.askopenfilename(defaultextension=".bmf",
                                            filetypes=(("BitMap File", '*.bmf'),
                                                       ("Text File", "*.txt"),
                                                       ("All Files", "*.*")))
            read = open(read_raw, "rb")

        if read:
            read.read(1)
            for y in range(16):
                for x in range(16):
                    for y_ in range(16):
                        value = int.from_bytes(read.read(1), "big")
                        for x_ in range(8):
                            shift_val = bin(value)[2:].zfill(8)[x_:x_+1]
                            self.Matrix[y][x].Pixels[x_][y_] = int(shift_val)
                    self.select_grid(x, y)

            self.CurrentFile = read.name
            self.select_grid(0, 0)
            self.Draw.update_screen()
            self.modified(False)
            read.close()

    def export(self, mode, event=None):
        write_raw = file.asksaveasfilename(confirmoverwrite=False, defaultextension="." + mode, title="Export As",
                                           filetypes=((mode.upper(), "." + mode), ("All Files", "*.*")))
        if write_raw:
            write = open(write_raw, "w")
            if mode == "asm":
                write.write("{0}".format(os.path.basename(self.CurrentFile).split(".")[0]))
                # write.write("\n\t; 8x{0} Character Size | 256 Characters Total".format(8 * (self.Mode + 1)))
                for y in range(16):
                    for x in range(16):
                        write.write("\n \t.byte ")
                        buffer = ""
                        for y_ in range(8 * (self.Mode + 1)):
                            bin_value = ""
                            for x_ in range(8):
                                bin_value += str(self.Matrix[y][x].Pixels[x_][y_])
                            buffer += "$" + str(hex(int(bin_value, 2)))[2:].zfill(2).upper() + ", "
                        write.write(buffer[:len(buffer)-2])
                        write.write(" ;char 0x{0}, {1}".format(hex(x + y * 16)[2:].zfill(2).upper(), x + y * 16))
                write.write("{0}_end".format(os.path.basename(self.CurrentFile).split(".")[0]))

            elif mode == "c":
                write.write("// {0}".format(os.path.abspath(self.CurrentFile)))
                write.write("\n// 8x{0} Character Size | 256 Characters Total".format(8 * (self.Mode + 1)))
                write.write("\n{")
                for y in range(16):
                    for x in range(16):
                        write.write("\n \t")
                        for y_ in range(8 * (self.Mode + 1)):
                            bin_value = ""
                            for x_ in range(8):
                                bin_value += str(self.Matrix[y][x].Pixels[x_][y_])
                            write.write("0x" + str(hex(int(bin_value, 2)))[2:].zfill(2).upper() + ", ")
                        write.write(" //Char {0} ; {1}".format(hex(x + y * 16)[2:].zfill(2).upper(), x + y * 16))
                write.write("\n}")

            elif mode == "out":
                write = open(write_raw, "wb")
                for y in range(16):
                    for x in range(16):
                        for y_ in range(8 * (self.Mode + 1)):
                            bin_value = ""
                            for x_ in range(8):
                                bin_value += str(self.Matrix[y][x].Pixels[x_][y_])
                            write.write(int(bin_value, 2).to_bytes(1, "big"))

            write.close()

    def copy(self, event=None):
        self.Copy = []
        for y_ in range(16):
            bin_value = ""
            for x_ in range(8):
                bin_value += str(self.Matrix[self.Y_Select][self.X_Select].Pixels[x_][y_])
            self.Copy.append(int(bin_value, 2))

    def paste(self, event=None):
        for y in range(16):
            txt = str(bin(self.Copy[y]))[2:].zfill(8)
            for x in range(8):
                self.Matrix[self.Y_Select][self.X_Select].Pixels[x][y] = int(txt[x])
        self.select_grid(self.X_Select, self.Y_Select)

    def build_matrix(self):
        hex_count_y = 0
        for y in range(18):
            row = []
            hex_count_x = 0
            for x in range(18):
                if x == 0 or x == 17:
                    if y != 0 and y != 17:
                        txt = tk.Label(master=self.UpperFrame, text=str(hex(hex_count_y)).upper()[2:],
                                       bg=self.background, fg=self.foreground, font=self.font)
                        txt.grid(row=y, column=x)
                        if x != 17:
                            self.Y_Text.append(txt)
                        if x == 17:
                            hex_count_y += 1

                        ToolTip(txt, "Y Coordinate.\nThis is the first Hex digit\n>> 0xY0")

                elif y == 0 or y == 17:
                    if x != 0 and x != 17:
                        txt = tk.Label(master=self.UpperFrame, text=str(hex(hex_count_x)).upper()[2:],
                                       bg=self.background, fg=self.foreground, font=self.font)
                        txt.grid(row=y, column=x)
                        if x != 17:
                            self.X_Text.append(txt)
                        hex_count_x += 1

                        ToolTip(txt, "X Coordinate.\nThis is the second Hex digit\n>> 0x0X")
                else:
                    matrix = ImageBox(master=self.UpperFrame, bg=self.draw_off, height=24, width=24,
                                      relief="flat", bd=1, background=self.draw_off, foreground=self.draw_on)
                    matrix.grid(row=y, column=x)
                    matrix.bind("<Button-1>", partial(self.select_grid, x - 1, y - 1))
                    matrix.bind("<Button-2>", partial(self.select_grid, x - 1, y - 1))
                    matrix.bind("<Button-3>", partial(self.select_grid, x - 1, y - 1))
                    row.append(matrix)
            if y != 0:
                self.Matrix.append(row)

    def update_draw(self):
        for i in range(16):
            self.X_Text[i].config(bg=self.background, fg=self.foreground)
            self.Y_Text[i].config(bg=self.background, fg=self.foreground)

        self.Draw.Size = self.Size.get()
        self.Draw.config(height=self.Size.get() * 8, width=self.Size.get() * 8)
        self.Draw.Outline = self.Grid.get()
        self.Draw.Drag = self.Drag.get()
        self.select_grid(self.X_Select, self.Y_Select)

    def update_brush(self):
        self.Draw.Brush = self.BrushVar.get()

    def start_project(self, mode=None, event=None):
        if mode:
            self.check_save_status()
            self.destroy()
        os.system("python3 main.py")

    def modified(self, status):
        self.Draw.Modified = status
        self.title("Bitmap Editor - {0}".format(os.path.basename(self.CurrentFile)))
        if status:
            self.title("Bitmap Editor - {0} *".format(os.path.basename(self.CurrentFile)))

    def check_save_status(self):
        if self.Draw.Modified:
            if tk.messagebox.askyesno(message="Do you want to Save?"):
                self.save()

    def select_grid(self, x, y, event=None):
        if self.Hint.get():
            self.X_Text[self.X_Select].config(bg=self.background, fg=self.foreground)
            self.Y_Text[self.Y_Select].config(bg=self.background, fg=self.foreground)
            self.X_Text[x].config(bg=self.foreground, fg=self.background)
            self.Y_Text[y].config(bg=self.foreground, fg=self.background)

        if self.Draw.Applied:
            pass

        self.Matrix[self.Y_Select][self.X_Select].load(self.Draw.PixelGrid, mode=self.Mode)
        self.Draw.load(self.Matrix[y][x].Pixels)

        self.Matrix[self.Y_Select][self.X_Select].config(relief="flat")
        self.Matrix[y][x].config(relief="solid")
        self.X_Select, self.Y_Select = x, y

        hex_number = str(hex(y)[2:]) + str(hex(x)[2:])
        self.CurrentCoord.config(text="{0} | 0x{1}".format(int(hex_number, 16), hex_number.upper()))
        if event and event.num == 2 or event and event.num == 3:
            extern = tk.Toplevel(master=self, height=20, width=20)
            extern.resizable(False, False)
            extern.title("{0} | 0x{1}".format(int(hex_number, 16), hex_number.upper()))
            extern_canvas = tk.Canvas(master=extern, bg=self.draw_off, height=255, width=255, relief="solid", bd=1)
            extern_canvas.pack(expand=1, fill="both")

            for y in range(8 * (self.Mode + 1)):
                for x in range(8):
                    fill = self.draw_off
                    out = self.draw_on
                    if self.Matrix[self.Y_Select][self.X_Select].Pixels[x][y]:
                        fill = self.draw_on
                        out = self.draw_off
                    x_cord = x * 32
                    y_cord = y * 32 / (self.Mode + 1)
                    extern_canvas.create_rectangle(x_cord, y_cord, x_cord + 32, y_cord + 32 / (self.Mode + 1),
                                                   fill=fill, outline=out, width=0)

        self.Draw.update_screen()

    def apply(self):
        self.Draw.Applied = True
        self.Matrix[self.Y_Select][self.X_Select].load(self.Draw.PixelGrid, mode=self.Mode)
        self.modified(True)

    def show_grid(self, event):
        if self.Grid.get():
            self.Grid.set(0)
        else:
            self.Grid.set(1)
        self.update_draw()

    def extend_draw(self, event):
        if self.Size.get() == 32:
            self.Size.set(16)
        else:
            self.Size.set(32)
        self.update_draw()

    def cursor(self, event):
        x, y = self.X_Select, self.Y_Select
        if event.keysym == "Left" or event.keysym == "a":
            x -= 1
        elif event.keysym == "Right" or event.keysym == "d":
            x += 1
        elif event.keysym == "Up" or event.keysym == "w":
            y -= 1
        elif event.keysym == "Down" or event.keysym == "s":
            y += 1

        if x < 0:
            x = 15
            if self.Wrap.get():
                y -= 1
        if x > 15:
            x = 0
            if self.Wrap.get():
                y += 1
        if y > 15:
            y = 0
        if y < 0:
            y = 15
        self.select_grid(x, y)

    def about_menu(self):
        menu = tk.Toplevel(self)
        menu.resizable(False, False)
        menu.title("About")

        textbox = tk.Text(master=menu, height=10, width=30)
        textbox.insert("end", InfoText)
        textbox.config(state="disabled")
        textbox.pack(side="top")
        exit_button = tk.Button(master=menu, text="Exit", command=menu.destroy)
        exit_button.pack(side="bottom", expand=0, fill="x")

    def import_code(self, code):
        for i in code:
            if len(i) > 1:
                if i == "[end]":
                    break
                elif not i[0] == "#":
                    try:
                        exec(i)
                    except Exception as e:
                        print("Error while Importing Code: \n", e)


class FileViewer(tk.Tk):
    def __init__(self, path, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title(os.path.basename(path))

        self.ShowText = tk.Text(master=self, bg="#FFFFFF", height=32, width=160)
        self.ShowText.pack(side="top", expand=1, fill="both")

        tk.Button(master=self, text="Close", bg="#FFFFFF",
                  command=lambda: self.destroy()).pack(side="bottom", expand=0, fill="x")

        file_read = open(path, "r")
        for i in file_read.read():
            self.ShowText.insert("end", i)
        file_read.close()

        self.ShowText.config(state="disabled")


class ToolTip(object):
    def __init__(self, widget, text):
        widget.bind("<Enter>", self.showtip)
        widget.bind("<Leave>", self.hidetip)

        self.widget = widget
        self.text = text
        self.window = None
        self.id = None
        self.x = 0
        self.y = 0

    def showtip(self, event):
        if self.window or not self.text or not main.Tooltip.get():
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 57
        y += cy + self.widget.winfo_rooty() + 27

        self.window = tk.Toplevel(self.widget)
        self.window.overrideredirect(True)
        self.window.wm_geometry("+%d+%d" % (x, y))

        label = tk.Label(self.window, text=self.text, background="#FFFFE0", relief="solid", bd=1, justify="left")
        label.pack(ipadx=1)

    def hidetip(self, event):
        win = self.window
        self.window = None
        if win:
            win.destroy()


class DrawBox(tk.Canvas):
    def __init__(self, size, mode, background, foreground, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.background = background
        self.foreground = foreground
        self.Size = size
        self.Mode = mode
        self.X_coord = []
        self.Y_coord = []
        self.Brush = 0
        self.Outline = 1
        self.Drag = 1
        self.Modified = False
        self.Applied = False
        self.Previous_X = -1
        self.Previous_Y = -1
        self.PixelGrid = [[0 for _ in range(16)] for _ in range(8)]
        self.update_coord(size)

        self.config(height=size * 8 + 1, width=size * 8 + 1)
        self.bind("<B1-Motion>", lambda e: self.draw("motion", e))
        self.bind("<Button-1>", lambda e: self.draw("click", e))

    def update_coord(self, size):
        self.X_coord.clear()
        self.Y_coord.clear()
        for i in range(8):
            self.X_coord.append(i * size)
        for i in range((self.Mode + 1) * 8):
            self.Y_coord.append(int(i * (size / (self.Mode + 1))))

    def draw(self, click, event):
        ex = event.x - (self.Size / 2)  # Brush Cursor fine tune
        ey = event.y - (self.Size / (2 * (self.Mode + 1)))
        x = int(min(self.X_coord, key=lambda x_: abs(x_ - (ex - int(self.Size / 16)))) / self.Size)
        y = int((min(self.Y_coord, key=lambda y_: abs(y_ - (ey - int(self.Size / 16)))) /
                 (self.Size / 128) / (8 / (self.Size / 16)) / (self.Size / (self.Mode + 1))))
        if click == "click" or click == "motion" and self.Drag != 0:
            if self.Previous_X != x or self.Previous_Y != y or click == "click":
                if self.Brush == 2:
                    if self.PixelGrid[x][y]:
                        self.PixelGrid[x][y] = 0
                    else:
                        self.PixelGrid[x][y] = 1
                elif self.Brush:
                    self.PixelGrid[x][y] = 1
                else:
                    self.PixelGrid[x][y] = 0
                self.update_screen()
        self.Previous_X, self.Previous_Y = x, y

    def update_screen(self):
        self.delete("all")
        for y in range(8 * (self.Mode + 1)):
            for x in range(8):
                fill = self.background
                out = self.foreground
                if self.PixelGrid[x][y]:
                    fill = self.foreground
                    out = self.background
                x_cord = x * self.Size
                y_cord = y * self.Size / (self.Mode + 1)
                self.create_rectangle(x_cord, y_cord, x_cord + self.Size, y_cord + self.Size / (self.Mode + 1),
                                      fill=fill, outline=out, width=self.Outline)

    def clear_screen(self, event=None):
        for y in range(8 * (self.Mode + 1)):
            for x in range(8):
                self.PixelGrid[x][y] = 0
        self.update_screen()

    def invert_screen(self, event=None):
        for y in range(8 * (self.Mode + 1)):
            for x in range(8):
                if self.PixelGrid[x][y]:
                    self.PixelGrid[x][y] = 0
                else:
                    self.PixelGrid[x][y] = 1
        self.update_screen()

    def load(self, carry):
        self.PixelGrid = carry


class ImageBox(tk.Canvas):
    def __init__(self, background, foreground, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.background = background
        self.foreground = foreground
        self.Pixels = [[0 for _ in range(16)] for _ in range(8)]

    def load(self, bitmap, mode):
        # self.Pixels = bitmap
        self.delete("all")
        for y in range((mode + 1) * 8):
            for x in range(8):
                fill_color = self.background
                if bitmap[x][y]:
                    fill_color = self.foreground
                self.create_rectangle(x * 3 + 2, (y * 3 + 2) / (mode + 1) + mode,
                                      x * 3 + 5, (y * 3 + 5) / (mode + 1) + mode,
                                      fill=fill_color, width=0)


class StartupDialog(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.exit_protocol)

        self.closed = False
        self.file = None
        self.ProjectSize = tk.IntVar()

        self.Button_Frame = tk.LabelFrame(master=self, text="Character Size:", bg="#FFFFFF")
        self.Button_Frame.pack(side="left", fill="both", expand=0)

        self.Action_Frame = tk.Frame(master=self, bg="#FFFFFF")
        self.Action_Frame.pack(side="right", fill="both", expand=0)

        self.Button_8 = tk.Radiobutton(master=self.Button_Frame, variable=self.ProjectSize, value=0,
                                       text="8x8 Pixels", bg="#FFFFFF", justify="center")
        self.Button_16 = tk.Radiobutton(master=self.Button_Frame, variable=self.ProjectSize, value=1,
                                        text="8x16 Pixels", bg="#FFFFFF", justify="center")

        self.Continue_Button = tk.Button(master=self, text="Open", bg="#FFFFFF", command=self.destroy, width=15)
        self.Cancel_Button = tk.Button(master=self, text="Cancel", bg="#FFFFFF", command=self.exit_protocol)
        self.Open_Button = tk.Button(master=self, text="Open File", bg="#FFFFFF", command=self.fileopen)

        self.File_Label = tk.Label(master=self, text="File: None\nNew Blank File", bg="#FFFFFF", justify="left")

        self.Button_8.pack(side="top", expand=1, fill="both")
        self.Button_16.pack(side="bottom", expand=1, fill="both")

        self.Cancel_Button.pack(side="bottom", expand=1, fill="x", padx=2, pady=2)
        self.Continue_Button.pack(side="bottom", expand=1, fill="x", padx=2, pady=2)
        self.Open_Button.pack(side="top", expand=1, fill="x", padx=2, pady=2)
        self.File_Label.pack(side="top", anchor="w", padx=2, pady=2)

        self.Continue_Button.focus()

        self.bind("<Return>", lambda _: self.destroy())
        self.bind("<Control-o>", self.fileopen)
        self.bind("<Escape>", self.exit_protocol)

    def exit_protocol(self, event=None):
        self.closed = True
        self.destroy()

    def fileopen(self, event=None):
        self.file = file.askopenfilename(defaultextension=".bmf", filetypes=(("BitMap File", '*.bmf'),
                                                                             ("Text File", "*.txt"),
                                                                             ("All Files", "*.*")))
        if self.file:
            read = open(self.file, "rb")
            if int.from_bytes(read.read(1), "big") == 1:
                self.ProjectSize.set(1)
            else:
                self.ProjectSize.set(0)

            self.File_Label.config(text="File: {0}\nDetected Size: {1}x{2}".
                                   format(os.path.basename(self.file), 8, (self.ProjectSize.get() + 1) * 8))

            read.close()
        else:
            self.File_Label.config(text="File: None\nNew Blank File")
            self.file = None


if __name__ == "__main__":
    selector = StartupDialog()
    selector.config(bg="#FFFFFF")
    selector.title("Project Selector")
    selector.resizable(False, False)
    selector.mainloop()

    if not selector.closed:
        main = Main(mode=selector.ProjectSize.get(), carry_file=selector.file)  # Mode: 0 = 8x8 | 1 = 8x16
        main.resizable(False, False)
        main.title("Bitmap Editor")
        main.mainloop()
