import tkinter as tk

from ble_device import BLEDevice
import asyncio
import os

class DeviceManager:
    def __init__(self, ui):
        self.ui = ui

    def update_table_weight(self, device_address, weight):
        # Loop through the table rows and update the corresponding device's weight
        for child in self.ui.table.get_children():
            values = list(self.ui.table.item(child, "values"))
            if values[0] == device_address:  # Assuming Controller ID is device_address
                values[3] = weight  # Assuming weight is the 4th column
                values[4] = "Connected"
                self.ui.table.item(child, values=values)
                break

    # Function to add device and store data in a file
    async def add_device(self, controller_id, device_id, mode_of_connection):
        self.ui.table.insert("", "end", values=(controller_id, device_id, mode_of_connection, "--", "Connecting..."))

        # Save the device info to a text file
        # with open(DATA_FILE, "a") as file:
        #     file.write(f"{controller_id},{device_id},{mode_of_connection},Weight,Connected\n")

        if mode_of_connection == "Bluetooth":
            controller_id = "7C:DF:A1:EE:D0:35"
            url = 'https://hicoresoft.pythonanywhere.com/machines'
            uuid = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
            ble_device = BLEDevice(controller_id, uuid, url, self.update_table_weight)
            try:
                await ble_device.run()
            finally:
                await ble_device.disconnect()

    def connect_all_devices(self):
        # Logic for connecting all devices
        for child in self.ui.table.get_children():
            values = list(self.ui.table.item(child, "values"))
            values[4] = "Connected"
            self.ui.table.item(child, values=values)

    def disconnect_all_devices(self):
        # Logic for disconnecting all devices
        for child in self.ui.table.get_children():
            values = list(self.ui.table.item(child, "values"))
            values[4] = "Disconnected"
            self.ui.table.item(child, values=values)



