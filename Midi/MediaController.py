import tkinter as tk
import requests
import Midi


class MediaController(Midi.MidiAction):
    def __init__(self, window:tk.Tk, config:Midi.Config) -> None:
        super().__init__("MediaController", config)
        
        self.allowed_midi_statuses:list[int]|None = [176, 144, 153]
        self.allowed_midi_notes:list[int]|None = [64, 49, 51, 36, 37, 38, 39, 40, 41, 42, 43, 70, 71]
        self.allowed_midi_velocities:list[int]|None = None

        self.window = window
        self.url = f"{config.server_ip}:{config.server_port}"

    def action(self, event:Midi.MidiEvent) -> None:
        try:
            if event.status == 176 and event.note == 64 and event.velocity == 0:
                r = requests.get(f"{self.url}/togglePlayback")
            elif event.status == 144 and event.note == 49:
                r = requests.get(f"{self.url}/prevTab")
            elif event.status == 144 and event.note == 51:
                r = requests.get(f"{self.url}/nextTab")
            elif event.status == 153 and event.note == 36:
                r = requests.get(f"{self.url}/hotkey1")
            elif event.status == 153 and event.note == 37:
                r = requests.get(f"{self.url}/hotkey2")
            elif event.status == 153 and event.note == 38:
                r = requests.get(f"{self.url}/hotkey3")
            elif event.status == 153 and event.note == 39:
                r = requests.get(f"{self.url}/hotkey4")
            elif event.status == 153 and event.note == 40:
                r = requests.get(f"{self.url}/hotkey5")
            elif event.status == 153 and event.note == 41:
                r = requests.get("f{self.url}/hotkey6")
            elif event.status == 153 and event.note == 42:
                r = requests.get(f"{self.url}/hotkey7")
            elif event.status == 153 and event.note == 43:
                r = requests.get(f"{self.url}/hotkey8")
        except:
            pass