from flask import Flask, render_template, url_for


app = Flask(__name__, template_folder="static", static_folder="styles")


@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html", 
                        MENU=render_template("menubar.html", STYLE=url_for('static', filename="menubar.css")), 
                        STYLE=url_for('static', filename="home.css"),
                        COMMANDS=render_template("base.html", COMMANDS="LS"))




@app.route("/login", methods=["GET", "POST"])
@app.route("/logout", methods=["GET", "POST"])
@app.route("/signin", methods=["GET", "POST"])
@app.route("/forum", methods=["GET"])
@app.route("/profile", methods=["GET"])
@app.route("/profile/<user_id>", methods=["GET"])
@app.route("/forum/post", methods=["GET", "POST"])
@app.route("/forum/post/<post_id>", methods=["GET", "POST"])
def test():
    return "Hello World!"




if __name__ == "__main__":
    app.run(host="0.0.0.0")