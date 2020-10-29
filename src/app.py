from typing import Tuple
import sys

from server.request_handler import HTTPRequestHandler
from database.database import Database
from server.server import PasteServer
from utils.logger import logger

DEFAULT_ADDRESS = "127.0.0.1"
DEFAULT_PORT = 8080

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


def parse_args() -> Tuple[str, int]:
    """Parses argv address and port information"""

    help_msg = "Usage: app.py [<address> <port>]"

    # Try to get address and port via argv
    try:
        if sys.argv[1] in ("--help" "-h"):
            print(help_msg)
            raise SystemExit

        address = sys.argv[1]
        port = int(sys.argv[2])

        return address, port

    # If there are bad arguments:
    except (IndexError, ValueError):
        logger.info(help_msg)
        return DEFAULT_ADDRESS, DEFAULT_PORT


if __name__ == '__main__':

    address, port = parse_args()

    print(ASCII_ART)
    logger.info("Welcome to MinimalPaste!")

    # Start the server
    server = PasteServer(server_address=(address, port),
                         RequestHandlerClass=HTTPRequestHandler,
                         db=Database())

    logger.info(f"Server is running at {address}:{port}!")

    server.serve_forever()
