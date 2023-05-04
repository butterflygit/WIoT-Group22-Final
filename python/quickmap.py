import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
# For scalability: In order to use a map that automatically resizes and rezones
# depending on the relative location of all LoRa data, you could use Bokeh.io
# with Google Maps to do this. However, we have decided to avoid this method
# for this prototype because it would require that we pay for Google API
# key permissions, which could be costly for us.

# Therefore, we are using a static display for our final project, but that is
# how we would plan to implement this in an actual application.

def mapper():
    lats = [] # To store latitudes
    longs = [] # To store longitudes
    names = [] # To store the name of each LoRa GPS device

    # Processing data file
    file0 = open("store.txt", "r")
    lines = file0.readlines()
    for line in lines:
        thing = line.split(", ")
        lats.append(thing[0]) # North/South
        longs.append(thing[1]) # East/West
        names.append(thing[2])
    file0.close()

    # Accessing map.png for background
    liveMap = plt.imread('map.png')

    # Starting the first iteration before updates
    plt.ion()
    newLongs = []
    newLats = []
    for element in longs:
        newLongs.append(float(element))
    for element in lats:
        newLats.append(float(element))
        
    # Bounding box to find the dimensions of the map to plot points on
    BBox = (min(newLongs), max(newLongs), min(newLats), max(newLats))
    fig,ax = plt.subplots()
    ax.set_xlim((BBox[0]-0.00001), (BBox[1]+0.00001))
    ax.set_ylim((BBox[2]-0.00001), (BBox[3]+0.00001))
    ax.set_title("Live GPS Data")
    deviceList = {}
    numDiff = 0
    for line in lines:
        thing = line.split(", ")
        newDevice = bytes(thing[2], 'utf-8')
        newDevice = str(newDevice[0]) + str(newDevice[1])
        if newDevice not in deviceList.keys():
            numDiff += 1
            deviceList[newDevice] = ''
    ax.imshow(liveMap, zorder=0, extent=BBox, aspect='equal')
    for device in deviceList:
        newLats = []
        newLongs = []
        for line in lines:
            thing = line.split(", ")
            ID = bytes(thing[2], 'utf-8')
            if (str(ID[0]) + str(ID[1])) == device:
                newLats.append(float(thing[0]))
                newLongs.append(float(thing[1]))
            deviceName = "Device " + device
            # Updating the map with all the new data
        ax.plot(newLongs, newLats, marker='v', label=deviceName)
    ax.legend(loc='right')
    plt.pause(0.1)

    # Loop to live-update the location data from the LoRa
    for _ in range(50):
        # Clear the plot and renew it each time to avoid repeating 
        ax.cla()
        ax.imshow(liveMap, zorder=0, extent=BBox, aspect='equal')
        # Get new data that was written to .txt file every 20 seconds
        numDiff = 0
        deviceList = {}
        file0 = open("store.txt", "r")
        lines = file0.readlines()
        file0.close()
        # Get new locations for any device
        for line in lines:
            thing = line.split(", ")
            newDevice = bytes(thing[2], 'utf-8')
            newDevice = str(newDevice[0]) + str(newDevice[1])
            if newDevice not in deviceList.keys():
                numDiff += 1
                deviceList[newDevice] = ''
        for device in deviceList:
            newLats = []
            newLongs = []
            for line in lines:
                thing = line.split(", ")
                ID = bytes(thing[2], 'utf-8')
                if (str(ID[0]) + str(ID[1])) == device:
                    newLats.append(float(thing[0]))
                    newLongs.append(float(thing[1]))
            deviceName = "Device " + device
            # Updating the map with all the new data
            ax.plot(newLongs, newLats, marker='v', label=deviceName)
        ax.legend(loc='right')
        ax.set_title("Live GPS Data")
        ax.set_xlim((BBox[0]-0.00001), (BBox[1]+0.00001))
        ax.set_ylim((BBox[2]-0.00001), (BBox[3]+0.00001))
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(10)
        ax.cla()
        ax.imshow(liveMap, zorder=0, extent=BBox, aspect='equal')
mapper()

