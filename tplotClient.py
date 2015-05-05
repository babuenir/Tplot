# client.py
import socket

def connect_to_server(host, port):
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connection to hostname on the port.
    client.connect((host, port))

    return client
