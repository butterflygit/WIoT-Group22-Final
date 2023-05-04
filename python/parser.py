# List your names: Gabriele Bright, Stephanie Skahen, Kelsen Donastien, Zach King
import matplotlib.pyplot as plt
import numpy as np
import quickmap # This is our file to plot each point on a map as it is read

lats = [] # To store latitude
longs = [] # To store longitude
names = []

def IEEEtoDigit(IEEENum):
    # Convert hex into binary for each
    hex_dict = {"0": '0000', "1": '0001', "2": '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111', '8': '1000', '9': '1001', 'a': '1010', 'b': '1011', 'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'}
    binaryString = ""
    i = 0
    while i < 4:
        for digit in hex(IEEENum[i])[2:]:
            binaryString += hex_dict[digit]
        i += 1
    if len(binaryString) < 32: #To account for positive numbers
        binaryString = "0" + binaryString
    print("CHECK01")
    # Reorganize binary into packets
    packet0 = binaryString[0]
    packet1 = binaryString[1:9]
    packet2 = binaryString[9:]
    # Get sign flag
    sign = False
    if packet0 == "0":
        sign = True
    print("CHECK11")
    # Get exponent from packet
    exponent = int(("0b"+packet1), 2) - 127
    # Get mantissa and do math
    mantissaList = []
    mantissaList.append(2**0)
    for idx, digit in enumerate(packet2):
        if digit == "1":
            mantissaList.append(2**-(idx+1))
    print("CHECK12")
    finalTemp = 0
    for item in mantissaList:
        finalTemp += item
    finalTemp = finalTemp * 2**exponent
    print("CHECK13")
    # To make sure negative numbers are negative
    if sign == False:
        finalTemp = -finalTemp
    print("CHECK14")
    print(finalTemp)
    return finalTemp


def decode(packet):
    """
    Decode the payload into GPS coordinates.

    This function returns nothing.
    """

    # Incoming packet format will be: 00 \\ XX XX XX XX \\ XX XX XX XX
    # The first IEEE is longitude, the second is latitude
    # Payload represented in IEEE-754 format

    # Divide into name, longitude and latitude
    GPSname = packet[:2]
    IEEElongitude = packet[2:6]
    IEEElatitude = packet[6:]
    print("CHECK0")
    #print(GPSname[0], GPSname[1])
    #print(hex(IEEElongitude[0]), hex(IEEElongitude[1]), hex(IEEElongitude[2]), hex(IEEElongitude[3]))
    #print(hex(IEEElatitude[0]))
    #print(hex(IEEElatitude[1]))
    #print(hex(IEEElatitude[2]))
    #print(hex(IEEElatitude[3]))
    # Form both into digits
    decLongitude = IEEEtoDigit(IEEElongitude)
    decLatitude = IEEEtoDigit(IEEElatitude)
    print("CHECK1")
    # All recorded coordinates are stored into a .txt file to be mapped 
    lats.append(decLatitude)
    longs.append(decLongitude)
    names.append(GPSname)
    print("CHECKagain")
    if (len(lats) == 1):
        print("the fuck")
        file0 = open("store.txt", "w")
        print("here0")
        L = str(decLatitude) + ", " + str(decLongitude) + ", " + str(GPSname)
        file0.writelines(L)
        print("here1")
        file0.close()
        print("CHECK2")
    else:
        file0 = open("store.txt", "a")
        print("here3")
        L = "\n" + str(decLatitude) + ", " + str(decLongitude) + ", " + str(GPSname)
        print(L)
        file0.write(L)
        print("here4")
        file0.close()
        print("CHECK3")

    # Call mapping file
    #quickmap.mapper()
    return True
