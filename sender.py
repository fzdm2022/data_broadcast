import socket
import time

UDP_IP = "255.255.255.255"  # Broadcast IP address
UDP_PORT = 5007

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

i = 0
while True:
    # message = input("Enter message to broadcast (type 'exit' to quit): ")
    t = time.time()
    fmt = time.gmtime(t)
    message = time.strftime("%D, %T", fmt)
    # if message.lower() == 'exit':
    #     break

    # Send data via UDP broadcast
    sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
    print("send:", message)
    time.sleep(2)

# Close the socket
sock.close()