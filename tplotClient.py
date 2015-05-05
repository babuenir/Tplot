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
    port = 9999

    cli = connect_to_server(host, port)

    while True:
       # Receive no more than 1024 bytes
       data = cli.recv(1024)
       reply = 'OK'

       if not data:
           break

       print data
       #cli.sendall(reply)

    cli.close()


if __name__ == "__main__":
    main()
