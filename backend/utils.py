import socket

def wake_on_lan(mac_address):
    mac = mac_address.replace(":", "").replace("-", "")
    data = bytes.fromhex("FF" * 6 + mac * 16)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(data, ("255.255.255.255", 9))
