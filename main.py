from flask import Flask, render_template, redirect
from create import Livestream
from view import View
from flask import request
import config 

app = Flask(__name__)
app.debug=True

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create")
def create_stream():
    data = Livestream.create()
    return render_template("entry.html", **data)

@app.route("/view/<entry_id>", methods=['get'])
def view_stream(entry_id): 
    if (config.player_v2):
        data = View.playback(entry_id, config.uiconf_idv2)
        return render_template("view-v2.html", **data)
    else: 
        data = View.playback(entry_id, config.uiconf_id)
        return render_template("view.html", **data)

@app.route("/moderator/<entry_id>", methods=['get'])
def moderator_view(entry_id): 
    moderator_url = View.moderator_view(entry_id)
    return redirect(moderator_url, code=302)

if __name__ == "__main__":
    app.run(debug=True)