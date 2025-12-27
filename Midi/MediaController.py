from typing import Literal
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

        self.__window = tk.Toplevel(window)
        self.__window.title("Server Connection Monitor")
        self.__window.geometry("500x500")

        self.listBox = tk.Listbox(self.__window, height=300, width=50)
        self.listBox.yview()
        self.listBox.pack(pady=10)

        self.url = f"{config.server_ip}:{config.server_port}"

        self.fails = 0
        self.failThreshold = config.failThreshold
        self.givenUp = False

        self.__window.withdraw()
        
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
    
    def log(self, message:str, type:Literal["INFO", "WARNING", "ERROR"]):
        self.__window.deiconify()
        self.listBox.insert(self.listBox.size(), message)
        self.listBox.see(self.listBox.size())
        if type == "INFO":
            self.listBox.itemconfig(self.listBox.size()-1, {"fg":"black"})
        elif type == "WARNING":
            self.listBox.itemconfig(self.listBox.size()-1, {"fg":"#ED9121"})
        elif type == "ERROR":
            self.listBox.itemconfig(self.listBox.size()-1, {"fg":"red"})

    def sendRequest(self, page):
        def thread():
            self.log(f"Making request to {page}...", "INFO")
            while True:
                try:
                    r = requests.get(f"{self.url}/{page}")
                    self.log(f"Success", "INFO")
                    self.fails = 0
                    break
                except requests.exceptions.ConnectTimeout:
                    print()
                    self.log(f"Failed to make request, trying {self.failThreshold - self.fails} more times...", "WARNING")
                    self.fails += 1
                if self.fails >= self.failThreshold:
                    self.givenUp = True
                    self.log("I've Given Up :'(", "ERROR")
                    break
            self.log("Thread Complete", "INFO")

        t = threading.Thread(target=thread)
        t.start()
