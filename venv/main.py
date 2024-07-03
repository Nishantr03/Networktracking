import dpkt
import socket
import pygeoip
import requests
import os

# Get full path to GeoLiteCity.dat assuming it's in the same directory as the script
current_dir = os.path.dirname(os.path.abspath(__file__))
geolite_city_file = os.path.join(current_dir, 'GeoLiteCity.dat')

# Initialize GeoIP object
gi = pygeoip.GeoIP(geolite_city_file)

def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    ip_data = response.json()
    return ip_data['ip']

def retKML(dstip, srcip):
    dst = gi.record_by_name(dstip)
    src = gi.record_by_name(srcip)
    if dst is None or src is None:
        return ''  # Handle the case where no record is found
    try:
        dstlongitude = dst['longitude']
        dstlatitude = dst['latitude']
        srclongitude = src['longitude']
        srclatitude = src['latitude']
        kml = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<extrude>1</extrude>\n'
            '<tessellate>1</tessellate>\n'
            '<styleUrl>#transBluePoly</styleUrl>\n'
            '<LineString>\n'
            '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
            '</LineString>\n'
            '</Placemark>\n'
        ) % (dstip, dstlongitude, dstlatitude, srclongitude, srclatitude)
        return kml
    except Exception as e:
        print(f"Error generating KML for {dstip}: {e}")
        return ''

def plotIPs(pcap, public_ip):
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            # Ensure IP is IPv4 and has correct length
            if isinstance(ip, dpkt.ip.IP) and len(ip.src) == 4 and len(ip.dst) == 4:
                src = socket.inet_ntoa(ip.src)
                dst = socket.inet_ntoa(ip.dst)
                kml = retKML(dst, public_ip)
                kmlPts += kml
        except Exception as e:
            print(f"Error processing packet: {e}")
            continue
    return kmlPts

def main():
    public_ip = get_public_ip()
    print(f"Public IP: {public_ip}")
    
    # Delete previous output.kml if it exists
    output_file = 'output.kml'
    try:
        if os.path.exists(output_file):
            os.remove(output_file)
            print(f"Deleted previous {output_file}")
    except Exception as e:
        print(f"Error deleting {output_file}: {e}")
    
    with open('wire.pcap', 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        kmlheader = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<Style id="transBluePoly">
  <LineStyle>
    <color>7d0000ff</color>  <!-- semi-transparent blue -->
    <width>3</width>         <!-- thicker line -->
  </LineStyle>
  <PolyStyle>
    <color>7d0000ff</color>  <!-- semi-transparent blue -->
  </PolyStyle>
</Style>
'''
        kmlfooter = '</Document>\n</kml>\n'
        kmldoc = kmlheader + plotIPs(pcap, public_ip) + kmlfooter
        
        # Save the KML document to a file
        with open(output_file, 'w') as kml_file:
            kml_file.write(kmldoc)
        print(f"KML document saved as '{output_file}'")

if __name__ == '__main__':
    main()
