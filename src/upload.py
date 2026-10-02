from lib.client.uploadHandler import UploadHandler
from lib.common.parserHandler import ParserHandler

if __name__ == "__main__":
    parser = ParserHandler()
    args = parser.get_arguments_upload()
    parser.configure_logging(args)
    upload = UploadHandler(args)
    upload.execute()
