import asyncio
import requests
from bleak import BleakClient
from device_class import Device


class BLEDevice(Device):
    def __init__(self, device_address, uuid, url, update_weight_callback):
        super().__init__()
        self.device_address = device_address
        self.client = None
        self.uuid = uuid
        self.notification_handler = self.create_notification_handler()
        self.url = url
        self.update_weight_callback = update_weight_callback  # Add callback for UI update

    def create_notification_handler(self):
        def handler(sender, data):
            # id_dict = {
            #     sender: 1
            # }
            # decimal_values = [byte for byte in data[1:3]]
            # weight = sum(decimal_values)

            # # Data to be sent as JSON
            # payload = {
            #     "machine_id": id_dict[sender],
            #     "weight": weight
            # }

            # # Send POST request
            # response = requests.post(self.url, json=payload)

            # # Check the response
            # if response.status_code == 200:
            #     print("Success:", response.json())
            # else:
            #     print("Error:", response.status_code, response.text)

            # Assuming the weight data is extracted here, for example:
            weight = sum([byte for byte in data[1:5]])  # Example extraction logic

            # Call the UI update function
            if self.update_weight_callback:
                self.update_weight_callback(self.device_address, weight)

            print(f"Notification from {sender}: {data}, weight: {weight}")

        return handler

    async def connect(self):
        print(f"Trying to connect....   :  {self.device_address}")
        self.client = BleakClient(self.device_address)
        await self.client.connect()
        if self.client.is_connected:
            print(f"Connected to {self.device_address}")

    async def start_notifications(self):
        try:
            await self.client.start_notify(self.uuid, self.notification_handler)
            print("Started notifications")
        except Exception as e:
            print(f"Failed to handle notifications: {e}")

    async def write_data(self, value):
        try:
            await self.client.write_gatt_char(self.uuid, value)
            print("Written value:", value)
        except Exception as e:
            print(f"Failed to write: {e}")

    async def run(self):
        await self.connect()
        await self.start_notifications()

        # Writing data examples
        await self.write_data(bytearray([0xA1, 0x00, 0x00, 0x50, 0x10, 0x00, 0x00, 0x00]))
        await asyncio.sleep(3)
        await self.write_data(bytearray([0xBB, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
        await asyncio.sleep(10)
        await self.write_data(bytearray([0xC1, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))

        # Keep the program running to receive notifications
        # await asyncio.sleep(90)  # Adjust time as needed

    async def disconnect(self):
        await self.client.stop_notify(self.uuid)
        await self.client.disconnect()
        print("Disconnected")