import tkinker as tk


class FormConstructor():
    def __init__(self, form_file='file.txt', data_file='data.txt'):
        self.widg = {}
        self.field = []
        self.form_file = form_file
        self.data_file = data_file

    def load(self):
        try:
            with open(self.form_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        name, field = line.rsplit(' ', 1)
                        self.field.append((name, field))
        except FileNotFoundError:
            tk.messagebox.showerror("Помилка", f"Файл {self.form_file} не знайдено")
            self.field = []


    def create_form(self, container):
        for _, (name, field) in enumerate(self.field):
            label = tk.Label(container, text=name)
            label.grid(row=_, column=0)


            if field.startwith('[') and field.endswith(']'):
                options = field[1:-1].split(',')
                var = tk.StringVar()
                lb = tk.Listbox(container, height=len(options), exportselection=0)
                for opt in options:
                    lb.insert(tk.END, opt)
                lb.grid(row=_, column=1)
                lb.bind('<<ListboxSelect>>', lambda e, v=var, l=lb: self.on_select(e, v, l))
                self.widg[name] = (lb, var)
            else:
                entry = tk.Entry(container)
                entry.grid(row=_, column=1)
                self.widg[name] = (entry, None)


    def on_select(self, ev, var, listbox):
        pass

    def save_data(self):
        data = []
        for name, _ in self.field:
            widget, var = self.widg[name]
            if var:  # Якщо лістбоксік
                value = var.get()
            else: # Ентрішка
                value = widget.get()
            data.append(f'"{value}"')

        with open(self.data_file, 'a', encoding='utf-8') as f:
            f.write(','.join(data) + '\n')
        return data


    def clear_fields(self):
        for name, _ in self.field:
            widget, var = self.widg[name]
            if var:
                widget.selection_clear(0, tk.END)
                var.set('')
            else:
                widget.delete(0, tk.END)
