import tkinter as tk
import pygame.midi

class MidiEvent():
    def __init__(self, event) -> None:
        self.status = event[0][0]
        self.note = event[0][1]
        self.velocity = event[0][2]

def createMidiEvents() -> None:
    if not midi_input.poll():
        window.after(10, createMidiEvents)
        return None    
    for event in midi_input.read(5):
        m = MidiEvent(event)
        s = f"Status: {m.status}, Note: {m.note}, Velocity: {m.velocity}"
        listBox.insert(listBox.size(), s)
        listBox.see(listBox.size())

    window.after(10, createMidiEvents)
    return None

pygame.midi.init()
midi_input_id = pygame.midi.get_default_input_id()
midi_input = pygame.midi.Input(midi_input_id)

window = tk.Tk()
window.title("Hi there, Hello")
window.geometry("500x500")

listBox = tk.Listbox(window, height=300, width=50)
listBox.yview()
listBox.pack(pady=10)

window.after(10, createMidiEvents)

window.mainloop()