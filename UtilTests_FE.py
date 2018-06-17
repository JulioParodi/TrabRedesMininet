from Topology import *


def ForwardingErrorTest():
    #ops_link['loss'] = 10
    topo = MyTopo(n=numHost_per_Switch)
    net = Mininet(topo, link=TCLink,xterms=False)

    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "# End of creation network "

    print "\n# Start test"
    print ops_link

    hosts = net.hosts
    #ping_allHost_to_ondeHost(hosts)
    host = net.get('h3')
    ping_oneHost_to_allHosts(host)

    net.stop()
