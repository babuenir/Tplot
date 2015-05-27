"""Parse procfs and create yml formatted output like top.

top command provides a very detailed information about a process's
memory utilization, cpu usage, uptime, id and user. These are taken from
a virtual filesystem is utilized to the fullest to fetch every single
detail close to top.
"""

import os
import pwd


class ProcStat(object):
    """The Class instance for the procparser object.

    Produces a procparser object which has the data about each process
    in a dictionary and the system uptime.
    """

    fields = ['pid', 'user', 'priority', 'nice', 'vsize', 'rss',
              'shared_mem', 'state', 'cpu', 'mem', 'time', 'comm']
    data = {}
    uptime = None

    def __init__(self, name):
        """Initialization of procparser object.

        Takes one argument name for the parser. Initializes the name,
        pagesize from system, hertz from the system, proclist, procdata
        and data parsed from the procps subsystem of Linux.
        """
        self.name = name
        self.statfld = ['pid', 'comm', 'state', 'ppid', 'pgrp',
                        'session', 'tty_nr', 'tpgid', 'flags',
                        'minflt', 'cminflt', 'majflt', 'cmajflt',
                        'utime', 'stime', 'cutime', 'cstime',
                        'priority', 'nice', 'num_threads',
                        'itrealvalue', 'starttime', 'vsize', 'rss',
                        'rsslim', 'startcode', 'endcode',
                        'startstack', 'kstkesp', 'kstkeip', 'signal',
                        'blocked', 'sigignore', 'sigcatch', 'wchan',
                        'nswap', 'cnswap', 'exit_signal', 'processor',
                        'rt_priority', 'policy',
                        'delayacct_blkio_ticks', 'guest_time',
                        'cguest_time']

        # Get the pagesize from the system.
        self.pagesize = os.sysconf(os.sysconf_names['SC_PAGE_SIZE'])
        # Get the ticks/sec from the system.
        self.hertz = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
        self.proclist = None
        self.procdata = None
        for field in self.fields:
            self.data[field] = None

    def get_proclist(self, infile):
        """get_proclist method for parsing all the files in procfs.

        Takes filepath as argument. Returns the processed data as list.
        """
        with open(infile) as fileptr:
            proclist = fileptr.read()
            self.proclist = proclist.splitlines()[0].split()

        return self.proclist

    def get_procdata(self, proclist, field=0):
        """get_procdata method for parsing out the data from the list.

        Takes proclist and field as arguments, proclist generated out
        from the file. Returns the specific data based on the field.
        """
        if type(field) is int:
            self.procdata = int(proclist[field])
        elif type(field) and field == 'state' or field == 'comm':
            # get the index of the field and get the data.
            field_id = self.statfld.index(field)
            self.procdata = proclist[field_id]
        else:
            field_id = self.statfld.index(field)
            self.procdata = int(proclist[field_id])

        return self.procdata

    def mem_in_bytes(self, pages):
        """mem_in_bytes method for converting pages to bytes.

        Takes pages and returns the size in bytes.
        """
        return self.pagesize * pages


def get_user(path):
    """get_user method for getting the user running that process.

    Takes the path as /proc/[pid]/status. Returns the username.
    """
    for line in open(path):
        if line.startswith('Uid:'):
            uid = int(line.split()[1])

    return pwd.getpwuid(uid).pw_name


def sizeof_fmt(num):
    """sizeof_fmt method for converting bytes to corresponding scale.

    Takes the number of bytes. Returns the converted with unit.
    """
    for unit in ['', 'k', 'm', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s" % (num, unit)
        num /= 1024.0
    return "%.1f%s" % (num, 'Y')


def proctime(procstat, proclist, uptime):
    """proctime method to calculate cpu usage of each process.

    Calculates the following,

    * time spent by the process in user context.
    * time spent by the process in kernel context.
    * time spent by the process idle or waited to be scheduled by the
    process in user context.
    * time spent by the process idle or waited to be scheduled by the
    process in kernel.
    * uptime of the system.
    * total_time of the process, seconds etc.,

    Takes procparser object, proclist and path as arguments. Returns
    time of the process, total_time and seconds.
    """
    utime = procstat.get_procdata(proclist, 'utime')
    stime = procstat.get_procdata(proclist, 'stime')
    cutime = procstat.get_procdata(proclist, 'cutime')
    cstime = procstat.get_procdata(proclist, 'cstime')

    time = float(format(float(utime), '.2f'))
    starttime = procstat.get_procdata(proclist, 'starttime')
    total_time = utime + stime + cutime + cstime

    seconds = uptime - (starttime / procstat.hertz)

    return time, total_time, seconds


def procparser(procstat, path):
    """procparser method of the module procparser.

    Consolidates all the data and stores them based on the field name to
    a dict available in the procparser object.

    Takes procparser object and path as arguments. Returns uptime and
    the dict data.
    """
    proclist = procstat.get_proclist(path + 'stat')
    shr_mem = procstat.get_proclist(path + 'statm')

    uptime = procstat.get_proclist(path + '../uptime')
    procstat.uptime = float(format(float(uptime[0]), '.2f'))

    time, total_time, seconds = proctime(procstat, proclist,
                                         procstat.uptime)

    cpu_usage = 100 * ((total_time / procstat.hertz) / seconds)
    cpu_usage = float(format(float(cpu_usage), '.2f'))

    for field in procstat.data.keys():
        if field == 'shared_mem':
            procstat.data[field] = procstat.get_procdata(shr_mem, 2)
        elif field == 'cpu':
            procstat.data[field] = cpu_usage
        elif field == 'user':
            procstat.data[field] = get_user(path + 'status')
        elif field == 'time':
            procstat.data[field] = time
        elif field == 'mem':
            # FIXME: memory consumption by the process needs to be calculated
            # and updated.
            pass
        else:
            procstat.data[field] = procstat.get_procdata(proclist, field)

    return procstat.data, procstat.uptime
