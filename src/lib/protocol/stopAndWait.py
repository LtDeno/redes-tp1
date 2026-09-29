from lib.protocol.transmissionProtocol import ProtocolTransmission

class StopAndWait(ProtocolTransmission):
    def __init__(self, context):
        self.client_handler = context #referencia al clientHandler
        #self.ctx.socket.settimeout(SENDER_TIMEOUT)


    def send_data(self, message):
       print("Recibiendo archivo")

    def recieve_data(self, message):
        print("Enviado archivo")
