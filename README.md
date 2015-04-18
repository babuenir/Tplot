Tplot
=====

Tplot is a python and shell mixed package that plots the data gathered
from top as a graph/chart for further analysis.

The data can be collected from one machine and plotted on other
machine. Basically intended to test and analyse the performance of
embedded systems.

A typical setup would be running the shell script to gather
information from the embedded Linux machine and plotting it to a
decent graph using python program in development machine. But both the
machines can be the same.

Usage
-----

In embedded Linux machine,

	$ ./top-report.sh <Delay for top> <report filename>

	<Delay for top> = any integer greater than 1 and less than 10
	<report filename> = default is top-report.csv, will be created in
		$PWD or provide the filename here.

The above command will generate a csv file containing typical top
output, the process related information in comma separated format,
which is needed by the plotter python program.

In development Linux machine,


	$ python top-plot.py [-h] [-f FILENAME] [-y {VIRT,RES,SHR,MEM,CPU}]
		[-x {PID,COMMAND,TIME}] -i ITEM

	Plotting of top report generated in work bench.

	optional arguments:
		-h, --help            show this help message and exit
		-f FILENAME, --filename FILENAME
			The filename from which plot to be generated.
		-y {VIRT,RES,SHR,MEM,CPU}, --yfield {VIRT,RES,SHR,MEM,CPU}
			The fields to be used for y axis.
		-x {PID,COMMAND,TIME}, --xfield {PID,COMMAND,TIME}
			The fields to be used for x axis.
		-i ITEM, --item ITEM  The item to be parsed.

The above command takes the csv file generated from shell script and
plots the field it is passed with.
