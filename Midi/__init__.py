from pygame import midi, mixer

mixer.init()
midi.init()
midi_input_id = midi.get_default_input_id()
midi_input = midi.Input(midi_input_id)

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

def createMidiEvents(window, listBox, MidiActions) -> None:
    if midi_input.poll():   
        for event in midi_input.read(5):
            midiEvent = MidiEvent(event)
            success = handleMidiEvent(midiEvent, MidiActions)
            logMidiEvent(midiEvent, listBox, success)

    window.after(10, lambda: createMidiEvents(window, listBox, MidiActions))
    return None

def handleMidiEvent(event:MidiEvent, midiActions) -> bool:
    for action in midiActions:
        if action.verify(event):
            action.action(event)
            return True
    return False

def logMidiEvent(event:MidiEvent, listBox, success:bool):
    s = f"Status: {event.status}, Note: {event.note}, Velocity: {event.velocity}, Success: {success}"
    listBox.insert(listBox.size(), s)
    listBox.see(listBox.size())
    if success:
        listBox.itemconfig(listBox.size()-1, {"fg":"Green"})
    else:
        listBox.itemconfig(listBox.size()-1, {"fg":"Red"})