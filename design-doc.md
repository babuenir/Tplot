# Design document for Tplot

Documentation for the design of Tplot, a split program, kind of
inspired from the GDB server and client model. Tplot is a similar
program, which can be used to analyze and understand the live
performance of any of the target machine intended to be plotted as a
graph.


## Initial Design and assumptions

It is initially designed to get the performance data from top report
as a comma separated data using a shell script. This was done in an
assumption that there wouldn't be any heavy Python modules or even
Python at all in the target machine. But as world getting revolved
around Python language for application development, it is wiser to
adapt the same in our design. So here the assumptions are, Python will
be present in the Embedded Linux systems that we are trying to
analyze. And as it is a Linux system there should be a proc filesystem
handling all the process related information in a nice detailed
format. This is pretty much the key things for our design.


## Sockets and procfs

TCP sockets are one of the wonderful entities of Linux systems. We can
create and play around them whenever we want.

*procfs* is another outcome of the virtual filesystems in Linux, which
allows the users to get all that they want from the system. About
processor, devices, commands, process informations and every single
detail like resources they use.


## Server and Client

  * A server program that runs in the Embedded Linux system / Target
    system.

  * The server program will parse the proc filesystem and gather the
    details about the processes running in the system and their
    resource consumptions.

  * It creates a socket connection, binds and listens over a tcp
    port. Once a connection is established from a client program, it
    will send this parsed data at an interval.

  * A client program that runs in the development Linux system / Host
    system.

  * This client program connects to the server in target system and
    receives the raw data.

  * The raw data is processed and plotted in the host system. This way
    the live performance analysis is done.


## Further tasks

  * Versioning scheme need to be introduced. Mostly adhere to semantic
	versioning scheme.

  * Changelog for each revision needs to be added.

  * Unittest cases are to be developed.

  * PEP8, Pylint and coverage are to be done for compliance.

  * Need to schedule for tagging.

  * The plot data has to be drawn instead of showing for continuous
    plotting of data. The data will be as of now CSV. CSV is simple
    yet powerful.

  * Need to add Travis CI for continuous build.

  * Packaging using setuptools have to be done.
