#!/usr/bin/env python

kube_description= \
"""
RCR Deployment
"""
kube_instruction= \
"""
Author: Jon Larrea
"""


import geni.portal as portal
import geni.rspec.pg as PG
import geni.rspec.igext as IG


pc = portal.Context()
rspec = PG.Request()


# Profile parameters.
pc.defineParameter("Hardware", "Machine Hardware",
                   portal.ParameterType.STRING,"d430",[("d430","d430"),("d710","d710"), ("d820", "d820"), ("pc3000", "pc3000")])
pc.defineParameter("nodes", "Number of RCR nodes",
                   portal.ParameterType.INTEGER, 1)
pc.defineParameter("token", "GitHub Token",
                   portal.ParameterType.STRING, "")


params = pc.bindParameters()

#
# Give the library a chance to return nice JSON-formatted exception(s) and/or
# warnings; this might sys.exit().
#
pc.verifyParameters()



tour = IG.Tour()
tour.Description(IG.Tour.TEXT,kube_description)
tour.Instructions(IG.Tour.MARKDOWN,kube_instruction)
rspec.addTour(tour)


# Network
netmask="255.255.255.0"
network = rspec.Link("Network")
network.link_multiplexing = True
network.vlan_tagging = True
network.best_effort = True

# RCR Nodes
for i in range(0,params.nodes):
    node = rspec.RawPC("node" + str(i+1))
    node.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
    node.addService(PG.Execute(shell="bash", command="/local/repository/scripts/setup.sh " + params.token))
    node.hardware_type = params.Hardware
    iface = node.addInterface()
    iface.addAddress(PG.IPv4Address("192.168.1."+str(i+1), netmask))
    network.addInterface(iface)

i+=1

# Client machine
client = rspec.RawPC("client")
client.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
client.addService(PG.Execute(shell="bash", command="/local/repository/scripts/setup.sh " + params.token))
client.hardware_type = params.Hardware
iface = client.addInterface()
iface.addAddress(PG.IPv4Address("192.168.1."+str(i+1), netmask))
network.addInterface(iface)


#
# Print and go!
#
pc.printRequestRSpec(rspec)