self.write_mode = "w"
self.file_extension = ".rs"
self.start_symbol = "{\n"
self.end_symbol = "}"
self.value = hex(value)
self.index = hex(index)
self.text_body = "    .byte ${value}, ${value}, ${value}, ${value}  ; Char: ${index}\n"


[end]
