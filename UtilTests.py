from Topology import *

def ping_allHost_to_oneHost(hosts, host, numPacket=4):
    print "######------------ping allHosts -> h1 -------------------------"
    for h in hosts:
        if h.name != 'h1' and h.name != 'h2':
            h.cmdPrint("ping %s -v -c %d" % (host.IP,numPacket))
            print "-------------------------------------"

def ping_oneHost_to_allHosts(host,hosts,numPacket=4):
    print "\n\n\n########------------ping %s -> allHosts ----------##############" % (host.name)
    i = 0
    for h in hosts:#range(1,2*numHost_per_Switch+1):
        i += 1
        print "# %s -> %s" % (host.name, h.name)
        print "ping 10.0.0.%d -v -c 4" % (i)
        host.cmdPrint("ping 10.0.0.%d -v -c %s" % (i,numPacket))
        print "-------------------------------------\n"

def createCongest(server,client):
    print "\n\n\n# Creating congestion"
    server.sendCmd("iperf -s")
    client.sendCmd("iperf -c 10.0.0.2 -t 200 ")
    time.sleep(3)


def CongestionTest():

    topo = MyTopo(n=numHost_per_Switch)
    net = Mininet(topo, link=TCLink,xterms=False)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "# End of creation network "
    h1, h2 = net.get('h1','h2')
    createCongest(h2,h1)
    print "\n# Start test congestion"
    hosts = net.hosts
    ping_allHost_to_oneHost(hosts)
    host = net.get('h3')
    ping_oneHost_to_allHosts(host)
    h1.terminate()
    h2.terminate()
    net.stop()

def ForwardingErrorTest():
    topo = MyTopo(n=numHost_per_Switch)
    h_broken = topo.addHost('h_broken')
    ops_link['loss'] = 20

    topo.addLink('s2',h_broken, **ops_link)
    net = Mininet(topo, link=TCLink,xterms=False)


    net.start()
    #print "Dumping host connections"
    #dumpNodeConnections(net.hosts)
    print "# End of creation network "
    print "\n# Start test\n"
    #net.pingAll()
    host = net.get('h3')
    hosts = net.hosts
    ping_oneHost_to_allHosts(host,hosts,8)

    net.stop()
