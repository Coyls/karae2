#!/usr/bin/env python

# IMPORT

from __future__ import print_function
import subprocess
import sys
import os
import time

from blue_st_sdk.manager import Manager
from blue_st_sdk.manager import ManagerListener
from blue_st_sdk.node import NodeListener

from utils.protocol import ProtocolGenerator
from websocket import create_connection



# CONSTANTS

# Presentation message.
INTRO = """##################
# Switch #
##################"""

# Bluetooth Scanning time in seconds (optional).
SCANNING_TIME_s = 5

til = "BCN-423"
ws = create_connection("ws://localhost:8000")

time.sleep(2)

name = "switch"
sendName =ProtocolGenerator("name", name)

ws.send(sendName.create())

# FUNCTIONS

#
# Printing intro.
#
def print_intro():
    print('\n' + INTRO + '\n')


# INTERFACES

#
# Implementation of the interface used by the Manager class to notify that a new
# node has been discovered or that the scanning starts/stops.
#
class MyManagerListener(ManagerListener):

    #
    # This method is called whenever a discovery process starts or stops.
    #
    # @param manager Manager instance that starts/stops the process.
    # @param enabled True if a new discovery starts, False otherwise.
    #
    def on_discovery_change(self, manager, enabled):
        print('Discovery %s.' % ('started' if enabled else 'stopped'))
        if not enabled:
            print()

    #
    # This method is called whenever a new node is discovered.
    #
    # @param manager Manager instance that discovers the node.
    # @param node    New node discovered.
    #
    def on_node_discovered(self, manager, node):
        print('New device discovered: %s.' % (node.get_name()))


#
# Implementation of the interface used by the Node class to notify that a node
# has updated its status.
#
class MyNodeListener(NodeListener):

    #
    # To be called whenever a node connects to a host.
    #
    # @param node Node that has connected to a host.
    #
    def on_connect(self, node):
        print('Device %s connected.' % (node.get_name()))

    #
    # To be called whenever a node disconnects from a host.
    #
    # @param node       Node that has disconnected from a host.
    # @param unexpected True if the disconnection is unexpected, False otherwise
    #                   (called by the user).
    #
    def on_disconnect(self, node, unexpected=False):
        print('Device %s disconnected%s.' % \
            (node.get_name(), ' unexpectedly' if unexpected else ''))
        if unexpected:
            # Exiting.
            print('\nExiting...\n')
            sys.exit(0)

#
# MAIN APPLICATION
#
def main(argv):

    # Printing intro.
    print_intro()

    try:
        # Creating Bluetooth Manager.
        manager = Manager.instance()
        manager_listener = MyManagerListener()
        manager.add_listener(manager_listener)

        while True:

            isConnected = False
            discovered_devices = []


            while not isConnected:
                # Synchronous discovery of Bluetooth devices.
                print('Scanning Bluetooth devices...\n')
                manager.discover(SCANNING_TIME_s)

                # Getting discovered devices.
                discovered_devices = manager.get_nodes()

                # Listing discovered devices.
                if not discovered_devices:
                    isConnected = False
                    print("retry...")
                else:
                    isConnected = True


            necklace = False

            for device in discovered_devices:
                if device.get_name() == til:
                    necklace = True
                print('%s: [%s]' % (device.get_name(), device.get_tag()))

            # Connecting to the device.
            print('Connecting to %s...' % (device.get_name()))
            """ if not device.connect():
                print('Connection failed.\n')
                continue """


            print("Connected !")
            data = ProtocolGenerator(name, "1")
            ws.send(data.create())
            print("Data send, sleep 10s and loop")
            # subprocess.run(['espeak','-vfr+f4','-s150', "Bonjour, Humain !"])
            time.sleep(10)
            device.disconnect()
            print('Disconnection done.')
            if not device.connect():
                print("Loop")
                isConnected = False
            
            
                

    except KeyboardInterrupt:
        try:
            # Exiting.
            print('\nExiting...\n')
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":

    main(sys.argv[1:])
