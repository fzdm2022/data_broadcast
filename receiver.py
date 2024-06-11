from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import socket
import threading
import time
from data_container import DaqQueue

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

UDP_IP = "0.0.0.0"
UDP_PORT = 5007

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)  # Increase buffer size
sock.setblocking(False)  # Set socket to non-blocking

latest_data = ""

if_log = False
logfile = None
dtQueue = DaqQueue(size=[1000, 6])


@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')


@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')


def broadcast_data(data):
    global latest_data
    latest_data = data
    socketio.emit('data', data)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/latest_data', methods=['GET'])
def get_latest_data():
    return jsonify({"data": latest_data})


def receive_udp_data():
    if if_log:
        logfile = initial_logging()
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if data:
                decoded_data = data.decode('utf-8')
                broadcast_data(decoded_data)
                if if_log:
                    logfile.write(f"{time.time()} - {decoded_data}\n")
                    logfile.flush()

        except BlockingIOError:
            pass


def initial_logging():
    log_file = open(f"log_{time.strftime('%Y%m%d_%H%M%S')}.log", 'a')
    return log_file


def get_ip_address():
    """Get the local IP address of the server."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


if __name__ == '__main__':
    udp_thread = threading.Thread(target=receive_udp_data)
    udp_thread.daemon = True
    udp_thread.start()

    server_ip = get_ip_address()
    print(f"Server is running. Visit http://{server_ip}/ to view the data.")

    socketio.run(app, host='0.0.0.0', port=80)
