import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os


def open_form_file(self):
    file_path = filedialog.askopenfilename(
        title="Виберіть файл форми",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if file_path:
        try:
            elements = self.form_constructor.parse_form_file(file_path)

            if elements:
                self.form_constructor.create_form(elements)
                self.toggle_buttons(True)
            else:
                messagebox.showerror("Помилка обробки файлу")

        except Exception as e:
            messagebox.showerror("неочікувана помилка")

