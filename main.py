from flask import Flask, render_template
from create import Livestream
from view import View
from flask import request

app = Flask(__name__)
app.debug=True

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create")
def create_stream():
    data = Livestream.create()
    # print(data.entry_id)
    return render_template("entry.html", **data)

@app.route("/view/", methods=['get'])
def view_stream(): 
    data = View.playback_for(request.args.get('username'), request.args.get('entry_id'), request.args.get('user_role'))
    return render_template("view.html", **data)

if __name__ == "__main__":
    app.run(debug=True)