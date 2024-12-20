import tkinter as tk
from tkinter import ttk
from ui import DeviceUI

def main():
    root = tk.Tk()
    root.title("Weight Machine Setup")

    # Initialize and run the UI
    app = DeviceUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
