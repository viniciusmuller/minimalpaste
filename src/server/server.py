from typing import Tuple

from socketserver import ThreadingMixIn
from socketserver import TCPServer

from server.request_handler import BaseHTTPRequestHandler
from database.database import Database


class PasteServer(TCPServer, ThreadingMixIn):
    """
    Server class that inherits ThreadingMixin for multithread
    
    Server class constructor.

    Parameters
    ----------
    address : Tuple[`str`, `int`]
        Tuple containing the server IP address (e.g "127.0.0.1")
        and an int representing the server port (e.g 8080).

    handler :
        A request handling class supported by 
        the `ThreadingHTTPServer` class.
    
    db : `Database`
        Database instance that will be managed by the
        `RequestHandlerClass` instances.
    """

    def __init__(self, *,
                 server_address: Tuple[str, int],
                 RequestHandlerClass: BaseHTTPRequestHandler,
                 db: Database):

        super().__init__(server_address, RequestHandlerClass)
        self.db = db
      
