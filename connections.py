"""Factory of connections between client and server.

There are different ways a connection can be established between the
system that analyses the performance of a system and the system that is
being analysed. Both can be the same system as well as different
systems. This factory allows us to make connections accordingly.
"""

import termios, os, sys, socket


class TplotConn(object):
    """Connection factory creator for tplot data communication.

    This creates an instance of a connection to be established, controls
    the connection and what has to be the connection parameters.
    """

    def __init__(self):
        self.serialport = sys.stdout.fileno()
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREA)

    def create_server(self):
        path = '/sys/class/net/'
        self.ifaces = os.listdir(path)

        if ifaces:
            for iface in ifaces:
                try:
                    iface = open(path + iface + '/carrier', 'r')
                    if int(iface.readline().splitlines()[0]) == 1:
                        host = socket.gethostbyname(socket.gethostname())
                        port = 9999
                        self.serversock.bind((host, port))
                        self.serversock.listen(5)
                except e as IOError:
                    print "Falling back to serial port"

        else:
            oldtc = termios.tcgetattr(self.serialport)
            newtc = termios.tcgetattr(self.serialport)
            new[3] = new[3] & ~termios.ECHO
            try:
                termios.tcsetattr(self.serialport, termios.TCSADRAIN, newtc)
            finally:
                termios.tcsetattr(self.serialport, termios.TCSADRAIN, oldtc)

    def send_data(self, client, data):

        client.send(datastr + 'END')

    def close_connection(sock):
        sock.close()
