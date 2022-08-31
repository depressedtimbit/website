from website import Create_app, socketio

app = Create_app()


if __name__ == '__main__':
    socketio.run(app, debug=True)
    #app.run(debug=True)