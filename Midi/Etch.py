import tkinter as tk
import Midi
import turtle

class Etch(Midi.MidiAction):
    def __init__(self, window:tk.Tk, config:Midi.Config) -> None:
        super().__init__("Etch-A-Sketch", config)
        
        self.allowed_midi_statuses:list[int]|None = [176]
        self.allowed_midi_notes:list[int]|None = [75, 76]
        self.allowed_midi_velocities:list[int]|None = None

        self.__window = tk.Toplevel(window)
        self.__window.title("Etch-A-Sketch")
        self.__window.resizable(False, False)
        self.__window.withdraw()

        self.__label = tk.Label(self.__window, text="Etch-A-Sketch", anchor=tk.CENTER)
        self.__label.pack(pady=10)

        self.__canvas = tk.Canvas(self.__window, width=500, height=500, highlightthickness=1, highlightbackground="black")
        self.__canvas.pack(padx=20, pady=20)

        self.__turtleScreen = turtle.TurtleScreen(self.__canvas)
        self.__turtleScreen.bgcolor("white")

        self.__turtle = turtle.RawTurtle(self.__turtleScreen, shape="turtle")

        self.__leftKnobVal:int = -1
        self.__rightKnobVal:int = -1

        self.__lastWinX:int = self.__window.winfo_x()
        self.__lastWinY:int = self.__window.winfo_y()

        self.__window.protocol("WM_DELETE_WINDOW", self.__window.withdraw)
        self.__window.bind("<Configure>", self.__onConfigure)
    
    def action(self, event:Midi.MidiEvent) -> None:
        self.__window.deiconify()
        if event.note == 75:
            self.__leftKnobVal = self.__velocityToCoordinate(event.velocity)
        if event.note == 76:
            self.__rightKnobVal = self.__velocityToCoordinate(event.velocity)

        if self.__leftKnobVal != -1 and self.__rightKnobVal != -1:
            self.__turtle.goto(self.__leftKnobVal, self.__rightKnobVal)
            self.__turtle.pendown()
            self.__label["text"] = "Shake window to clear"
        else:
            self.__label["text"] = "Rotate both knobs to calibrate"
            self.__turtle.penup()

    def __velocityToCoordinate(self, velocity:int) -> int:
        return round(velocity/127 * 500) - 250
    
    def __onConfigure(self, event):
        currentX = self.__window.winfo_x()
        currentY = self.__window.winfo_y()

        if (currentX, currentY) != (self.__lastWinX, self.__lastWinY):
            self.__turtle.clear()
            self.__lastWinX = currentX
            self.__lastWinY = currentY