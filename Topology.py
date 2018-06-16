from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class MyTopo(Topo):
    "Single switch connected to n hosts."
    ops_link_cat5e = dict(bw=100, delay='10ms', loss=10, max_queue_size=1000, use_htb=True)
    ops_link_fiber = dict(bw=1000, delay='5ms', loss=2, max_queue_size=1000, use_htb=True)
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


def simpleTest():
    "Create and test a simple network"
    topo = MyTopo(n=10)
    net = Mininet(topo)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()