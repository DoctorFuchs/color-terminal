from flask import Flask, request

from terminal import *

client = terminal()
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def terminal():  # interface
    # get command (skip on when command is not given)
    if request.method == "POST":
        command = request.form["command_line"]

    else:
        command = request.args.get("command_line")

    if command is not None:
        # log this to the client (see in terminal.py)
        client_out = client.log(command)

    else:
        client_out = ""
        command = " "

    # log to history (so you can see them later at the console)
    client.history.append(client.getBeforeInput() + command)
    client.history.append(client_out)

    return f"""
<html style="background-color:{BACKGROUND}"> 
<head>
    <meta charset="UTF-8">
    <title>{client.getBeforeInput()}</title>
</head>

<body>
    {client.getRecentHTML()}
    <form method="POST" method="POST" action="/">
        <label for"command_line" style="color:{INPUT}">{client.getBeforeInput()}</label>
        <input type="text" id="command_line" name="command_line" list="commands" style="{style}" autofocus="{autofocus}" autocomplete={autocomplete}> 
        <datalist id="commands">
            {client.getCommandsHTML()}
        </datalist>
    </form>
</body>
</html>"""


# run
if __name__ == "__main__":
    app.run("localhost", 5000, debug=True)
