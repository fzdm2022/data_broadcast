from flask import Flask, render_template, jsonify
import socket

app = Flask(__name__)

UDP_IP = "0.0.0.0"  # Listen on all available interfaces
UDP_PORT = 5005


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def get_data():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    # Receive UDP broadcast data
    data, addr = sock.recvfrom(1024)

    # Close the socket
    sock.close()

    return jsonify({'data': data.decode('utf-8')})


if __name__ == '__main__':
    app.run(debug=True)