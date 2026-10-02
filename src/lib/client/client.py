import socket

BUFFER_SIZE = 4000
TIMEOUT = 2.0


class Client:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = (host, port)

    def finish(self):
        self.socket.close()

    def send_packet(self, packet):
        self.socket.sendto(packet, self.server_addr)

    def get_packet(self, timeout=TIMEOUT):
        self.socket.settimeout(timeout)
        try:
            data, _ = self.socket.recvfrom(BUFFER_SIZE)
            return data
        except socket.timeout:
            raise TimeoutError
