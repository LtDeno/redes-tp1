FAIL_CONNECTION = "No se pudo establecer conexion."
TIMEOUT_ACK = "Timeout en handshake - Timeout esperando ACK al START " \
    "- Reintento {num}/{max_retries}"
TIMEOUT_READY = (
    "Timeout en handshake - Timeout esperando READY tras CONFIRM - "
    "Handshake incompleto"
)
# TIMEOUT_HANSHAKE = "Timeout en handshake - Reintento {num}/{max_retries}"
ERROR_TRANSFER = "Error durante la transferencia: {error}"

"""Logins downloadhandler"""
REQUEST_DOWNLOAD = "Solicitando descarga del archivo: {filename}"
INIT_RECV_DATA = "Conexion establecida - Iniciando recepción de datos..."
FILE_NOT_EXIST = "El archivo '{filename}' no existe en el servidor."
SUCCESSFUL_DOWNLOAD = (
    "Descarga del archivo '{filename}' finalizada - "
    "Guardado exitosamente en '{dst}'."
)


"""Logins uploadHandler"""
REQUEST_UPLOAD = "Preparando subida del archivo: {filename}"
INIT_TRANS_DATA = "Conexion establecida - Iniciando transferencia de datos..."
SUCCESSFUL_UPLOAD = "Subida del archivo '{filename}' finalizada"
ERROR_FILE = "No se pudo leer el archivo '{filename}'."
FIN_NOT_CONFIRMED = (
    "Cierre de sesion no confirmado tras {max_retries} intentos - "
    "Los {chunks} chunks fueron confirmados por el receptor, "
    "pero puede no haber guardado el archivo"
)
