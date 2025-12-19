from MidiActions import MidiAction, Timer, MidiEvent

import tkinter as tk
from tkinter import ttk
import pygame.midi

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
            action.action(event)
            return True
    return False

def logMidiEvent(event:MidiEvent, success:bool):
    s = f"Status: {event.status}, Note: {event.note}, Velocity: {event.velocity}, Success: {success}"
    listBox.insert(listBox.size(), s)
    listBox.see(listBox.size())
    if success:
        listBox.itemconfig(listBox.size()-1, {"fg":"Green"})
    else:
        listBox.itemconfig(listBox.size()-1, {"fg":"Red"})
    

pygame.midi.init()
midi_input_id = pygame.midi.get_default_input_id()
midi_input = pygame.midi.Input(midi_input_id)

window = tk.Tk()
window.title("MIDI Input Logger")
window.geometry("500x500")
ttk.Style().theme_use("clam")

listBox = tk.Listbox(window, height=300, width=50)
listBox.yview()
listBox.pack(pady=10)

MidiActions = [Timer(window)]

window.after(10, createMidiEvents)

window.mainloop()