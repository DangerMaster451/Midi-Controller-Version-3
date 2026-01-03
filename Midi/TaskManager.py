import Midi
import tkinter as tk
from datetime import timedelta, date, time
from PIL import Image, ImageTk

class CalendarDay(tk.Frame):
    def __init__(self, root:tk.Frame, index:int):
        super().__init__(root, width=110, height=380, borderwidth=5, relief="groove")
        self.grid(row=0, column=index, padx=2, pady=5, sticky="new")
        self.grid_propagate(False)

        text = (date.today() + timedelta(days=index)).strftime("%m-%d")

        self.__label = tk.Label(self, text=text)
        self.__label.grid(row=0, column=0, pady=2)

class CalendarEvent(tk.Frame):
    def __init__(self, root:tk.Frame, index:int, title:str, startTime:time, endTime:time, color:str):
        self.__title = title
        self.__startTime = startTime
        self.__endTime = endTime
        self.__color = color
        super().__init__(root, width=100, height=75, borderwidth=2, relief="groove", bg=self.__color)
        self.grid(row=index, column=0)

class TaskManager(Midi.MidiAction):
    def __init__(self, window:tk.Tk, config:Midi.Config) -> None:
        super().__init__("Task Manager", config)
        
        self.allowed_midi_statuses:list[int]|None = [144]
        self.allowed_midi_notes:list[int]|None = [48]
        self.allowed_midi_velocities:list[int]|None = None

        self.__window = tk.Toplevel(window, width=850, height=500)
        self.__window.title("Task Manager")
        self.__window.resizable(False, False)
        self.__window.grid_columnconfigure(0, weight=1)
        self.__window.grid_columnconfigure(1, weight=6)
        self.__window.grid_rowconfigure(0)
        self.__window.grid_propagate(False)
        self.__window.withdraw()

        # set background
        background_image=ImageTk.PhotoImage(Image.open("assets/taskmanager_wallpaper.jpg").resize((1280,720)))
        background_label = tk.Label(self.__window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image #type: ignore

        # setup todo section
        self.__todoFrame = tk.Frame(self.__window, width=200, height=400, borderwidth=5, relief="groove")
        self.__todoFrame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.__todoFrame.grid_propagate(False)

        self.__label = tk.Label(self.__todoFrame, text="TODAY", anchor="w")
        self.__label.pack(pady=10)

        self.__tasksFrame = tk.Frame(self.__todoFrame, height=300, width=150, borderwidth=0)
        self.__tasksFrame.pack()
        self.__tasksFrame.pack_propagate(False)

        self.__inputFrame = tk.Frame(self.__todoFrame, borderwidth=5, relief="groove")
        self.__inputFrame.pack(anchor="center", side="bottom", pady=10)

        self.__itemInput = tk.Entry(self.__inputFrame, relief="flat")
        self.__itemInput.bind("<Return>", lambda event: self.__newItem())
        self.__itemInput.grid(row=0, column=0)
        
        self.__submitInput = tk.Button(self.__inputFrame, command=self.__newItem, text="↵", borderwidth=0)
        self.__submitInput.grid(row=0, column=1)

        # setup calendar section
        self.__calendarFrame = tk.Frame(self.__window, borderwidth=5, relief="groove")
        self.__calendarFrame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.__calendarDayFrames:list[CalendarDay] = []
        
        for i in range(0,5):
            self.__calendarDayFrames.append(CalendarDay(self.__calendarFrame, i))

        test = CalendarEvent(self.__calendarDayFrames[0], 1, "test", time(0,0,0), time(0,0,0), "red")
        
        self.__window.protocol("WM_DELETE_WINDOW", self.__window.withdraw)

    def action(self, event:Midi.MidiEvent) -> None:
        self.__window.deiconify()

    def __newItem(self):
        item = tk.Checkbutton(self.__tasksFrame, text=self.__itemInput.get())
        self.__itemInput.delete(0, tk.END)
        item.pack(anchor="w", padx=2, pady=2)