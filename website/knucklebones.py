from flask import Blueprint, flash, render_template, request, session, redirect, url_for
from flask_socketio import emit
from . import socketio

bones = Blueprint('bones', __name__)



@bones.route('/', methods=['GET', 'POST'])
def lobby():
    if request.method == 'POST':
        session['name'] = request.form.get("username")
        session['room'] = request.form.get("room-id")
        return redirect(url_for("bones.game"))
    return render_template("knucklebones_lobby.html.j2")

@bones.route('/game')
def game():
    username = session.get('name', '')
    room = session.get('room', '')
    if username == '' or room == '':
        flash("no room", category="error")
        return redirect(url_for('.lobby'))
    return render_template('knucklebones.html',username=username, room=room)

@socketio.on('joined')
def handle_message(Data):
    print(Data)
    