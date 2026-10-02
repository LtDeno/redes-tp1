from lib.common.parserHandler import ParserHandler
from lib.server.server import Server

if __name__ == "__main__":
    parser = ParserHandler()
    args = parser.get_arguments_start_server()
    parser.configure_logging(args)
    server = Server((args.host, args.port), args.storage)
    server.start()
