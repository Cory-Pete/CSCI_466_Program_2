'''
Created on Oct 12, 2016

@author: Cory Petersen, Austin Johnson
'''
import network_2
import link_2
import threading
from time import sleep

##configuration parameters
router_queue_size = 0  # 0 means unlimited
simulation_time = 4  # give the network sufficient time to transfer all packets before quitting

if __name__ == '__main__':
    object_L = []  # keeps track of objects, so we can kill their threads
    # create network nodes
    client = network_2.Host(1)
    object_L.append(client)
    server = network_2.Host(2)
    object_L.append(server)
    router_a = network_2.Router(name='A', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(router_a)

    # create a Link Layer to keep track of links between network nodes
    link_layer = link_2.LinkLayer()
    object_L.append(link_layer)

    # add all the links
    link_layer.add_link(link_2.Link(client, 0, router_a, 0, 50))
    link_layer.add_link(link_2.Link(router_a, 0, server, 0, 30)) #updated to 30 in accordance to problem

    # start all the objects
    thread_L = []
    thread_L.append(threading.Thread(name=client.__str__(), target=client.run))
    thread_L.append(threading.Thread(name=server.__str__(), target=server.run))
    thread_L.append(threading.Thread(name=router_a.__str__(), target=router_a.run))

    thread_L.append(threading.Thread(name="Network", target=link_layer.run))

    for t in thread_L:
        t.start()

    # create some send events
    #for i in range(3):
    client.udt_send(2, "This message is generated so that we can test sending a message that is over 80 characters long. I beleive this message is now larger than that")

    # give the network sufficient time to transfer all packets before quitting
    sleep(simulation_time)

    # join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()

    print("All simulation threads joined")

# writes to host periodically