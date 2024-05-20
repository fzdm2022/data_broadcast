from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import socket
import threading

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")  # Specify gevent as the async mode

UDP_IP = "0.0.0.0"  # Listen on all available interfaces
UDP_PORT = 5007

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)  # Increase buffer size

# List to store connected clients
connected_clients = set()

@socketio.on('connect')
def handle_connect():
    # Add client to the list of connected clients
    connected_clients.add(request.sid)
    print(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    # Remove client from the list of connected clients
    connected_clients.remove(request.sid)
    print(f'Client disconnected: {request.sid}')

def broadcast_data(data):
    # Send data to all connected clients
    socketio.emit('data', data)

@app.route('/')
def index():
    return render_template('index.html')

def receive_udp_data():
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            broadcast_data(data.decode('utf-8'))
        except Exception as e:
            print(f"Error receiving data: {e}")

def get_ip_address():
    """Get the local IP address of the server."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    # Start the background thread for receiving UDP data
    udp_thread = threading.Thread(target=receive_udp_data)
    udp_thread.daemon = True
    udp_thread.start()

    # Get the server IP address
    server_ip = get_ip_address()
    print(f"Server is running. Visit http://{server_ip}/ to view the data.")

    # Run the Flask app with SocketIO
    socketio.run(app, host='0.0.0.0', port=80)
