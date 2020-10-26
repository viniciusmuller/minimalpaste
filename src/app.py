import sys

from server.request_handler import HTTPRequestHandler
from server.server import PasteServer
from utils.logger import logger


ASCII_ART = r"""
  __  __ _       _                 _    
 |  \/  (_)     (_)               | |   
 | \  / |_ _ __  _ _ __ ___   __ _| |   
 | |\/| | | '_ \| | '_ ` _ \ / _` | |   
 | |  | | | | | | | | | | | | (_| | |   
 |_|  |_|_|_| |_|_|_| |_| |_|\__,_|_|   
                 _____          _       
                |  __ \        | |      
                | |__) |_ _ ___| |_ ___ 
                |  ___/ _` / __| __/ _ \
                | |  | (_| \__ \ ||  __/
                |_|   \__,_|___/\__\___|
"""


if __name__ == '__main__':
    address = ''
    port = 0

    # Try to get address and port via argv
    try:
        address = sys.argv[1]
        port = int(sys.argv[2])

    # If there is no argv... 
    except (IndexError, ValueError):
        logger.info("Usage: app.py [address] [port]")
        address = '127.0.0.1'
        port = 8080

    print(ASCII_ART)
    logger.info("Welcome to MinimalPaste!")

    # Start the server
    server = PasteServer(server_address=(address, port),
                         RequestHandlerClass=HTTPRequestHandler)

    logger.info(f"Server is running at {address}:{port}!")

    server.serve_forever()
