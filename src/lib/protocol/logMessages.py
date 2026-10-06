SEND_FIN = "FIN enviado -- Intento Nro. {num}"
RECV_FIN_ACK = "FIN_ACK recibido -- Fin conexion completado"
RECV_FIN = "FIN recibido - Enviando FIN_ACK de confirmacion"
RECV_FIN_RETRANSMIT = "FIN reenviado - El FIN_ACK anterior no llego, reenviando FIN_ACK"
ERROR_FIN_ACK = "No se recibio FIN_ACK despues de {max_retries} intentos"


WINDOW_SLIDE = "Ventana deslizada - {delivered} chunks entregados en orden - recv_base={base} - Ultimo seq_num de red {seq}"
DISCARD_DUP = "DATA seq_num [{seq_num}] descartado - Se esperaba seq_num [{expected}]"

SEND_DATA_PACKET = "DATA enviado - Nro. de secuencia: {seq_num}"
SEND_ACK_DATA    = "ACK enviado - Nro. de secuencia: {seq_num}"

RECV_ACK_DATA = "Recibido ACK - Nro. de secuencia: {seq_num}"
RECV_DATA = "Recibido DATA - Nro. de secuencia recibido correctamente: {seq_num}"
NO_DATA_RECEIVED = "Recepcion abandonada: no llego ningun DATA en {timeout}(s)"

TRANSFER_INCOMPLETE = "Recepcion abandonada tras {timeout}s - {received} chunks recibidos - Archivo incompleto, no se guardo"

"""SELECTIVE REPEAT"""
RETRY_DATA = "DATA reenviado (timeout {timeout}s) - Nro. de secuencia: {seq_num}"
STALE_ACK = "ACK duplicado/atrasado - Nro. de secuencia: {seq_num}"
ERROR_SEND_STALL = (
    "Transferencia abandonada tras {timeout}s sin confirmaciones - "
    "{confirmed}/{total} chunks confirmados"
)