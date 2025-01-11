from flask_socketio import SocketIO

# Sets up the SocketIO object
# SocketIO lets the server(backend) communicate with the user(frontend) without reloading
socketio = SocketIO(async_mode='eventlet', logger=True, engineio_logger=True,cors_allowed_origins="*", ping_interval=10)
