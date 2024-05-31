import socket
import time
from data_generator import RandomDataGenerator

UDP_IP = "255.255.255.255"  # Broadcast IP address
UDP_PORT = 5007

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

dt_generator = RandomDataGenerator(data_type='numbers', length=6)


def get_message():
    t = time.time()
    fmt = time.gmtime(t)
    message = time.strftime("%D, %T", fmt)
    dt = dt_generator.generate_random_data(6)
    message = str(t) + ',' + dt
    return message


while True:

    message = get_message()
    # Send data via UDP broadcast
    sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
    print("send:", message)
    time.sleep(1)

# Close the socket
sock.close()
