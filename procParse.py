"""Parse procfs and create csv formatted output like top.

top command provides a very detailed information about a process's
memory utilization, cpu usage, uptime, id and user. These are taken
from a virtual filesystem in Linux called procfs. Here this virtual
filesystem is utilized to the fullest to fetch every single detail
close to top.
"""

import os
import pwd
from collections import namedtuple


class procStat:
    # The class instance for the parser object.
    def __init__(self, name):
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

        self.data =  namedtuple('Psdata',
                                'pid user pr ni vir res shr S cpu mem tm cmd')

        self.pgsize = os.sysconf(os.sysconf_names['SC_PAGE_SIZE'])
        self.hz = os.sysconf(os.sysconf_names['SC_CLK_TCK'])

    def get_proclist(self, fp):
        with open(fp) as infile:
            proclist = infile.read()
            self.proclist = proclist.splitlines()[0].split(' ')

        return self.proclist

    def get_procdata(self, proclist, field=0):
        if type(field) is int:
            self.procdata = int(proclist[field])
        elif field == 'state' or field == 'comm':
            field_id = self.statfld.index(field)
            self.procdata = proclist[field_id]
        else:
            field_id = self.statfld.index(field)
            self.procdata = int(proclist[field_id])

        return self.procdata

    def mem_in_bytes(self, pages):
        self.memory = self.pgsize * pages

        return self.memory

    def get_user(self, path):
        for ln in open(path):
            if ln.startswith('Uid:'):
                uid = int(ln.split()[1])

        self.user = pwd.getpwuid(uid).pw_name

        return self.user

    def sizeof_fmt(self, num):
        for unit in ['','K','M','G','T','P','E','Z']:
            if abs(num) < 1024.0:
                return "%3.1f%s" % (num, unit)
            num /= 1024.0
        return "%.1f%s" % (num, 'Y')


def procParser(procstat, path):
    proclist = procstat.get_proclist(path + 'stat')
    userpath = path + 'status'
    shr_mem  = procstat.get_proclist(path + 'statm')
    uptime   = procstat.get_proclist(path + '../uptime')
    procstat.data.pid   = procstat.get_procdata(proclist, 'pid')
    procstat.data.user  = procstat.get_user(userpath)
    procstat.data.pr    = procstat.get_procdata(proclist, 'priority')
    procstat.data.ni    = procstat.get_procdata(proclist, 'nice')
    vir                 = procstat.get_procdata(proclist, 'vsize')
    procstat.data.vir   = procstat.sizeof_fmt(vir)
    procstat.data.res   = procstat.get_procdata(proclist, 'rss')
    shr                 = procstat.get_procdata(shr_mem, 2)
    procstat.data.shr   = procstat.sizeof_fmt(procstat.mem_in_bytes(shr))
    procstat.data.S     = str(procstat.get_procdata(proclist, 'state'))
    utime               = procstat.get_procdata(proclist, 'utime')
    stime               = procstat.get_procdata(proclist, 'stime')
    cutime              = procstat.get_procdata(proclist, 'cutime')
    cstime              = procstat.get_procdata(proclist, 'cstime')
    procstat.data.tm    = utime
    cmd                 = str(procstat.get_procdata(proclist, 'comm'))
    procstat.data.cmd   = cmd[cmd.index("(") + 1:cmd.rindex(")")]
    starttime           = procstat.get_procdata(proclist, 'starttime')
    total_time          = utime + stime + cutime + cstime
    uptime              = float(format(float(uptime[0]), '.2f'))
    seconds             = uptime - (starttime / procstat.hz)
    procstat.data.cpu   = 100 * ((total_time / procstat.hz) / seconds)
    procstat.data.mem   = 0 # FIXME

    return procstat.data
