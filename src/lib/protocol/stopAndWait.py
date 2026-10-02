from lib.protocol.transmissionProtocol import TransmissionProtocol

class StopAndWait(TransmissionProtocol):
    def __init__(self, context):
        self.client_handler = context #referencia al clientHandler
        #self.ctx.socket.settimeout(SENDER_TIMEOUT)


    def send_data(self, chunks):
       print("Enviando archivo - Stop And Wait")

    def recieve_data(self, chunks):
        print("Recibiendo Archivo - Stop And Wait")
