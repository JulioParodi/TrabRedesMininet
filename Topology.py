from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.node import CPULimitedHost
from subprocess import os
import sys
import time
from UtilTests import *

numHost_per_Switch = 3
ops_link = dict(bw=1, delay='10ms',loss=0)
#ops_link_fiber = dict(bw=1, delay='10ms', loss=0 , use_htb=False)

class MyTopo (Topo):
    def build(self, n=2):

        switch = self.addSwitch('s2')

        for h in range(n):
        	host = self.addHost('h%s' % (h + 1))
        	self.addLink(host, switch, **ops_link)

        switch = self.addSwitch('s3')

        for h in range(n):
            host = self.addHost('h%s' % (n + h + 1))
            self.addLink(host, switch, **ops_link)

        switch = self.addSwitch('s1')
        self.addLink ('s1', 's2', **ops_link)
        self.addLink ('s1', 's3', **ops_link)


def help():
    print "use command line:"
    print "sudo python Topology.py [-c or -h]"
    print "-c = test congestion"
    print "-h = help\n"

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    os.system("sudo mn -c")
    os.system("clear")
    print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    if len(sys.argv)==2 and sys.argv[1] == '-c':
        CongestionTest()
    elif len(sys.argv)==2 and sys.argv[1] == '-f':
        ForwardingErrorTest()
    elif len(sys.argv)==2 and sys.argv[1] == '-h':
        help()
    else:
        help()

    os.system("rm -f *pyc")
