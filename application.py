import os, requests

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Data memory storage
votes = {"yes": 0, "no": 0, "maybe": 0}


@app.route("/")
def index():
    return render_template("index.html", votes=votes)


@socketio.on("submit vote")
def vote(data):
    selection = data["selection"]
    votes[selection] += 1
    emit("vote totals", votes, broadcast=True)


# Adapted from https://flask-socketio.readthedocs.io/en/latest/
# Handles the default namespace
@socketio.on_error()
def error_handler(e):
    print(e)


# handles the '/chat' namespace
@socketio.on_error("/chat")
def error_handler_chat(e):
    print(e)


# handles all namespaces without an explicit error handler
@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"])  # "my error event"
    print(request.event["args"])  # (data,)
