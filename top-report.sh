#!/bin/bash

# Trap the ctrl+c keyboard event and report it properly.
trap ctrl_c SIGINT

# Getting delay and filename for storing the report.
DELAY=$1
DEFAULT_FILE=top-report.csv
REPORT=${2:-$DEFAULT_FILE}
CLEANEXIT=1
USEREXIT=2
ERROR=-1

function usage() {
    echo "Usage:"
    echo "$0 <Delay for top> <report filename>"
    echo "<Delay for top>   = any integer greater than 1 and less than 10"
    echo "<report filename> = default is top-report.csv, will be created in $PWD"
    echo "                    or provide the filename here."

    exiting $CLEANEXIT
}

function exiting() {
    exit $1
}

function ctrl_c() {
    echo "*** Got Keyboard Interrupt := CTRL-C ***"
    echo "*** Exiting.. "
    # removing the top four lines that prints shared memory and cpu
    # info etc.
    sed -r -i -e '/^(top|Tasks|\%Cpu|KiB)/d' $REPORT
    sed -i '/^PID/d' $REPORT
    sed -i '$ d' $REPORT

    exiting $USEREXIT
}

function store_output() {
    # Squeezing all the spaces in top report and making it comma
    # separated.
    top -d$DELAY -b | tr -s [[:space:]] | sed 's/^[ \t]//' \
	| sed 's/$[ \t]//' | tr ' ' , > $REPORT
}

if [ $# -lt 1 ];then
    echo "Requires atleast argument delay but none given."
    usage
fi

store_output
