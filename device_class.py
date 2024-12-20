

class Device:
    def connect(self):
        raise NotImplementedError("Subclasses should implement this!")

    def disconnect(self):
        raise NotImplementedError("Subclasses should implement this!")

    def write_data(self, value):
        raise NotImplementedError("Subclasses should implement this!")


    def start_notifications(self):
        raise NotImplementedError("Subclasses should implement this!")

