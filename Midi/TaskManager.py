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
        self.__window.resizable(False, False)
        self.__window.grid_rowconfigure(0, minsize=400)
        self.__window.grid_columnconfigure(0, minsize=200)
        self.__window.withdraw()
        
        # setup todo section
        self.__todoFrame = tk.Frame(self.__window, width=300, height=400, borderwidth=5, relief="groove")
        self.__todoFrame.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        self.__todoFrame.grid_propagate(False)

        self.__label = tk.Label(self.__todoFrame, text="TODAY", anchor="w")
        self.__label.pack(pady=10)

        self.__tasksFrame = tk.Frame(self.__todoFrame, height=300, width=250, borderwidth=0)
        self.__tasksFrame.pack()
        self.__tasksFrame.pack_propagate(False)

        self.__inputFrame = tk.Frame(self.__todoFrame, borderwidth=5, relief="groove")
        self.__inputFrame.grid_rowconfigure(0)
        self.__inputFrame.grid_columnconfigure(0)
        self.__inputFrame.pack(anchor="center", side="bottom", pady=10)

        self.__itemInput = tk.Entry(self.__inputFrame, relief="flat")
        self.__itemInput.bind("<Return>", lambda event: self.__newItem())
        self.__itemInput.grid(row=0, column=0)
        
        self.__submitInput = tk.Button(self.__inputFrame, command=self.__newItem, text="↵", borderwidth=0)
        self.__submitInput.grid(row=0, column=1)

        # setup calendar section
        self.__calendarFrame = tk.Frame(self.__window, borderwidth=5, relief="groove")
        self.__calendarFrame.grid_rowconfigure(0)
        self.__calendarFrame.grid_columnconfigure(0)
        self.__calendarFrame.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        #self.__calendarFrame.grid_propagate(False)

        self.day1Frame = tk.Frame(self.__calendarFrame, width=100, height=380, borderwidth=5, relief="groove")
        self.day1Frame.grid(row=0, column=0, padx=2, pady=5, sticky="n")
        
        self.day2Frame = tk.Frame(self.__calendarFrame, width=100, height=380, borderwidth=5, relief="groove")
        self.day2Frame.grid(row=0, column=1, padx=2, pady=5, sticky="n")

        self.day3Frame = tk.Frame(self.__calendarFrame, width=100, height=380, borderwidth=5, relief="groove")
        self.day3Frame.grid(row=0, column=2, padx=2, pady=5, sticky="n")

        self.day4Frame = tk.Frame(self.__calendarFrame, width=100, height=380, borderwidth=5, relief="groove")
        self.day4Frame.grid(row=0, column=3, padx=2, pady=5, sticky="n")

        self.day5Frame = tk.Frame(self.__calendarFrame, width=100, height=380, borderwidth=5, relief="groove")
        self.day5Frame.grid(row=0, column=4, padx=2, pady=5, sticky="n")
        

        self.__window.protocol("WM_DELETE_WINDOW", self.__window.withdraw)

    def action(self, event:Midi.MidiEvent) -> None:
        self.__window.deiconify()

    def __newItem(self):
        item = tk.Checkbutton(self.__tasksFrame, text=self.__itemInput.get())
        self.__itemInput.delete(0, tk.END)
        item.pack(anchor="w", padx=2, pady=2)