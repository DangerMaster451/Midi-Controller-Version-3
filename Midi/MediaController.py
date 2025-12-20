from http.server import BaseHTTPRequestHandler, HTTPServer
import tkinter as tk
import threading
import Midi

PORT = 8000
CURRENT_COMMAND:str = "None"

class Server(threading.Thread):
    def __init__(self, host, port, gui, queue):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.gui = gui
        self.queue = queue
        self.daemon = True

    def run(self):
        print(f"Listening on http://{self.host}:{self.port}\n")
        server = HTTPServer((self.host, self.port), Handler)
        server.serve_forever()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Contest-type", "text/plain")
        self.end_headers()
        self.wfile.write(CURRENT_COMMAND.encode("utf-8"))
        print("GET!")

class MediaController(Midi.MidiAction):
    def __init__(self, window:tk.Tk) -> None:
        super().__init__("Media Controller")
        
        self.allowed_midi_statuses:list[int]|None = [176]
        self.allowed_midi_notes:list[int]|None = [64]
        self.allowed_midi_velocities:list[int]|None = [0]

        self.__window = tk.Toplevel(window)
        self.__window.title("Media Controller")
        self.__window.resizable(False, False)
        self.__window.withdraw()

        self.__window.protocol("WM_DELETE_WINDOW", self.__window.withdraw)

        server = Server("localhost", 8000, None, None)
        server.start()

    def action(self, event:Midi.MidiEvent) -> None:
        print("toggle media playback")