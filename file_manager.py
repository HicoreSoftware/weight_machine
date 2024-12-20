from tkinter import messagebox, filedialog
import os


class FileManager:
    def __init__(self, ui):
        self.ui = ui
        self.data_file = "devices.txt"

    def save_devices(self):
        # Logic for saving devices to a file
        with open(self.data_file, "w") as file:
            for child in self.ui.table.get_children():
                values = self.ui.table.item(child, "values")
                file.write(",".join(values) + "\n")

    def load_file(self):
        # Logic for loading devices from a file
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.data_file = file_path
            self.load_devices()

    def load_devices(self):
        # Logic for loading devices from `self.data_file`
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                for line in file:
                    data = line.strip().split(',')
                    self.ui.table.insert("", "end", values=(data[0], data[1], data[2], data[3], data[4]))
