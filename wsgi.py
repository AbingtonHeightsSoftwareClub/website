from run import flask_app, socketio

if __name__=="main":
    socketio.run(flask_app)