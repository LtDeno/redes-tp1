from lib.protocol.protocolTransmission import ProtocolTransmission


class StopAndWait(ProtocolTransmission):
    def __init__(self, context):
        self.ctx = context  # referencia al clientHandler
        # self.ctx.socket.settimeout(SENDER_TIMEOUT)

    def send_file(self, chunks):
        print("Recibiendo archivo - Implementar Stop and Wait")

    def receive_file(self, chunks):
        print("Enviando archivo - Implementar Stop and Wait")
