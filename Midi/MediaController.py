import tkinter as tk
import requests
import threading
import Midi

class MediaController(Midi.MidiAction):
    def __init__(self, window:tk.Tk, config:Midi.Config) -> None:
        super().__init__("MediaController", config)
        
        self.allowed_midi_statuses:list[int]|None = [176, 144, 153]
        self.allowed_midi_notes:list[int]|None = [64, 49, 51, 36, 37, 38, 39, 40, 41, 42, 43, 70, 71]
        self.allowed_midi_velocities:list[int]|None = None

        self.window = window
        self.url = f"{config.server_ip}:{config.server_port}"

        self.fails = 0
        self.failThreshold = config.failThreshold
        self.givenUp = False
        
    def action(self, event:Midi.MidiEvent) -> None:
        if self.givenUp:
            return None
        if event.status == 176 and event.note == 64 and event.velocity == 0:
            self.sendRequest("/togglePlayback")
        elif event.status == 144 and event.note == 49:
            self.sendRequest("/prevTab")
        elif event.status == 144 and event.note == 51:
            self.sendRequest("/nextTab")
        elif event.status == 153 and event.note == 36:
            self.sendRequest("/hotkey1")
        elif event.status == 153 and event.note == 37:
            self.sendRequest("/hotkey2")
        elif event.status == 153 and event.note == 38:
            self.sendRequest("/hotkey3")
        elif event.status == 153 and event.note == 39:
            self.sendRequest("/hotkey4")
        elif event.status == 153 and event.note == 40:
            self.sendRequest("/hotkey5")
        elif event.status == 153 and event.note == 41:
            self.sendRequest("/hotkey6")
        elif event.status == 153 and event.note == 42:
            self.sendRequest("/hotkey7")
        elif event.status == 153 and event.note == 43:
            self.sendRequest("/hotkey8")
        return None

    def sendRequest(self, page:str):
        def thread():
            print(f"Making request to {page}...")
            while True:
                try:
                    r = requests.get(f"{self.url}/{page}")
                    print("Success")
                    self.fails = 0
                    break
                except requests.exceptions.ConnectTimeout:
                    print(f"Failed to make request, trying {self.failThreshold - self.fails} more times...")
                    self.fails += 1
                if self.fails >= self.failThreshold:
                    self.givenUp = True
                    print("I've given up :'(")
                    break
            print("Thread Complete")

        t = threading.Thread(target=thread)
        t.start()
