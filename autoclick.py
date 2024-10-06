import tkinter as tk
from pynput.mouse import Listener, Button
from pynput.keyboard import Listener as KeyboardListener, Key


class AutoClickerModel:
    def __init__(self):
        self.recording = False

    def toggle_recording(self):
        self.recording = not self.recording
        return self.recording

    def stop_recording(self):
        self.recording = False
        return self.recording
    
    def reset(self):
        self.recording = False
    
class AutoClickerView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("AutoClicker")
        self.geometry("400x200")

        self.status_label = tk.Label(self, text="Recording: False")
        self.status_label.pack(pady=20)

        self.record_frame = tk.Frame(self)
        self.record_frame.pack(pady=10)

        self.controller.start_listeners()

        self.start_button = tk.Button(self.record_frame, text="Start Records", command=self.controller.start_records)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.record_frame, text="Stop Records", command=self.controller.stop_records)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(self.record_frame, text="Reset", command=self.controller.reset_records)
        self.reset_button.pack(side=tk.LEFT, padx=5)


    def update_status(self, status):
        self.status_label.config(text=f"Recording: {status}")

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
                status = self.model.toggle_recording()
                self.view.update_status(status)
            elif key.char == 'b':
                return False  # Stop the keyboard listener
        except AttributeError:
            pass

    def reset_records(self):
        self.stop_records()
        self.model.reset()
        self.view.update_status(self.model.recording)
        with open('clicks.txt', 'w') as f:
            f.truncate(0)


    def start_listeners(self):
        self.mouse_listener = Listener(on_click=self.on_click)
        self.keyboard_listener = KeyboardListener(on_press=self.on_press)
        self.keyboard_listener.start()


    def stop_listeners(self):
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        self.view.update_status(self.model.stop_recording())

    def start_records(self):
        self.model.toggle_recording()
        self.view.update_status(self.model.recording)

        if self.model.recording:
            self.start_listeners()
            self.mouse_listener.start()
        else:
            self.stop_records()

    def stop_records(self):
        self.stop_listeners()


if __name__ == "__main__":
    model = AutoClickerModel()
    controller = AutoClickerController(model, None)
    view = AutoClickerView(controller=controller)
    controller.view = view
    view.mainloop()

