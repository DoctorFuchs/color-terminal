import os, socket
import subprocess as sub
from settings import *


class terminal:
    def __init__(self):
        # init
        self.history = []
        self.path = os.environ["HOME"]
        self.options = ["python3 <file>", "python <file>", "apt", "pip3", "pip", "git", "ls", "cd"]

    def getUser(self):
        return os.environ["USER"]


    def getVisiblePath(self):
        # replace pwd path if you are at HOME
        if self.path == os.environ["HOME"]:
            path = "⁓"

        else:
            path = self.path

        return path

    def getCommandsHTML(self):
        # generates suggestions for autocompletion (in html)
        completion = """"""
        for i in range(len(self.options)):
            completion += f"""<option value="{self.options[i]}">"""

        for j in range(len(os.listdir(self.path))):
            completion += f"""<option value="{os.listdir(self.path)[j]}">"""

        return completion

    def log(self, command):
        # replace clear command
        if command == "clear":
            # clear the history
            self.history = []
            return "cleared!"

        # client
        output = sub.Popen(command, shell="true", stdout=sub.PIPE, stderr=sub.PIPE, stdin=sub.PIPE, cwd=self.path)

        try:
            # modified commands
            if command.startswith("cd"):
                try:
                    print(command.split("cd ")[1])
                    if os.path.isdir(command.split("cd ")[1]):
                        self.path = command.split("cd ")[1]

                except:
                    self.path = os.environ["HOME"]

            if command.startswith("ls"):
                try:
                    if os.path.isdir(command.split("ls ")[1]):
                        return os.listdir(command.split("ls ")[1])

                except IndexError:
                    return os.listdir(self.path)

        except IndexError:
            pass

        try:
            return output.stdout.read().decode("utf-8") + output.stderr.read().decode("utf-8")

        except AttributeError:
            try:
                return output.stdout.read().decode("utf-8")

            except AttributeError:
                return output.stderr.read().decode("utf-8")

    def getBeforeInput(self):
        return f"{self.getUser()}@{socket.gethostbyname(socket.gethostname())}  {self.getVisiblePath()} % "

    def getRecentHTML(self):
        # print the history (in html)
        returner = ""
        for i in range(len(self.history)):
            try:
                if self.history[i].startswith(self.getUser()):
                    returner += f"<label style='color:{INPUT}'>{self.history[i]}</label><br>"

                else:
                    returner += f"<label style='color:{OUTPUT}'>{self.history[i]}</label><br>"

            except AttributeError:
                for j in range(len(self.history[i])):
                    returner += f"<label style='color:{OUTPUT}'>{self.history[i][j]}</label><br>"

        return returner