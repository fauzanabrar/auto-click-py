import tkinter as tk
from pynput.mouse import Listener, Button
from pynput.keyboard import Listener as KeyboardListener, Key

class AutoClickerModel:
    def __init__(self):
        self.recording = False
        self.auto_clicker = False

    def toggle_recording(self):
        self.recording = not self.recording
        return self.recording

    def stop_recording(self):
        self.recording = False
        return self.recording
    
    def reset(self):
        self.recording = False
    
    def toggle_auto_clicker(self):
        self.auto_clicker = not self.auto_clicker
        return self.auto_clicker
    
class AutoClickerView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("AutoClicker")
        self.geometry("400x300")

        # Records
        self.status_label = tk.Label(self, text="Recording: False")
        self.status_label.pack(pady=20)

        self.record_frame = tk.Frame(self)
        self.record_frame.pack(pady=10)

        self.records_button = tk.Button(self.record_frame, text="Records", command=self.start_records)
        self.records_button.pack(side=tk.LEFT, padx=5)

        self.toggle_records_button = tk.Button(self.record_frame, text="Start", command=self.toggle_records, state=tk.DISABLED)
        self.toggle_records_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(self.record_frame, text="Reset", command=self.controller.reset_records)
        self.reset_button.pack(side=tk.LEFT, padx=5)


        # Auto Clicker
        self.auto_label = tk.Label(self, text="Auto Click: False")
        self.auto_label.pack(pady=20)

        self.auto_click_frame = tk.Frame(self)
        self.auto_click_frame.pack(pady=10)

        self.auto_click_button = tk.Button(self.auto_click_frame, text="Start Auto Clicker Listener", command=self.start_auto_clicker)
        self.auto_click_button.pack(side=tk.LEFT, padx=5)

        self.auto_click_toggle_button = tk.Button(self.auto_click_frame, text="Start", command=self.toggle_auto_clicker, state=tk.DISABLED)
        self.auto_click_toggle_button.pack(side=tk.LEFT, padx=5)

    def update_status(self, status):
        self.status_label.config(text=f"Recording: {status}")
    
    def start_records(self):
        self.controller.start_records_listener()
        if self.controller.model.recording:
            self.toggle_records_button.config(state=tk.NORMAL)
        else:
            self.toggle_records_button.config(state=tk.DISABLED)

    def toggle_records(self):
        self.controller.toggle_records()
        self.toggle_records_button.config(text="Stop" if self.controller.model.recording else "Start")

    def update_auto_clicker(self, status):
        self.auto_label.config(text=f"Auto Click: {status}")

    def start_auto_clicker(self):
        self.controller.start_auto_clicker_listener()
        if self.controller.model.auto_clicker:
            self.auto_click_toggle_button.config(state=tk.NORMAL)
        else:
            self.auto_click_toggle_button.config(state=tk.DISABLED)

    def toggle_auto_clicker(self):
        self.controller.toggle_auto_clicker()
        self.auto_click_toggle_button.config(text="Stop" if self.controller.model.auto_clicker else "Start")

class AutoClickerController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.mouse_listener = None
        self.keyboard_listener = None

    def on_click(self, x, y, button, pressed):
        if self.model.recording and pressed and button == Button.left:
            with open('clicks.txt', 'a') as f:
                f.write(f'{x} {y}\n')

    def on_press(self, key):
        try:
            if key.char == 'a':
                if self.model.auto_clicker:
                    self.toggle_auto_clicker()
                if self.model.recording:
                    self.toggle_records()
            elif key.char == 'b':
                self.stop_listeners()
        except AttributeError:
            pass

    def click(self, x, y):
        pass

    
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
        self.view.update_status(self.model.recording)
        with open('clicks.txt', 'w') as f:
            f.truncate(0)

    def start_records_listener(self):
        if self.model.recording:
            self.stop_listeners()
        else:
            self.start_listeners()
        self.view.update_status(self.model.toggle_recording())

    def toggle_records(self):
        self.model.toggle_recording()

    # Auto Clicker
    def start_auto_clicker_listener(self):
        if self.model.auto_clicker:
            self.stop_listeners()
        else:
            self.start_listeners()
        self.view.update_auto_clicker(self.model.toggle_auto_clicker())

    def toggle_auto_clicker(self):
        self.model.toggle_auto_clicker()


if __name__ == "__main__":
    model = AutoClickerModel()
    controller = AutoClickerController(model, None)
    view = AutoClickerView(controller=controller)
    controller.view = view
    view.mainloop()

