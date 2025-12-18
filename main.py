import tkinter as tk
import pygame.midi

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

    def action(self):
        print(self.name)


def createMidiEvents() -> None:
    if midi_input.poll():   
        for event in midi_input.read(5):
            midiEvent = MidiEvent(event)
            success = handleMidiEvent(midiEvent)
            logMidiEvent(midiEvent, success)

    window.after(10, createMidiEvents)
    return None

def handleMidiEvent(event:MidiEvent) -> bool:
    for action in MidiActions:
        if action.verify(event):
            action.action()















    return True

def logMidiEvent(event:MidiEvent, success:bool):
    s = f"Status: {event.status}, Note: {event.note}, Velocity: {event.velocity}, Success: {success}"
    listBox.insert(listBox.size(), s)
    listBox.see(listBox.size())

pygame.midi.init()
midi_input_id = pygame.midi.get_default_input_id()
midi_input = pygame.midi.Input(midi_input_id)

window = tk.Tk()
window.title("MIDI Input Logger")
window.geometry("500x500")

listBox = tk.Listbox(window, height=300, width=50)
listBox.yview()
listBox.pack(pady=10)

MidiActions = [MidiAction("C", [144], [60], None)]

window.after(10, createMidiEvents)

window.mainloop()