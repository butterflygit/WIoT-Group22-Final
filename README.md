# WIoT-Group22-Final

LoRAWAN zip file: Contains the files needed to collect GPS data using the LoRa + GPS device, encode this data into proper packet format, and send this to The Things Network

Python folder contents:
- main.py: Connects to TTN application and pulls packets sent to it by the LoRA+GPS device(s), sends this packet information to parser.py
- parser.py: Parses the packet information (device number and longitude and latitude encoded as IEEE 754 decimals) and writes these to a txt file called 'store.txt'
- quickmap.py: Uses the information in 'store.txt' to create a dynamically-updating graph that shows the path of the device since the start of data collection. Updates the map in real-time for one or multiple devices using matplotlib.
