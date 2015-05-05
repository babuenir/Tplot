# -*- coding: utf-8 -*-
"""Plotting of top report generated in work bench.

The purpose of this module is to plot the data as a graph/chart for
further analysis.

Usage:
  $ python top-plot.py

"""
import numpy as np
import os
import sys
import argparse
import socket
import matplotlib.pyplot as plt
from tplotClient import connect_to_server

csv_header = ['PID','USER','PR','NI','VIRT','RES','SHR','S','%CPU','%MEM','TIME+','COMMAND']
csv_dtypes = "i8,|S10,|S3,f8,|S5,|S5,|S5,|S5,f8,f8,|S10,|S10"

def get_data(filename, header, dtypes):
    """ get_data function of module top-plot.

    This function yields the array of data for each of the fields in csv
    header.

    Args:
      filename - Name of the csv file to be plotted.
      header   - list of columns/field in the csv header.
      dtypes   - The type of each field in the csv header.

    Returns:
      pltdata  - data as numpy data array.

    """
    pltdata = np.genfromtxt(filename, delimiter=',', names=header, dtype=dtypes)

    pid = pltdata['PID']
    user = pltdata['USER']
    pr = pltdata['PR']
    ni = pltdata['NI']
    virt = pltdata['VIRT']
    res = pltdata['RES']
    shr = pltdata['SHR']
    s = pltdata['S']
    cpu = pltdata['CPU']
    mem = pltdata['MEM']
    t = pltdata['TIME']
    cmd = pltdata['COMMAND']

    pdata = [pid, user, pr, ni, virt, res, shr, s, cpu, mem, t, cmd]

    return pltdata, pdata


def parse_data(data, field, entries, item):
    """parse_data function of module top-plot.

    splits into different data from the data taken from csv file.

    Args:
      data  - csv data from the file.
      field - field to be processed.
      item  - item to be compared.

    Returns:
      dlist - list of parsed data.

    """

    if item in data['COMMAND']:
        ifield = 'COMMAND'
    elif item in data['USER']:
        ifield = 'USER'
    elif int(item) in data['PID']:
        item = int(item)
        ifield = 'PID'

    plist = [piece for piece in enumerate(data[ifield])]

    if field is not 'TIME':
        for pitem in plist:
            if pitem[1] == item:
                entries.append(pitem[0])

    dlist = [data[field].item(x) for x in entries]

    if type(dlist[0]) is str:
        axis = [ax[0] for ax in enumerate(dlist)]
        plt.xticks(axis, dlist, rotation=45)
    else:
        axis = dlist

    return entries, axis


def plot_graphic(x, y, gtype):
    plt.plot(x, y, '-', x, y, gtype)
    plt.draw()


def option_parser():
    """option_parser function of module top-plot.

    This function parses the arguments passed to the module.

    Args:
      None.

    Returns:
      dict: commandline arguments.

    """
    parser = argparse.ArgumentParser(
        description="Plotting of top report generated in work bench.")
    parser.add_argument('-f', '--filename',
                        dest='filename',
                        default='top-report.csv',
                        help='The filename from which plot to be generated.')
    parser.add_argument('-y', '--yfield',
                        dest='yfield',
                        default='CPU',
                        choices=['VIRT', 'RES', 'SHR', 'MEM', 'CPU'],
                        help='The fields to be used for y axis.')
    parser.add_argument('-x', '--xfield',
                        dest='xfield',
                        default='TIME',
                        choices=['PID', 'COMMAND', 'TIME'],
                        help='The fields to be used for x axis.')
    parser.add_argument('-i', '--item',
                        dest='item',
                        required=True,
                        help='The item to be parsed.')

    args = parser.parse_args()

    return args


def main():
    """main function of module top-plot.

    The main entry for getting the data and plotting the data of any two
    fields.

    """

    options = option_parser()

    fname = options.filename
    xfld = options.xfield
    yfld = options.yfield
    itm  = options.item
    aentry = []

    plt.xlabel(xfld)
    plt.ylabel(yfld)
    plt.title("%s vs %s for %s" %(xfld,yfld,itm))

    if os.path.exists(fname):
        data, pdata = get_data(fname, csv_header, csv_dtypes)
        yentry, yplot = parse_data(data, yfld, aentry, itm)
        xentry, xplot = parse_data(data, xfld, yentry, itm)

        plot_graphic(xplot, yplot, 'ro')

    else:
        print "%s File not found" % fname
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

            data = data.split('END')[0]

            yentry, yplot = parse_data(data, yfld, aentry, itm)
            xentry, xplot = parse_data(data, xfld, yentry, itm)

            plot_graphic(xplot, yplot, 'ro')

        cli.close()



if __name__ == "__main__":
    main()
