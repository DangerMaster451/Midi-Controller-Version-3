from http.server import BaseHTTPRequestHandler, HTTPServer
import tkinter as tk
import threading
import Midi

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

        self.currentCommand:str = "None"

        server = Server("", 8000, self)
        server.start()
        print("Server Started!")

    def action(self, event:Midi.MidiEvent) -> None:
        if self.currentCommand == "None":
            self.currentCommand = "toggle"
        
class Server(threading.Thread):
    def __init__(self, host, port, controller:MediaController):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.daemon = True
        self.controller = controller
        
    def run(self):
        def handler(*args):
            return Handler(self.controller, *args)
        server = HTTPServer((self.host, self.port), handler)
        server.serve_forever()

class Handler(BaseHTTPRequestHandler):
    def __init__(self, controller:MediaController, *args):
        self.controller = controller
        BaseHTTPRequestHandler.__init__(self, *args)

    def log_message(self, format: str, *args) -> None:
        pass

    def do_GET(self):
        if self.path == "/controller":
            self.send_response(200)
            self.send_header("Contest-type", "text/html")
            self.end_headers()

            with open("html/controller.html", "rb") as file:
                content = file.read()
                self.wfile.write(content)


        elif self.path == "/clicked?":
            self.send_response(200)
            self.send_header("Contest-type", "text/html")
            self.end_headers()

            with open("html/clicked.html", "rb") as file:
                content = file.read()
                self.wfile.write(content)
            self.controller.currentCommand = "toggle"

        else:
            self.send_response(200)
            self.send_header("Contest-type", "text/plain")
            self.end_headers()

            self.wfile.write(self.controller.currentCommand.encode("utf-8"))
            self.controller.currentCommand = "None"