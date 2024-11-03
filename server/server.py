from flask import Flask


app = Flask(__name__)


@app.route("/")
@app.route("/home")
@app.route("/login", methods=["GET", "POST"])
@app.route("/logout", methods=["GET", "POST"])
@app.route("/signin", methods=["GET", "POST"])
@app.route("/forum", methods=["GET"])
@app.route("/profile", methods=["GET"])
@app.route("/profile/<user_id>", methods=["GET"])
@app.route("/forum/post", methods=["GET", "POST"])
@app.route("/forum/post/<post_id>", methods=["GET", "POST"])
def home():
    return "Hello World!"




if __name__ == "__main__":
    app.run(host="0.0.0.0")