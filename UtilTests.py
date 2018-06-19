from Topology import *

def ping_allHost_to_oneHost(hosts, hostIP, numPacket=4):
    setLogLevel('info')
    print "######------------ping allHosts -> h1 -----------------##############"
    print hostIP
    for h in hosts:
        if h.name != 'h1' and h.name != 'h2':
            h.cmdPrint("ping %s -v -c %d" % (hostIP,numPacket))
            print "-------------------------------------"
    setLogLevel()

def ping_oneHost_to_allHosts(host,hosts,numPacket=4):
    setLogLevel('info')
    print "\n\n########------------ping %s -> allHosts ----------##############" % (host.name)
    i = 0
    for h in hosts:
        i += 1
        print "# %s -> %s" % (host.name, h.name)
        host.cmdPrint("ping 10.0.0.%d -v -c %d" % (i,numPacket))
        print "-------------------------------------\n"
    setLogLevel()

def ping_Host_to_Host(host1,hostIP,numPacket=4):
    setLogLevel('info')
    print "\n\n########------------ping %s -> %s ----------##############" % (host1.name,hostIP)
    host1.cmdPrint("ping %s -v -c %d" % (hostIP,numPacket))
    print "-------------------------------------\n"
    setLogLevel()


def createCongest(server,client):
    print "\n\n# Creating congestion"
    server.sendCmd("iperf -s")
    client.sendCmd("iperf -u -c 10.0.0.2 -t 200 ")
    time.sleep(3)


def CongestionTest():
    setLogLevel()
    topo = MyTopo(n=numHost_per_Switch)
    net = Mininet(topo, link=TCLink,xterms=False)
    net.start()
    h1, h2 = net.get('h1','h2')
    createCongest(h2,h1)
    print "\n# Start test congestion"
    hosts = net.hosts
    hostTest = net.get('h3')
    hostIP = "10.0.0.1"
    
    ping_oneHost_to_allHosts(hostTest, hosts)

    ping_allHost_to_oneHost(hosts,hostIP)

    h1.terminate()
    h2.terminate()
    net.stop()

def ForwardingErrorTest():
    setLogLevel()
    topo = MyTopo(n=numHost_per_Switch)
    h_broken = topo.addHost('h_broken')
    ops_link['loss'] = 30
    topo.addLink('s2',h_broken, **ops_link)
    net = Mininet(topo, link=TCLink)
    net.start()
    #print "Dumping host connections"
    #dumpNodeConnections(net.hosts)

    print "# End of creation network \n\n\n\n\n"
    print "\n# Start test Forwarding Error\n"
    host = net.get('h3')
    hosts = net.hosts
    ping_oneHost_to_allHosts(host,hosts,8)
    net.stop()

def Bandwidth1():
    setLogLevel()
    print "================== FIRST TEST ====================================="
    topo = MyTopo(n=numHost_per_Switch)
    net = Mininet(topo, link=TCLink)
    net.start()
    h1, h2 = net.get('h1','h2')

    createCongest(h2,h1)

    print "\n# Start test congestion"
    hostTest = net.get('h3')
    hostIP = "10.0.0.1"
    print "# bw = %s Mb" % (ops_link['bw'])
    ping_Host_to_Host(hostTest,hostIP)
    h1.terminate()
    h2.terminate()
    net.stop()

    print "================== SECOND TEST ====================================="

    os.system("sudo mn -c")
    ops_link['bw'] = 100
    topo = MyTopo(n=numHost_per_Switch)
    net = Mininet(topo, link=TCLink)
    net.start()
    h1, h2 = net.get('h1','h2')

    createCongest(h2,h1)

    print "\n# Start test congestion"
    hostTest = net.get('h3')
    hostIP = "10.0.0.1"
    print "# bw = %s Mb" % (ops_link['bw'])
    ping_Host_to_Host(hostTest,hostIP)
    h1.terminate()
    h2.terminate()
    net.stop()

def Bandwidth2():
    setLogLevel()

    print "# bw = %s Mb" % (ops_link['bw'])
    topo = MyTopo(n=numHost_per_Switch)
    net = Mininet(topo, link=TCLink, xterms = False, cleanup = True, waitConnected = True)
    net.start()
    h_rcv, h_server = net.get('h1','h2')
    h_test = net.get('h3')

    setLogLevel('info')
    print "================== TEST PATHLOAD ==================================="

    h_test.sendCmd("./../../pathload_1.3.2/pathload_snd ")
    h_rcv.cmdPrint("./../../pathload_1.3.2/pathload_rcv -s 10.0.0.3 -o test1.log ")


    setLogLevel()

    h_server.terminate()
    h_rcv.terminate()
    h_test.terminate()


    os.system("sudo mn -c")
    os.system("clear")


    print "# bw = %s Mb" % (ops_link['bw'])
    topo = MyTopo(n=numHost_per_Switch)
    net = Mininet(topo, link=TCLink, xterms = False, cleanup = True, waitConnected = True)
    net.start()
    h_rcv, h_server = net.get('h1','h2')
    h_test = net.get('h3')

    setLogLevel('info')
    print "\n==================  TEST PATHLOAD  ========CONGESTIONADO==========================="

    h_test.sendCmd("./../../pathload_1.3.2/pathload_snd ")
    h_server.sendCmd ("iperf -s")
    h_rcv.cmdPrint("iperf -c 10.0.0.2 -t 200 >> iperftest1.txt & ./../../pathload_1.3.2/pathload_rcv -s 10.0.0.3 -o test1_c.log ")


    h_server.terminate()
    h_rcv.terminate()
    h_test.terminate()
    net.stop()
