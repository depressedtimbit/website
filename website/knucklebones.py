from flask import Blueprint, flash, render_template, request, session, redirect, url_for
from flask_socketio import emit, join_room
from random import randint
from . import socketio

bones = Blueprint('bones', __name__)

class Gamesmanager():
    def __init__(self) -> None:
        self.activeGames = {}
    def newgame(self, gameid):
        if not gameid in self.activeGames:
            self.activeGames[gameid]=Game(gameid)
        return self.activeGames[gameid]
    def removegame(self, gameid):
        self.activeGames.pop(gameid)
class player():
    def __init__(self, name) -> None:
        self.name = name
        self.board = []
        for i in range(3):
            row = [0, 0, 0]
            self.board.append(row)
        print(self.board)
            
class Game():
    def __init__(self, gameid) -> None:
        self.gameid = gameid
        self.players = []
        self.turn = 0
        self.lastroll = 0
    def playerjoined(self, newplayername):
        self.players.append(player(newplayername))
    def update_board(self):
        player1 = self.players[0]
        player2 = self.players[1]
        return [player1.board, player2.board]
    def player_selection(self, playerselection):
        player = self.players[self.turn]
        oplayer = self.players[-self.turn+1]
        for i, val in enumerate(player.board[playerselection]):
            #print(player.board[playerselection])
            if val == 0:
                    player.board[playerselection][i] = self.lastroll
                    for oi, oval in enumerate(oplayer.board[playerselection]):
                        print(f'{oval}:{self.lastroll}')
                        if oval == self.lastroll:
                            oplayer.board[playerselection][oi] = 0
                    return True
                
        

gamemanager = Gamesmanager()

@bones.route('/')
def lobby():
    return render_template("knucklebones_lobby.html.j2")

@bones.route('/fullscreen')
def fullscreen():
    return render_template("knucklebones_black.html.j2")


@socketio.on('join')
def handle_message(data):
    room = data['Room']
    Game = gamemanager.newgame(room)
    Game.playerjoined(data["Player"])
    playerlist = []
    for player in Game.players:
        playerlist.append(player.name)
    join_room(room)
    #send({'PlayerJoined': playerlist}, to=data["Room"])
    emit("PlayerJoined", playerlist, room=room)
    return len(playerlist) -1
 
@socketio.on('startLobby')
def handle_message(data):
    room = data['Room']
    Game = gamemanager.activeGames[room]
    roll = randint(1, 6)
    Game.lastroll = roll
    emit('newturn', [Game.turn, roll], to=room)
    emit('update-board', Game.update_board(), to=room)

@socketio.on('progressTurn')
def handle_message(data):
    room = data['Room']
    player = data['Player']
    choice = data['Choice']
    game:Game = gamemanager.activeGames[room]
    if game.turn == player:
        valid_choice = game.player_selection(choice)
        print(valid_choice)
        if valid_choice:
            roll = randint(1, 6)
            game.lastroll = roll
            if game.turn == 1:
                game.turn = 0
            else: game.turn = 1
            emit('newturn', [game.turn, roll], to=room)
            emit('update-board', game.update_board(), to=room)


