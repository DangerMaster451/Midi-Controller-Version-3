import tkinter as tk
from tkinter import ttk, Toplevel
import random
from pygame import mixer

mixer.init()

class MidiEvent():
    def __init__(self, event) -> None:
        self.status = event[0][0]
        self.note = event[0][1]
        self.velocity = event[0][2]

class MidiAction():
    def __init__(self, name:str) -> None:
        self.name = name
        self.allowed_midi_statuses:list[int]|None
        self.allowed_midi_notes:list[int]|None
        self.allowed_midi_velocities:list[int]|None

    def verify(self, event:MidiEvent) -> bool:
        if self.allowed_midi_statuses != None and event.status not in self.allowed_midi_statuses:
            return False
        if self.allowed_midi_notes != None and event.note not in self.allowed_midi_notes:
            return False
        if self.allowed_midi_velocities != None and event.velocity not in self.allowed_midi_velocities:
            return False
        return True

    def action(self, event:MidiEvent) -> None:
        pass

class Timer(MidiAction):
    def __init__(self, window:tk.Tk) -> None:
        super().__init__("timer")
        
        self.allowed_midi_statuses:list[int]|None = [176]
        self.allowed_midi_notes:list[int]|None = [74, 118]
        self.allowed_midi_velocities:list[int]|None = None

        self.maxTime = 90

        self.timeValue:int = 45
        self.timerRunning:bool = False

        self.__EASAlarm = mixer.Sound("sounds/EAS.mp3")
        self.__normalAlarm = mixer.Sound("sounds/lofiAlarm.mp3")

        self.window = tk.Toplevel(window)
        self.window.title("Timer")
        self.window.withdraw()

        self.label = tk.Label(self.window, text="Timer", anchor=tk.CENTER)
        self.label.pack(pady=10)

        self.progressbar = ttk.Progressbar(self.window, length=400)
        self.progressbar["maximum"] = 90
        self.progressbar["value"] = 45
        self.progressbar.pack(padx=20, pady=20)

        self.window.protocol("WM_DELETE_WINDOW", self.window.withdraw)
    
    def action(self, event:MidiEvent) -> None:
        if event.note == 74:
            self.__handleKnob(event)
        if event.note == 118:
            self.__handleButton(event)
    
    def __handleKnob(self, event:MidiEvent) -> None:
        self.window.deiconify()
        if self.timerRunning:
            return None
        self.timeValue = self.__midiVelocityToTimeValue(event.velocity)
        self.progressbar["value"] = self.timeValue
        self.label["text"] = self.__convertTimeValueToString(self.timeValue)

    def __handleButton(self, event:MidiEvent) -> None:
        self.window.withdraw()
        if self.timerRunning:
            return None
        if self.timeValue == 0:
            mixer.pause()
            return None
        self.timerRunning = True
        self.progressbar["maximum"] = self.timeValue
        self.window.after(0, self.__timerTick)

    def __convertTimeValueToString(self, velocity:int) -> str:
        if velocity >= 60:
            if velocity-60 >= 10:
                return f"01:{velocity-60}"
            return f"01:0{velocity-60}"
        if velocity >= 10:
            return f"00:{velocity}"
        return f"00:0{velocity}"
    
    def __midiVelocityToTimeValue(self, velocity:int) -> int:
        return round(velocity / 127 * self.maxTime)
    
    def __timerTick(self) -> None:
        self.timeValue -= 1
        self.progressbar["value"] = self.timeValue
        self.label["text"] = self.__convertTimeValueToString(self.timeValue)
        self.window.update_idletasks()

        if self.timeValue > 0:
            self.window.after(60000, self.__timerTick)
        else:
            self.timerRunning = False
            self.progressbar["maximum"] = 90
            self.__timerSound()

    def __timerSound(self) -> None:
        self.window.deiconify()
        if random.randint(1,6) == 1:
            self.__EASAlarm.play()
        else:
            self.__normalAlarm.play()