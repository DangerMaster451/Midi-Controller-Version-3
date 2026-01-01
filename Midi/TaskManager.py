import Midi
import tkinter as tk

class TaskManager(Midi.MidiAction):
    def __init__(self, window:tk.Tk, config:Midi.Config) -> None:
        super().__init__("Task Manager", config)
        
        self.allowed_midi_statuses:list[int]|None = [144]
        self.allowed_midi_notes:list[int]|None = [48]
        self.allowed_midi_velocities:list[int]|None = None

        self.__window = tk.Toplevel(window)
        self.__window.title("Task Manager")
        self.__window.minsize(300, 200)
        self.__window.resizable(False, False)
        self.__window.withdraw()

        self.__label = tk.Label(self.__window, text="TODAY", anchor=tk.CENTER)
        self.__label.pack(pady=10)

        self.__inputFrame = tk.Frame(self.__window, borderwidth=5, relief="groove")
        self.__inputFrame.rowconfigure(0, weight=1)
        self.__inputFrame.columnconfigure(0, weight=1)
        self.__inputFrame.pack(anchor="center", side="bottom", pady=10)

        self.__itemInput = tk.Entry(self.__inputFrame, relief="flat")
        self.__itemInput.bind("<Return>", lambda event: self.__newItem())
        self.__itemInput.grid(row=0, column=0)
        

        self.__submitInput = tk.Button(self.__inputFrame, command=self.__newItem, text="↵", borderwidth=0)
        self.__submitInput.grid(row=0, column=1)

        self.__window.protocol("WM_DELETE_WINDOW", self.__window.withdraw)

    def action(self, event:Midi.MidiEvent) -> None:
        self.__window.deiconify()

    def __newItem(self):
        item = tk.Checkbutton(self.__window, text=self.__itemInput.get())
        self.__itemInput.delete(0, tk.END)
        item.pack(anchor="w", padx=2, pady=2)