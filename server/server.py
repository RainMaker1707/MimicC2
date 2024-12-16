from flask import Flask, render_template, url_for, request, redirect, make_response
from threading import Thread
import json
import random


BOLD = "\033[1m"
RED = "\033[91m"
BLUE = "\033[94m"
END = "\033[0m"


app = Flask(__name__, template_folder="static", static_folder="static")

commands = list()

configs = dict()
with open("config/config.json", "r") as file:
    configs = json.loads(file.read())


def get_command():
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




@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    resp = make_response(
            render_template("base.html", TITLE="Home",
                        MENU=render_template("menu/menubar.html", STYLE=url_for('static', filename="styles/menubar.css")), 
                        STYLE=url_for('static', filename="styles/base.css"), 
                        COMMANDS= render_template("commands.html", COMMANDS=f'[{get_command()}]') if len(commands) > 0 else "",
                        ADD=render_template("html/home.html")
                        )
                    )
    resp.set_cookie('logged', 'False')
    return resp


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        handle_post(request)
        resp = make_response(redirect("/profile", code=302))
        resp.set_cookie('logged', 'True')
        return resp
    else:
        if request.cookies.get("logged") == "True":
            return redirect("/profile", code=302)
        return render_template("base.html", TITLE="Login",
                            MENU=render_template("menu/menubar.html", STYLE=url_for('static', filename="styles/menubar.css")), 
                            STYLE=url_for('static', filename="styles/base.css"),
                            COMMANDS=render_template("commands.html", COMMANDS=f'[{get_command()}]') if len(commands) > 0 else "",
                            ADD=render_template("forms/form.html",
                                CLASS="formLogin",
                                ACTION="/login",
                                CONTENT=render_template("forms/form_input.html", LABEL="Pseudo", TYPE="text") 
                                        + render_template("forms/form_input.html", LABEL="Password", TYPE="password")
                            ),
                        )


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        handle_post(request)
        return redirect("/profile", code=302)
    else:
        if request.cookies.get("logged") == "True":
                return redirect("/profile", code=302)
        return render_template("base.html", TITLE="Signin",
                            MENU=render_template("menu/menubar.html", STYLE=url_for('static', filename="styles/menubar.css")), 
                            STYLE=url_for('static', filename="styles/base.css"),
                            COMMANDS=render_template("commands.html", COMMANDS=f'[{get_command()}]') if len(commands) > 0 else "",
                            ADD=render_template("forms/form.html",
                                CLASS="formLogin",
                                ACTION="/signin",
                                CONTENT=render_template("forms/form_input.html", LABEL="Pseudo", TYPE="text") 
                                        + render_template("forms/form_input.html", LABEL="Password", TYPE="password")
                                        + render_template("forms/form_input.html", LABEL="Password confirmation", TYPE="password")
                            ),
                        )


@app.route("/profile", methods=["GET"])
def profile():
    if not request.cookies.get('logged') == "True":
        return redirect("/login", code=302)
    return render_template("base.html", TITLE="Profile",
                            MENU=render_template("menu/menubar.html", STYLE=url_for('static', filename="styles/menubar.css")), 
                            STYLE=url_for('static', filename="styles/base.css"),
                            COMMANDS=render_template("commands.html", COMMANDS=f'[{get_command()}]') if len(commands) > 0 else "",
                            ADD=render_template("profile.html", NAME="Heru'ur", RANK="members", INS="17-07-2023"),
                            )


@app.route("/logout", methods=["GET"])
def logout():
    resp = make_response(redirect("/", code=302))
    resp.set_cookie('logged', "False")
    return resp


@app.route("/forum", methods=["GET"])
@app.route("/forum/", methods=["GET"])
def forum():
    return render_template("base.html", TITLE='Forum', 
                            ADD=render_template("/html/subject.html"),
                            MENU=render_template("menu/menubar.html", STYLE=url_for('static', filename="styles/menubar.css")), 
                            STYLE=url_for('static', filename="styles/base.css"),
                            COMMANDS=render_template("commands.html", COMMANDS=f'[{get_command()}]') if len(commands) > 0 else "",)


@app.route("/forum/<string:sub>", methods=["GET"])
@app.route("/forum/<string:sub>/", methods=["GET"])
def subject(sub):
    if sub not in configs.get("subjects"):
        return redirect("/forum", code=404)
    else:
        if sub == "sg1":
            links = configs.get("sg1_links")
            members = {"oneill": "Jack O'Neill", "jackson": "Daniel Jackson", "carter":"Samantha Carter", "tealc":"Teal'c", "vala": "Vala Maldoran", "jonas": "Jonas Quinn"}
            bal = ""
            for e  in [f'<a href="{links.get(key)}">{members.get(key)}</a></br>' for key in links.keys()]:
                bal += e 
            return render_template("base.html", TITLE=f'SG1',
                                MENU=render_template("menu/menubar.html", STYLE=url_for('static', filename="styles/menubar.css")), 
                                STYLE=url_for('static', filename="styles/base.css"),
                                COMMANDS=render_template("commands.html", COMMANDS=f'[{get_command()}]') if len(commands) > 0 else "",
                                ADD=bal)
        else:
            return "PASS"


@app.route("/forum/<string:sub>/<string:wiki>", methods=["GET"])
@app.route("/forum/<string:sub>/<string:wiki>/", methods=["GET"])
def wiki_page(sub, wiki):
    if sub not in configs.get("subjects"):
        return redirect("/forum", code=404)
    else:
        if sub == "sg1":
            links = configs.get("sg1_links")
            members = {"oneill": "Jack O'Neill", "jackson": "Daniel Jackson", "carter":"Samantha Carter", "tealc":"Teal'c", "vala": "Vala Maldoran", "jonas": "Jonas Quinn"}
            if wiki not in members.keys():
                return redirect("/forum/sg1", code=404)
            bal = ""
            for e  in [f'<a href="{links.get(key)}">{members.get(key)}</a></br>' for key in links.keys() if key != wiki]:
                bal += e 
            return render_template("base.html", TITLE=f'Wiki - {members.get(wiki)}',
                                MENU=render_template("menu/menubar.html", STYLE=url_for('static', filename="styles/menubar.css")), 
                                STYLE=url_for('static', filename="styles/base.css"),
                                COMMANDS=render_template("commands.html", COMMANDS=f'[{get_command()}]') if len(commands) > 0 else "",
                                ADD=render_template("html/character.html",
                                    IMG=url_for('static', filename=f'imgs/{wiki}.jpg'),
                                    NAME=members.get(wiki),
                                    LINKS=bal
                                    ),
                                )
        return wiki







def start():
    print("Flask server started")
    app.run(host="0.0.0.0")



def operator_interface():
    while True:
        command = input("Enter a command:")
        print(command)
        if len(command.split()) > 0:
            if command.split()[0] in configs.get("allowed_commands"):
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