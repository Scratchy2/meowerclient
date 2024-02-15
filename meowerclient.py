import requests, time, PySimpleGUI as sg, threading, pyautogui as p, re

class MeowerClient:
    def __init__(self) -> None:
        self.token = ""
        self.messages = []
        self.history = []
        self.old = []
        self.author = ""
        self.new = []
        self.window = ""
        self.p = ""
        global layout
        layout = []

    def _initialize(self, token: str):
        """
        Please use the RUNCLIENT() function instead of this one.
        """
        self.token = token
        self.messages = []
        self.history = requests.get("https://api.meower.org/home?autoget&page=1").json()["autoget"][0:25]

    def _showHistory(self):
        """
        Please use the RUNCLIENT() function instead of this one.
        """
        for i in range(len(self.history)):
            self.old = self.history[24 - i]
            self.p = self.old["p"]
            try:
                if self.old["unfiltered_p"]:
                    self.p = self.old["unfiltered_p"]
            except:
                pass
            
            self.author = self.old["u"]
            if self.author == "Discord":
                self.messages.append(f'(#{len(self.messages) + 1}, bridged) {self.p}')
            else:
                self.messages.append(f'(#{len(self.messages) + 1}, meower ) {self.author}: {self.p}')

    def _createWin(self):
        """
        Please use the RUNCLIENT() function instead of this one.
        """
        global layout
        layout = [
            [
                sg.Text("MeowerClient", font=("Terminal", 32), text_color="#000", background_color="#e48b26"),
            ],
            [
                sg.Text("\n".join(self.messages), key="history", font=("Terminal", 12), text_color="#000", background_color="#e48b26"),
            ],
            [
                sg.Input(background_color="#000", text_color="#FFF", font=("Terminal", 14), key="message", size=(100, 1)),
                sg.Button("Send", button_color=("#FFF", "#000"), font=("Terminal", 14))
            ],
            [
                sg.Button("Reply", button_color=("#FFF", "#000"), font=("Terminal", 14)),
                sg.Button("Copy", button_color=("#FFF", "#000"), font=("Terminal", 14))
            ]
        ]
        self.window = sg.Window(title="Meower Python Client", layout=layout, margins=(5, 10), location=(0, 0), background_color="#e48b26")
    
    def _run(self):
        """
        Please use the RUNCLIENT() function instead of this one.
        """
        def newmessages():
            self.old = requests.get("https://api.meower.org/home?autoget&page=1").json()["autoget"][0]
            self.p = self.old["p"]
            try:
                if self.old["unfiltered_p"]:
                    self.p = self.old["unfiltered_p"]
            except:
                pass
            
            self.author = self.old["u"]
            if self.author == "Discord":
                self.messages.append(f'(#{len(self.messages) + 1}, bridged) {self.old["p"]}')
            else:
                self.messages.append(f'(#{len(self.messages) + 1}, meower ) {self.author}: {self.old["p"]}')
            while True:
                self.new = requests.get("https://api.meower.org/home?autoget&page=1").json()["autoget"][0]
                if self.new != self.old:
                    self.old = self.new
                    self.author = self.old["u"]
                    self.p = self.old["p"]
                    try:
                        if self.old["unfiltered_p"]:
                            self.p = self.old["unfiltered_p"]
                    except:
                        pass
                    
                    if self.author == "Discord":
                        self.messages.append(f'(#{len(self.messages) + 1}, bridged) {self.p}')
                    else:
                        self.messages.append(f'(#{len(self.messages) + 1}, meower ) {self.author}: {self.p}')

                    self.window["history"].update(value="\n".join(self.messages[len(self.messages) - 25:]))
        
                time.sleep(0.01)

        thread = threading.Thread(target=newmessages)
        thread.start()

        while True:
            event, values = self.window.read()
            if event == "Send":
                msg = values["message"]
                requests.post("https://api.meower.org/home", json={"content": msg}, headers={"username": "username", "token": self.token})
                self.window["message"].update(value="", select=True)
            elif event == "Reply":
                try:
                    idx = int(p.prompt("Message number on the list to reply to:"))
                    pattern = "\) (.+?: )(.+)"
                    matches = re.search(pattern, self.messages[idx - 1])
                    if len(matches.group(2)) > 35:
                        self.window["message"].update(value=f'@{matches.group(1)}"{matches.group(2)[:34]}..." {values["message"]}', select=True)
                    else:
                        self.window["message"].update(value=f'@{matches.group(1)}"{matches.group(2)}" {values["message"]}', select=True)
                    
                    p.hotkey("right")
                except:
                    print("error in input")
            elif event == "Copy":
                try:
                    idx = int(p.prompt("Message number on the list to copy:"))
                    prev = values["message"]
                    self.window["message"].update(value=self.messages[idx - 1], select=True)
                    p.hotkey("ctrl", "c", "backspace")
                    self.window["message"].update(value=prev, select=True)
                    p.hotkey("right")
                except:
                    print("error in input")
            elif event == sg.WIN_CLOSED:
                exit("program stopped")
            
            time.sleep(0.01)
    
    def RUNCLIENT(self, token: str):
        """
        Function to run the client. This function will call all initialization functions for you.
        """
        self.token = token
        MeowerClient._initialize(self=self, token=self.token)
        MeowerClient._showHistory(self=self)
        MeowerClient._createWin(self=self)
        MeowerClient._run(self=self)
