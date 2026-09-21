import argparse
import logging


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Argument parser for UDP client/server"
        )

    def _add_verbosity(self):
        group = self.parser.add_mutually_exclusive_group()
        group.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="increase output verbosity",
        )
        group.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            help="decrease output verbosity",
        )

    def _add_host(self):
        """Añade el argumento para la dirección IP."""
        self.parser.add_argument(
            "-H", "--host", required=True, help="server IP address"
        )

    def _add_port(self):
        """Añade el argumento para el puerto."""
        self.parser.add_argument(
            "-p",
            "--port",
            required=True,
            type=int,
            help="server port",
        )

    def _add_source_path(self):
        """Añade el argumento para el archivo de origen."""
        self.parser.add_argument(
            "-s",
            "--src",
            required=True,
            help="source file path",
        )

    def _add_destination_path(self):
        """Añade el argumento para el archivo de origen."""
        self.parser.add_argument(
            "-d",
            "--dst",
            required=True,
            help="destination file path",
        )

    def _add_filename(self):
        """Añade el argumento para el nombre del archivo."""
        self.parser.add_argument(
            "-n",
            "--name",
            required=True,
            help="file name",
        )

    def _add_protocol(self):
        """Añade el argumento para el protocolo de recuperación"""
        self.parser.add_argument(
            "-r",
            "--protocol",
            required=True,
            choices=["sw", "sr"],
            help="error recovery protocol",
        )

    def _add_service_host(self):
        """Añade el argumento para la dirección IP."""
        self.parser.add_argument(
            "-H", "--host", required=True, help="service IP address"
        )

    def _add_service_port(self):
        """Añade el argumento para el puerto."""
        self.parser.add_argument(
            "-p",
            "--port",
            required=True,
            type=int,
            help="service port",
        )

    def _add_storage_path(self):
        """Añade el argumento para el archivo de origen."""
        self.parser.add_argument(
            "-s",
            "--storage",
            required=True,
            help="storage dir path",
        )

    def _parse(self):
        """Parsea y devuelve los argumentos."""
        return self.parser.parse_args()

    def get_arguments_upload(self):
        """Argumentos para subida desde el cliente."""
        self._add_verbosity()
        self._add_host()
        self._add_port()
        self._add_source_path()
        self._add_filename()
        self._add_protocol()
        return self._parse()

    def get_arguments_download(self):
        """Argumentos para descarga desde el cliente."""
        self._add_verbosity()
        self._add_host()
        self._add_port()
        self._add_destination_path()
        self._add_filename()
        self._add_protocol()
        return self._parse()

    def get_arguments_start_server(self):
        """Argumentos para el incio del servidor."""
        self._add_verbosity()
        self._add_host()
        self._add_port()
        self._add_storage_path()
        return self._parse()

    def configure_logging(self, args):
        levels = {
            (True, False): logging.DEBUG,
            (False, True): logging.ERROR,
        }
        level = levels.get((args.verbose, args.quiet), logging.INFO)
        logging.basicConfig(level=level, format="%(levelname)s - %(message)s")
