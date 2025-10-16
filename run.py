from app import create_app
from extensions import socketio

flask_app = create_app()

if __name__ == "__main__":

    socketio.run(flask_app, port = 5000, allow_unsafe_werkzeug=True, debug=True)
