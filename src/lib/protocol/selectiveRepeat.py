from lib.protocol.protocolTransmission import ProtocolTransmission


class SelectiveRepeat(ProtocolTransmission):
    def __init__(self, context):
        self.ctx = context  # referencia al clientHandler
        # self.ctx.socket.settimeout(SENDER_TIMEOUT)

    def send_file(self, chunks):
        print("Recibiendo archivo - Implementar Selective repeat")

    def receive_file(self, chunks):
        print("Enviado archivo - Implementar Selective repeat")
