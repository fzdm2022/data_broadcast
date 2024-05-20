from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import socket
import threading
import select

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent')  # Specify gevent as the async mode

UDP_IP = "0.0.0.0"  # Listen on all available interfaces
UDP_PORT = 5007

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# List to store connected clients
connected_clients = set()

@socketio.on('connect')
def handle_connect():
    # Add client to the list of connected clients
    connected_clients.add(request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    # Remove client from the list of connected clients
    connected_clients.remove(request.sid)

def broadcast_data(data):
    # Send data to all connected clients
    for client in connected_clients:
        socketio.emit('data', data, room=client)
        # socketio.emit('data', data, broadcast=True, include_self=True, room=client)

@app.route('/')
def index():
    return render_template('index.html')

def receive_udp_data():
    while True:
        ready = select.select([sock], [], [], 1)
        if ready[0]:
            try:
                while True:
                    data, addr = sock.recvfrom(1024)
                    broadcast_data(data.decode('utf-8'))
            except BlockingIOError:
                pass


if __name__ == '__main__':
    # Start the background thread for receiving UDP data
    udp_thread = threading.Thread(target=receive_udp_data)
    udp_thread.daemon = True
    udp_thread.start()

    # Run the Flask app with SocketIO
    socketio.run(app, host='0.0.0.0', port=80)
