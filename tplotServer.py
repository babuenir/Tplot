import glob
import os
import socket
import csv
import procParse
from procParse import procParser


def create_server():
    # creating a server socket object for a connection.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    # port is 2345 for convenience.
    port = 9999
    server.bind((host, port))
    server.listen(5)

    return server


def close_connection(sock):
    # Closing sock connection on exit gracefully.
    sock.close()


def send_data(client, data):
    datastr = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (data.pid,
                                                       data.user,
                                                       data.pr,
                                                       data.ni,
                                                       data.vir,
                                                       data.res,
                                                       data.shr,
                                                       data.S,
                                                       data.cpu,
                                                       data.mem,
                                                       data.tm,
                                                       data.cmd)
    client.send(datastr + 'END')


def main():
    srv = create_server()
    ps = procParse.procStat('proc')

    # establish a connection
    cli, addr = srv.accept()
    print("Got a connection from %s" % str(addr))

    while True:
        # send parsed data here.
        for fp in glob.glob('/proc/[0-9]*/'):
            if os.path.exists(fp):
                topcsv = procParser(ps, fp)
                send_data(cli, topcsv)


if __name__ == "__main__":
    main()
