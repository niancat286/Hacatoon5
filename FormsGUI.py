import tkinter as tk
from form_constructor import FormConstructor
from tkinter import messagebox, filedialog
from tkinter import Listbox, END

class FormsGUI:
    def  __init__(self, root):
        self.root = root
        self.root.title("Форма")
        self.form_constructor = None
        self.data_file = 'data.txt'
        self.build_menu()

    def build_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open file", command=self.open_form_file)
        file_menu.add_command(label="Close widget", command=self.root.quit)
        menubar.add_cascade(label="Menu", menu=file_menu)
        self.root.config(menu=menubar)


    def open_form_file(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
            if not file_path:
                return

            if hasattr(self, 'main_frame'):
                self.main_frame.destroy()

            self.main_frame = tk.Frame(self.root)
            self.main_frame.pack(padx=10, pady=10, fill='both', expand=True)

            self.form_constructor = FormConstructor(self.root, file_path)
            self.form_constructor.create_form(self.main_frame)

            button_frame = tk.Frame(self.main_frame)
            button_frame.pack(pady=10)

            tk.Button(button_frame, text="Далі", command=self.on_next).pack(side='left', padx=5)
            tk.Button(button_frame, text="Готово", command=self.on_done).pack(side='left', padx=5)
            tk.Button(button_frame, text="Відмінити", command=self.on_cancel).pack(side='left', padx=5)

        except Exception as e:
            messagebox.showerror("неочікувана помилка")

    def on_next(self):
        if self.form_constructor:
            self.save_data()
            self.form_constructor.clear_form()

    def on_done(self):
        if self.form_constructor:
            self.save_data()
            self.show_saved_data()
            self.root.quit()

    def on_cancel(self):
        if self.form_constructor:
            self.form_constructor.clear_form()

    def save_data(self):
        data = self.form_constructor.get_data()
        if any(val == "" for val in data):
            tk.messagebox.showwarning(message = "Будь ласка, заповніть усі поля.")
            return
        line = ",".join(f'"{value}"' for value in data)
        with open(self.data_file, "a", encoding="utf-8") as file:
            file.write(line + "\n")

    def show_saved_data(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Збережені записи")

        with open(self.data_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            tk.Label(new_window, text=line.strip()).pack(anchor='w', padx=10)

