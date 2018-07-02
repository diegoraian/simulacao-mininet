#!/usr/bin/python

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

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.10.0.0/16')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h2 = net.addHost('h2', cls=Host, ip='10.10.1.2', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.10.2.1', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.10.2.2', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='10.10.3.3', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.10.1.1', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.10.2.3', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.10.1.3', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.10.3.2', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.10.3.1', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(h3, s1)
    net.addLink(h2, s1)
    net.addLink(h1, s1)
    net.addLink(h4, s2)
    net.addLink(h5, s2)
    net.addLink(h6, s2)
    net.addLink(h7, s3)
    net.addLink(h8, s3)
    net.addLink(h9, s3)
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s2, s3)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
