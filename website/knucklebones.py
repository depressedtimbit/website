from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_socketio import emit
from . import socketio

bones = Blueprint('bones', __name__)



@bones.route('/', methods=['GET', 'POST'])
def lobby():
    if request.method == 'POST':
        session['name'] = request.form.get("username")
        session['room'] = request.form.get("room-id")
    return render_template("knucklebones_lobby.html.j2")

@bones.route('/game')
def game():
    username = session.get('username', '')
    room = session.get('room-id', '')
    if username == '' or room == '':
        return redirect(url_for('.lobby'))
    return render_template('knucklebones.html.j2',username=username, room=room)

@socketio.on('hello')
def handle_message(data):
    print('received message: ' + data["data"])
    emit('hi', {'data' : "I heard!"})
    