import Midi
from Midi import Timer, Etch, MediaController, TaskManager
import tkinter as tk
from tkinter import ttk

config = Midi.Config("config/config.json")

window = tk.Tk()
window.title("MIDI Input Logger")
window.geometry("500x500")
ttk.Style().theme_use("clam")

listBox = tk.Listbox(window, height=300, width=50)
listBox.yview()
listBox.pack(pady=10)

MidiActions = [Timer.Timer(window, config), Etch.Etch(window, config), MediaController.MediaController(window, config), TaskManager.TaskManager(window, config)]

window.after(10, lambda: Midi.createMidiEvents(window, listBox, MidiActions))

window.mainloop()