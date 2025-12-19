import Midi
from Midi import Timer
import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title("MIDI Input Logger")
window.geometry("500x500")
ttk.Style().theme_use("clam")

listBox = tk.Listbox(window, height=300, width=50)
listBox.yview()
listBox.pack(pady=10)

MidiActions = [Timer.Timer(window)]

window.after(10, lambda: Midi.createMidiEvents(window, listBox, MidiActions))

window.mainloop()