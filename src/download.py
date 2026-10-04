from lib.client.downloadHandler import DownloadHandler
from lib.common.parserHandler import ParserHandler

if __name__ == "__main__":
    parser = ParserHandler()
    args = parser.get_arguments_download()
    parser.configure_logging(args)
    download = DownloadHandler(args)
    download.execute()
