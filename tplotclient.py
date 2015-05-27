# client.py
import socket


def connect_to_server(host, port):
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connection to hostname on the port.
    client.connect((host, port))

    return client


def receive(client, size):
    # Receive no more than 1024 bytes
    data = client.recv(size)
    reply = 'OK'

    data = data.split('END')[0]

    return data


def main():
    host = socket.gethostname()
    port = 9999

    cli = connect_to_server(host, port)

    while True:
        csvline = receive(cli, 1024)

        if not csvline:
            break

        print csvline

    cli.close()


if __name__ == "__main__":
    main()
