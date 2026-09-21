from lib.common.argumentParser import ArgumentParser as argParse

if __name__ == "__main__":
    args = argParse().get_arguments_start_server()
    argParse.configure_logging(args)
