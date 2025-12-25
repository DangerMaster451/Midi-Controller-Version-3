import tkinter as tk
import requests
import Midi


class MediaController(Midi.MidiAction):
    def __init__(self, window:tk.Tk) -> None:
        super().__init__("MediaController")
        
        self.allowed_midi_statuses:list[int]|None = [176, 144]
        self.allowed_midi_notes:list[int]|None = [64, 49, 51]
        self.allowed_midi_velocities:list[int]|None = None

        self.window = window

       
    def action(self, event:Midi.MidiEvent) -> None:
        if event.status == 176 and event.note == 64 and event.velocity == 0:
            r = requests.get("http://192.168.4.205:8000/togglePlayback")
        elif event.status == 144 and event.note == 49:
            r = requests.get("http://192.168.4.205:8000/prevTab")
        elif event.status == 144 and event.note == 51:
            r = requests.get("http://192.168.4.205:8000/nextTab")