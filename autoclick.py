import tkinter as tk
from tkinter import messagebox
from pynput.mouse import Listener, Button, Controller
from pynput.keyboard import Listener as KeyboardListener, Key
import time
import threading

class AutoClickerModel:
    def __init__(self):
        self.records_listener = False
        self.records = False
        self.auto_clicker_listener = False
        self.auto_clicker = False

    def start_records_listener(self):
        self.records_listener = not self.records_listener
        return self.records_listener

    def toggle_records(self):
        self.records = not self.records
        return self.records

    def stop_records(self):
        self.records = False
        return self.records
    
    def reset(self):
        self.records = False

    def start_auto_clicker_listener(self):
        self.auto_clicker_listener = not self.auto_clicker_listener
        return self.auto_clicker_listener

    def toggle_auto_clicker(self):
        self.auto_clicker = not self.auto_clicker
        return self.auto_clicker
    
class AutoClickerView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("AutoClicker")
        self.geometry("400x400")
        self.configure(bg="#2c3e50")

        # Title Label
        self.title_label = tk.Label(self, text="AutoClicker", font=("Helvetica", 18, "bold"), bg="#2c3e50", fg="#ecf0f1")
        self.title_label.pack(pady=20)

        # Records Section
        self.records_frame = tk.LabelFrame(self, text="Records", padx=10, pady=10, bg="#34495e", fg="#ecf0f1", font=("Helvetica", 12, "bold"))
        self.records_frame.pack(pady=10, fill="x", padx=20)

        self.status_label = tk.Label(self.records_frame, text="Status: False", bg="#34495e", fg="#ecf0f1", font=("Helvetica", 10))
        self.status_label.pack(pady=5)

        self.records_button_frame = tk.Frame(self.records_frame, bg="#34495e")
        self.records_button_frame.pack(pady=5)

        self.records_button = tk.Button(self.records_button_frame, text="Start Listener", command=self.controller.start_records_listener, bg="#1abc9c", fg="#ecf0f1", font=("Helvetica", 10, "bold"), padx=8, pady=5)
        self.records_button.pack(side=tk.LEFT, padx=5)

        self.toggle_records_button = tk.Button(self.records_button_frame, text="Start", command=self.controller.toggle_records, state=tk.DISABLED, bg="#e67e22", fg="#ecf0f1", font=("Helvetica", 10, "bold"), padx=8, pady=5)
        self.toggle_records_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(self.records_button_frame, text="Reset", command=self.confirm_reset, bg="#d35400", fg="#ecf0f1", font=("Helvetica", 10, "bold"), padx=8, pady=5)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Auto Clicker Section
        self.auto_clicker_frame = tk.LabelFrame(self, text="Auto Clicker", padx=10, pady=10, bg="#34495e", fg="#ecf0f1", font=("Helvetica", 12, "bold"))
        self.auto_clicker_frame.pack(pady=10, fill="x", padx=20)

        self.auto_label = tk.Label(self.auto_clicker_frame, text="Status: False", bg="#34495e", fg="#ecf0f1", font=("Helvetica", 10))
        self.auto_label.pack(pady=5)

        self.auto_click_button_frame = tk.Frame(self.auto_clicker_frame, bg="#34495e")
        self.auto_click_button_frame.pack(pady=5)

        self.auto_click_button = tk.Button(self.auto_click_button_frame, text="Start Listener", command=self.controller.start_auto_clicker_listener, bg="#1abc9c", fg="#ecf0f1", font=("Helvetica", 10, "bold"), padx=8, pady=5)
        self.auto_click_button.pack(side=tk.LEFT, padx=5)

        self.auto_click_toggle_button = tk.Button(self.auto_click_button_frame, text="Start", command=self.controller.toggle_auto_clicker, state=tk.DISABLED, bg="#e67e22", fg="#ecf0f1", font=("Helvetica", 10, "bold"), padx=8, pady=5)
        self.auto_click_toggle_button.pack(side=tk.LEFT, padx=5)

        # Adding icons to buttons
        self.icon_start_listener = tk.PhotoImage(file="icons/icons8-record-32.png").subsample(2, 2)
        self.icon_toggle_start = tk.PhotoImage(file="icons/icons8-start-32.png").subsample(2, 2)
        self.icon_reset = tk.PhotoImage(file="icons/icons8-reset-64.png").subsample(2, 2)

        self.records_button.config(image=self.icon_start_listener, compound=tk.LEFT)
        self.toggle_records_button.config(image=self.icon_toggle_start, compound=tk.LEFT)
        self.reset_button.config(image=self.icon_reset, compound=tk.LEFT)

        self.icon_auto_start_listener = tk.PhotoImage(file="icons/icons8-record-32.png").subsample(2, 2)
        self.icon_auto_toggle_start = tk.PhotoImage(file="icons/icons8-start-32.png").subsample(2, 2)

        self.auto_click_button.config(image=self.icon_auto_start_listener, compound=tk.LEFT)
        self.auto_click_toggle_button.config(image=self.icon_auto_toggle_start, compound=tk.LEFT)
        # Ensure you have the icons in the specified paths or update the paths accordingly
        # You can use any icon images you prefer. Here are some example paths:
        # "path/to/start_listener_icon.png"
        # "path/to/toggle_start_icon.png"
        # "path/to/reset_icon.png"
        # "path/to/auto_start_listener_icon.png"
        # "path/to/auto_toggle_start_icon.png"

        # Example icons can be downloaded from websites like:
        # - https://www.flaticon.com/
        # - https://icons8.com/
        # - https://www.iconfinder.com/

        # Make sure to download the icons and place them in the correct paths.
        # Example icons can be downloaded from websites like:
        # - https://www.flaticon.com/
        # - https://icons8.com/
        # - https://www.iconfinder.com/

        # Make sure to download the icons and place them in the correct paths.
    def update_status(self, status):
        self.status_label.config(text=f"Status : {status}")
    
    def start_records(self):
        if self.controller.model.records_listener:
            self.toggle_records_button.config(state=tk.NORMAL)
        else:
            self.toggle_records_button.config(state=tk.DISABLED)

    def confirm_reset(self):
        confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset?")
        if confirm:
            self.controller.reset_records()

    def toggle_records(self):
        self.toggle_records_button.config(text="Stop" if self.controller.model.records else "Start")

    def update_auto_clicker(self, status):
        self.auto_label.config(text=f"Status : {status}")

    def start_auto_clicker(self):
        if self.controller.model.auto_clicker_listener:
            self.auto_click_toggle_button.config(state=tk.NORMAL)
        else:
            self.auto_click_toggle_button.config(state=tk.DISABLED)

    def toggle_auto_clicker(self):
        self.auto_click_toggle_button.config(text="Stop" if self.controller.model.auto_clicker else "Start")

