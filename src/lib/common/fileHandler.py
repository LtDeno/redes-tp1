import logging
from pathlib import Path

from lib.common.constants import PAYLOAD_SIZE
from lib.common.logMessages import (
    CREATE_FILE,
    ERROR_EMPTY_LIST,
    ERROR_PROCESS_FILE,
    FILE_NOT_FOUND,
)

logger = logging.getLogger(__name__)


class FileHandler:
    def __init__(self, file_path, filename):
        self.base_path = Path(file_path)
        self.name = filename
        self.path = self.base_path / self.name

    """Recibe una lista de bytes"""
    """Crea carpetas si no existen y escribe el archivo final"""

    def write(self, chunks):

        if not chunks:
            logger.warning(ERROR_EMPTY_LIST.format(filename=self.name))
            return
        try:
            logger.debug(
                CREATE_FILE.format(filename=self.name,
                                   base_path=self.base_path))

            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("wb") as f:
                for chunk in chunks:
                    f.write(chunk)

        except OSError:
            logger.exception(ERROR_PROCESS_FILE.format(filename=self.name))

    """Lee el archivo completo en bytes y los devuelve
    solo si la lectura fue exitosa."""

    def read(self):
        chunks = []
        try:
            with self.path.open("rb") as f:
                while True:
                    chunk = f.read(PAYLOAD_SIZE)
                    if not chunk:
                        break
                    chunks.append(chunk)
            return chunks
        except FileNotFoundError:
            logger.error(FILE_NOT_FOUND.format(file_path=self.path))
            return None
        except OSError:
            logger.exception(ERROR_PROCESS_FILE.format(filename=self.name))
            return None
