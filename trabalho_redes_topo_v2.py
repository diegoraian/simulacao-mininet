#!/usr/bin/python
#
#
#
#
#
#
#
# ARQUIVO GERADO PELO MINIEDIT
#
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None, build=False)
                     
    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',controller=RemoteController,protocol='tcp',port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.10.1.1')
    h2 = net.addHost('h2', cls=Host, ip='10.10.1.2')
    h3 = net.addHost('h3', cls=Host, ip='10.10.1.3')
    h4 = net.addHost('h4', cls=Host, ip='10.10.2.1')
    h5 = net.addHost('h5', cls=Host, ip='10.10.2.2')
    h6 = net.addHost('h6', cls=Host, ip='10.10.2.3')
    h7 = net.addHost('h7', cls=Host, ip='10.10.3.1')
    h8 = net.addHost('h8', cls=Host, ip='10.10.3.2')
    h9 = net.addHost('h9', cls=Host, ip='10.10.3.3')

    info( '*** Add links\n')
    #Links entre hosts subrede 1 e S1
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    #Links entre hosts subrede 2 e S2
    net.addLink(h4, s2)
    net.addLink(h5, s2)
    net.addLink(h6, s2)
    #Links entre hosts subrede 3 e S3
    net.addLink(h7, s3)
    net.addLink(h8, s3)
    net.addLink(h9, s3)
    #Links entre switches
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s2, s3)
      

    info( '*** Starting network\n')
    #Inicializa rede
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()
    
    info( '*** Starting switches\n')
    #Controladores associados a cada switch (nesse caso 'c0')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])

    info( '*** Post configure switches and hosts\n')
    ##FORs encadeados para adicionar rotas (default) e setar valores ARP(IP,MAC) nas tabelas ARP de cada host
    for i in xrange(9):
      h = net.get('h%d' % (i + 1))
      h.cmd("ip route add default dev %s-eth0" % ('h%d' % (i + 1)))
      for j in xrange(9):
        h_dst = net.get('h%d' % (j+1))
        h.setARP(h_dst.IP(), h_dst.MAC())
      print 'h%d ARP configurado'%(i+1)  
            
    #Inicializa a Command-Line Interface (CLI) da network "net"        
    CLI(net)
    net.stop()   

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