class AutoClickerController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.mouse_controller = Controller()
        self.mouse_listener = None
        self.keyboard_listener = None
        self.clicker_thread = None

    def on_click(self, x, y, button, pressed):
        if self.model.records and pressed and button == Button.left:
            with open('clicks.txt', 'a') as f:
                f.write(f'{x} {y}\n')

    def on_press(self, key):
        try:
            if key.char == 'a':
                if self.model.auto_clicker_listener:
                    self.toggle_auto_clicker()
                if self.model.records_listener:
                    self.toggle_records()
            elif key.char == 'b':
                self.stop_listeners()
                self.model.records_listener = False
                self.model.auto_clicker_listener = False
                self.model.records = False
                self.model.auto_clicker = False
                self.view.start_records()
                self.view.start_auto_clicker()
                self.view.update_status(self.model.records_listener)
                self.view.update_auto_clicker(self.model.auto_clicker_listener)
                self.view.toggle_records()
                self.view.toggle_auto_clicker()
                if self.clicker_thread is not None:
                    self.clicker_thread.stop()
                
        except AttributeError:
            pass

    def click(self):
        clicks = []
        with open('clicks.txt', 'r') as f:
            for line in f:
                x, y = line.split()
                clicks.append((int(x), int(y)))

        def auto_click():
            while self.model.auto_clicker:
                for x, y in clicks:
                    self.mouse_controller.position = (x, y)
                    self.mouse_controller.click(Button.left, 1)
                    time.sleep(0.5)

        self.clicker_thread = threading.Thread(target=auto_click)
        self.clicker_thread.start()
        
    
    def stop_listeners(self):
        if self.keyboard_listener is not None:
            self.keyboard_listener.stop()
        if self.mouse_listener is not None:
            self.mouse_listener.stop()

    def start_listeners(self):
        self.mouse_listener = Listener(on_click=self.on_click)
        self.keyboard_listener = KeyboardListener(on_press=self.on_press)
        self.keyboard_listener.start()
        self.mouse_listener.start()

    # Records
    def reset_records(self):
        self.stop_listeners()
        self.model.reset()
        self.view.update_status(self.model.records)
        with open('clicks.txt', 'w') as f:
            f.truncate(0)

    def start_records_listener(self):
        if self.model.records_listener:
            self.stop_listeners()
        else:
            self.start_listeners()
        self.view.update_status(self.model.start_records_listener())
        self.view.start_records()

    def toggle_records(self):
        self.model.toggle_records()
        self.view.toggle_records()

    # Auto Clicker
    def start_auto_clicker_listener(self):
        if self.model.auto_clicker_listener:
            self.stop_listeners()
        else:
            self.start_listeners()
        self.view.update_auto_clicker(self.model.start_auto_clicker_listener())
        self.view.start_auto_clicker()

    def toggle_auto_clicker(self):
        self.model.toggle_auto_clicker()
        self.view.toggle_auto_clicker()
        if self.model.auto_clicker:
            self.click()


if __name__ == "__main__":
    model = AutoClickerModel()
    controller = AutoClickerController(model, None)
    view = AutoClickerView(controller=controller)
    controller.view = view
    view.mainloop()

