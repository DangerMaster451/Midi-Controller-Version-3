import tkinter as tk
import Midi
from tkinter import ttk, Toplevel
import random
from pygame import mixer
import time

class Timer(Midi.MidiAction):
    def __init__(self, window:tk.Tk, config:Midi.Config) -> None:
        super().__init__("timer", config)
        
        self.allowed_midi_statuses:list[int]|None = [176]
        self.allowed_midi_notes:list[int]|None = [74, 118]
        self.allowed_midi_velocities:list[int]|None = None

        self.maxTime = 90

        self.timeValue:int = 45
        self.timerRunning:bool = False

        self.__EASAlarm = mixer.Sound(config.EAS_sound_location)
        self.__normalAlarm = mixer.Sound(config.normal_sound_location)

        self.window = tk.Toplevel(window)
        self.window.title("Timer")
        self.window.withdraw()

        self.label = tk.Label(self.window, text="Timer", anchor=tk.CENTER)
        self.label.pack(pady=10)

        self.progressbar = ttk.Progressbar(self.window, length=400)
        self.progressbar["maximum"] = 90 * 60
        self.progressbar["value"] = 45
        self.progressbar.pack(padx=20, pady=20)

        self.window.protocol("WM_DELETE_WINDOW", self.window.withdraw)
    
    def action(self, event:Midi.MidiEvent) -> None:
        if event.note == 74:
            self.__handleKnob(event)
        if event.note == 118:
            self.__handleButton(event)
    
    def __handleKnob(self, event:Midi.MidiEvent) -> None:
        self.window.deiconify()
        if self.timerRunning:
            return None
        self.timeValue = self.__midiVelocityToTimeValue(event.velocity)
        self.progressbar["value"] = self.timeValue
        self.label["text"] = self.__convertTimeValueToString(self.timeValue)

    def __handleButton(self, event:Midi.MidiEvent) -> None:
        if self.timerRunning:
            self.window.withdraw()
            return None
        if self.timeValue == 0:
            mixer.pause()
            return None
        self.timerRunning = True
        self.timeValue -= 60
        self.progressbar["maximum"] = self.timeValue
        self.window.after(0, self.__timerTick)

    def __convertTimeValueToString(self, value:int) -> str:
        if self.timerRunning:
            return time.strftime("%H:%M:%S", time.gmtime(value))
        return time.strftime("%H:%M", time.gmtime(value))
            
    
    def __midiVelocityToTimeValue(self, velocity:int) -> int:
        return round(velocity / 127 * self.maxTime * 60)
    
    def __timerTick(self) -> None:
        self.timeValue -= 1
        self.progressbar["value"] = self.timeValue
        self.label["text"] = self.__convertTimeValueToString(self.timeValue)
        self.window.update_idletasks()

        if self.timeValue > 0:
            self.window.after(1000, self.__timerTick)
        else:
            self.timerRunning = False
            self.progressbar["maximum"] = 90 * 60
            self.__timerSound()

    def __timerSound(self) -> None:
        self.window.deiconify()
        if random.randint(1,6) == 1:
            self.__EASAlarm.play()
        else:
            self.__normalAlarm.play()