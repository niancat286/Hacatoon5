import tkinter as tk
from tkinter import Listbox, END


class FormConstructor():
    def __init__(self, parent, form_file):
        self.parent = parent
        self.form_file = form_file
        self.fields = []
        self.widgets = {}
        self.load_form()

    def load_form(self):
        with open(self.form_file, 'r', encoding='utf-8') as file:
            for line in file:
                name, field = line.strip().split(maxsplit=1)
                self.fields.append((name, field))

    def create_form(self, frame):
        for name, field_type in self.fields:
            label = tk.Label(frame, text=name)
            label.pack(anchor='w')

            if '()' in field_type:
                entry = tk.Entry(frame)
                entry.pack(fill='x')
                self.widgets[name] = entry

            elif '[' in field_type and ']' in field_type:
                options = field_type.strip('[]').split(',')
                listbox = Listbox(frame, exportselection=0, height=len(options))
                for opt in options:
                    listbox.insert(END, opt)
                listbox.pack()
                self.widgets[name] = listbox

    def get_data(self):
        data = []
        for name, widget in self.widgets.items():
            if isinstance(widget, tk.Entry):
                value = widget.get()
            elif isinstance(widget, Listbox):
                selections = widget.curselection()
                value = ','.join([widget.get(i) for i in selections])
            data.append(f'"{value}"')
        return ','.join(data)

    def clear_form(self):
        for widget in self.widgets.values():
            if isinstance(widget, tk.Entry):
                widget.delete(0, END)
            elif isinstance(widget, Listbox):
                widget.selection_clear(0, END)
