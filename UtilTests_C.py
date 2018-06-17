from Topology import *

def ping_allHost_to_ondeHost(hosts):
    print "######------------ping allHosts -> h1 -------------------------"
    for h in hosts:
        if h.name != 'h1' and h.name != 'h2':
            h.cmdPrint("ping 10.0.0.1 -v -c 3")
            print "-------------------------------------"

def ping_oneHost_to_allHosts(host):
    print "\n\n\n########------------ping %s -> allHosts ----------##############" % (host.name)
    for i in range(1,2*numHost_per_Switch+1):
        print "#%s -> h%d" % (host.name, i)
        host.cmdPrint("ping 10.0.0.%d -v -c 4" % (i))
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
    ping_allHost_to_ondeHost(hosts)
    host = net.get('h3')
    ping_oneHost_to_allHosts(host)
    h1.terminate()
    h2.terminate()
    net.stop()
