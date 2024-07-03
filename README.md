# KML Packet Plotter

This project generates a KML file that plots IP packet data from a pcap file. The KML file can be viewed in Google Earth or Google Maps, with the IP locations represented as placemarks.

## Features

- Reads packet capture (pcap) files.
- Extracts source and destination IP addresses from the packets.
- Geolocates the IP addresses using the GeoLiteCity database.
- Generates a KML file with placemarks for the IP addresses.
- Uses Google-compatible styling for placemarks.
- Automatically deletes previous KML output before generating a new one.

## Requirements

- Python 3.x
- `dpkt` library
- `socket` library
- `pygeoip` library
- `requests` library
- GeoLiteCity database (`GeoLiteCity.dat`)

## Usage

1. Place your pcap file (e.g., `wire.pcap`) in the same directory as the script.

2. Run the script:

    ```bash
    python main.py
    ```

The script will:

- Retrieve your public IP address.
- Process the pcap file to extract IP addresses.
- Geolocate the IP addresses.
- Generate a KML file (`output.kml`) with placemarks for the IP addresses.

The KML file can be opened in Google Earth or Google Maps to visualize the IP locations.

## Acknowledgements
- This project is based on the tutorial "Python Cybersecurity: Network Tracking Using Wireshark and Google Maps" by Vinsloev Academy.
