from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.node import CPULimitedHost
from subprocess import os
import sys
import time

numHost_per_Switch = 3
ops_link_cat5e = dict(bw=1, delay='10ms',loss=0,  use_htb=False)
ops_link_fiber = dict(bw=1, delay='10ms', loss=0 , use_htb=False)
class MyTopo (Topo):
    def build(self, n=2):

        switch = self.addSwitch('s2')
        # Python's range(N) generates 0..N-1
        for h in range(n):
        	host = self.addHost('h%s' % (h + 1))
        	self.addLink(host, switch, **ops_link_cat5e)

        switch = self.addSwitch('s3')
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (n + h + 1))
            self.addLink(host, switch, **ops_link_cat5e)

        switch = self.addSwitch('s1')
        self.addLink ('s1', 's2', **ops_link_fiber)
        self.addLink ('s1', 's3', **ops_link_fiber)
        #host = self.addHost('h0')
        #self.addLink(switch,host, **ops_link_fiber)
def ping_allHost_to_ondeHost(hosts):
    print "######------------ping allHosts -> h1 -------------------------"
    for h in hosts:
        if h.name != 'h1' and h.name != 'h2':
            h.cmdPrint("ping 10.0.0.1 -v -c 3")
            print "-------------------------------------"

def ping_oneHost_to_allHosts(host):
    print "\n\n\n########------------ping %s -> allHosts ----------##############" % (host.name)
    for i in range(1,2*numHost_per_Switch+1):
        #if i != 3:
        host.cmdPrint("ping 10.0.0.%d -v -c 4" % (i))
        print "-------------------------------------\n"

def createCongest(server,client):
    print "\n\n\n# Criando congestionamento"

    server.sendCmd("iperf -s")
    client.sendCmd("iperf -c 10.0.0.2 -t 200 ")
    time.sleep(3)


def MainTest():

    os.system("sudo mn -c")
    os.system("clear")
    print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

    topo = MyTopo(n=numHost_per_Switch)
    net = Mininet(topo, link=TCLink,xterms=False)

    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    h1, h2 = net.get('h1','h2')
    createCongest(h2,h1)

    print "\n# Inicio teste congestionamento"
    hosts = net.hosts
    ping_allHost_to_ondeHost(hosts)

    host = net.get('h3')
    ping_oneHost_to_allHosts(host)


    h1.terminate()
    h2.terminate()
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    MainTest()
