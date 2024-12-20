import asyncio
import os
import tkinter as tk
from tkinter import ttk, messagebox
from concurrent.futures import ThreadPoolExecutor
import winsound

from device_manager import DeviceManager
from file_manager import FileManager
from utils import Utils


popup_open = False
executor = ThreadPoolExecutor(max_workers=1)

class DeviceUI:
    def __init__(self, root):
        self.root = root
        self.device_manager = DeviceManager(self)
        self.file_manager = FileManager(self)
        self.utils = Utils()
        self.retain_state = tk.BooleanVar(value=self.load_checkbox_state())
        self.create_widgets()
        self.create_menu()
        self.file_manager.load_devices()

    def load_checkbox_state(self):
        """Load the checkbox state from a file."""
        if os.path.exists("checkbox_state.txt"):
            with open("checkbox_state.txt", "r") as f:
                return f.read() == "1"
        return False

    def save_checkbox_state(self):
        """Save the current checkbox state to a file."""
        with open("checkbox_state.txt", "w") as f:
            f.write(str(int(self.retain_state.get())))

    def create_widgets(self):
        """Create the main UI components."""
        self.create_checkbox()
        self.create_table()
        self.create_buttons()
        self.create_scrollbars()

    def create_checkbox(self):
        """Create a checkbox to retain state."""
        checkbox = tk.Checkbutton(self.root, text="Retain Previous State", variable=self.retain_state,
                                   command=self.save_checkbox_state)
        checkbox.grid(row=0, column=3, sticky='ne', padx=10, pady=10)  # Position at the top-right

    def create_table(self):
        """Create the device table."""
        self.table = ttk.Treeview(self.root, columns=("Controller ID", "Device ID", "Mode", "Weight", "Status"),
                                   show="headings")
        self.table.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        # Configure columns
        for col in ("Controller ID", "Device ID", "Mode", "Weight", "Status"):
            self.table.heading(col, text=col)
            self.table.column(col, anchor='center')

        # Bind copy event
        self.table.bind("<Button-3>", self.utils.copy_cell_content)

    def create_scrollbars(self):
        """Create scrollbars for the table."""
        vsb = ttk.Scrollbar(self.root, orient="vertical", command=self.table.yview)
        vsb.grid(row=1, column=4, sticky='ns')
        self.table.configure(yscrollcommand=vsb.set)

        # hsb = ttk.Scrollbar(self.root, orient="horizontal", command=self.table.xview)
        # hsb.grid(row=2, column=0, columnspan=4, sticky='ew')
        # self.table.configure(xscrollcommand=hsb.set)

    def create_buttons(self):
        """Create buttons for device actions."""
        tk.Button(self.root, text="Add Device", command=self.open_add_device_popup).grid(
            row=2, column=0, padx=10, pady=10, sticky='ew')
        tk.Button(self.root, text="Connect All", command=self.device_manager.connect_all_devices).grid(
            row=2, column=1, padx=10, pady=10, sticky='ew')
        tk.Button(self.root, text="Disconnect All", command=self.device_manager.disconnect_all_devices).grid(
            row=2, column=2, padx=10, pady=10, sticky='ew')
        tk.Button(self.root, text="Close", command=self.root.quit).grid(
            row=2, column=3, padx=10, pady=10, sticky='ew')

    def create_menu(self):
        """Create the menu bar."""
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.open_add_device_popup)
        file_menu.add_command(label="Load", command=self.file_manager.load_file)
        file_menu.add_command(label="Save", command=self.file_manager.save_devices)
        # Uncomment to enable "Save As" functionality
        # file_menu.add_command(label="Save As", command=self.device_manager.save_as)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    # Function to open the Add Device popup window
    def open_add_device_popup(self):
        global popup_open

        if popup_open:
            # add_device_popup.bell()  # Beep sound (for all platforms)
            winsound.Beep(1000, 500)  # Windows beep (frequency, duration in ms)
            messagebox.showwarning("Warning", "A popup is already open!")
            return

        popup_open = True

        def toggle_wifi_fields():
            if connection_mode.get() == "WiFi":
                ssid_entry.config(state='normal')
                password_entry.config(state='normal')
            else:
                ssid_entry.config(state='disabled')
                password_entry.config(state='disabled')

        def on_close():
            global popup_open
            popup_open = False
            add_device_popup.destroy()

        add_device_popup = tk.Toplevel(self.root)
        add_device_popup.title("Add Device")
        add_device_popup.protocol("WM_DELETE_WINDOW", on_close)

        # Device info fields across two columns
        tk.Label(add_device_popup, text="Controller ID").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        controller_id_entry = tk.Entry(add_device_popup)
        controller_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew', columnspan=2)

        tk.Label(add_device_popup, text="Device ID").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        device_id_entry = tk.Entry(add_device_popup)
        device_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew', columnspan=2)

        tk.Label(add_device_popup, text="Capacity").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        capacity_entry = tk.Entry(add_device_popup)
        capacity_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew', columnspan=2)

        tk.Label(add_device_popup, text="Mode of Connection").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        connection_mode = tk.StringVar(value="WiFi")
        wifi_radio = tk.Radiobutton(add_device_popup, text="WiFi", variable=connection_mode, value="WiFi",
                                    command=toggle_wifi_fields)
        wifi_radio.grid(row=3, column=1, padx=10, pady=5, sticky='w')
        bluetooth_radio = tk.Radiobutton(add_device_popup, text="Bluetooth", variable=connection_mode,
                                         value="Bluetooth", command=toggle_wifi_fields)
        bluetooth_radio.grid(row=3, column=2, padx=10, pady=5, sticky='w')

        tk.Label(add_device_popup, text="SSID").grid(row=4, column=0, padx=10, pady=5, sticky='w')
        ssid_entry = tk.Entry(add_device_popup)
        ssid_entry.grid(row=4, column=1, padx=10, pady=5, sticky='ew', columnspan=2)

        tk.Label(add_device_popup, text="Password").grid(row=5, column=0, padx=10, pady=5, sticky='w')
        password_entry = tk.Entry(add_device_popup, show="*")
        password_entry.grid(row=5, column=1, padx=10, pady=5, sticky='ew', columnspan=2)

        tk.Label(add_device_popup, text="Tray Weight").grid(row=6, column=0, padx=10, pady=5, sticky='w')
        tray_weight_entry = tk.Entry(add_device_popup)
        tray_weight_entry.grid(row=6, column=1, padx=10, pady=5, sticky='ew', columnspan=2)

        tk.Label(add_device_popup, text="Tolerance").grid(row=7, column=0, padx=10, pady=5, sticky='w')
        tolerance_entry = tk.Entry(add_device_popup)
        tolerance_entry.grid(row=7, column=1, padx=10, pady=5, sticky='ew', columnspan=2)

        tk.Label(add_device_popup, text="Stock Name").grid(row=8, column=0, padx=10, pady=5, sticky='w')
        stock_name_entry = tk.Entry(add_device_popup)
        stock_name_entry.grid(row=8, column=1, padx=10, pady=5, sticky='ew', columnspan=2)

        tk.Label(add_device_popup, text="Single Stock Weight").grid(row=9, column=0, padx=10, pady=5, sticky='w')
        single_stock_weight_entry = tk.Entry(add_device_popup)
        single_stock_weight_entry.grid(row=9, column=1, padx=10, pady=5, sticky='ew', columnspan=2)

        # Using a thread pool to run the async function
        def add_device_wrapper():
            asyncio.run(self.device_manager.add_device(controller_id_entry.get(), device_id_entry.get(), connection_mode.get()))

        tk.Button(add_device_popup, text="Add Device", command=lambda: executor.submit(add_device_wrapper)).grid(row=10,
                                                                                                                 column=0,
                                                                                                                 padx=10,
                                                                                                                 pady=10,
                                                                                                                 sticky='ew')
        tk.Button(add_device_popup, text="Cancel", command=on_close).grid(row=10, column=1, padx=10, pady=10,
                                                                          columnspan=2, sticky='ew')

        add_device_popup.grid_columnconfigure(0, weight=1)
        add_device_popup.grid_columnconfigure(1, weight=1)

        toggle_wifi_fields()

