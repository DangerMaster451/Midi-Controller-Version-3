import tkinter as tk
from tkinter import ttk, Toplevel

class MidiEvent():
    def __init__(self, event) -> None:
        self.status = event[0][0]
        self.note = event[0][1]
        self.velocity = event[0][2]

class MidiAction():
    def __init__(self, name:str, allowed_midi_statuses:list[int]|None = None, allowed_midi_notes:list[int]|None = None, allowed_midi_velocities:list[int]|None = None):
        self.name = name
        self.allowed_midi_statuses:list[int]|None = allowed_midi_statuses
        self.allowed_midi_notes:list[int]|None = allowed_midi_notes
        self.allowed_midi_velocities:list[int]|None = allowed_midi_velocities

    def verify(self, event:MidiEvent) -> bool:
        if self.allowed_midi_statuses != None and event.status not in self.allowed_midi_statuses:
            return False
        if self.allowed_midi_notes != None and event.note not in self.allowed_midi_notes:
            return False
        if self.allowed_midi_velocities != None and event.velocity not in self.allowed_midi_velocities:
            return False
        return True

    def action(self, event:MidiEvent):
        pass

class Timer(MidiAction):
    def __init__(self, window:tk.Tk):
        self.name = "timer"
        super().__init__(self.name)
        
        self.allowed_midi_statuses:list[int]|None = [176]
        self.allowed_midi_notes:list[int]|None = [74]
        self.allowed_midi_velocities:list[int]|None = None

        self.window = tk.Toplevel(window)
        self.window.title("Timer")
        #self.window.withdraw()

        self.label = tk.Label(self.window, text="Timer", anchor=tk.CENTER)
        self.label.pack(pady=10)

        self.progressbar = ttk.Progressbar(self.window, length=400)
        self.progressbar["maximum"] = 90
        self.progressbar["value"] = 45
        self.progressbar.pack(padx=20, pady=20)
    
    def action(self, event:MidiEvent):
        self.progressbar["value"] = event.velocity
        