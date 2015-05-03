# client.py
import socket

def connect_to_server(host, port):
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connection to hostname on the port.
    client.connect((host, port))

    return client


def main():
    # get local machine name
    host = socket.gethostname()
    port = 2345

    try:
        cli = connect_to_server(host, port)
        # Receive no more than 1024 bytes
        while True:
            data = cli.recv(1024)
            print "Data from server %s\n", data

    finally:
        cli.close()


if __name__ == "__main__":
    main()
