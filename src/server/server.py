from typing import Tuple

from socketserver import ThreadingMixIn
from socketserver import TCPServer


class PasteServer(TCPServer, ThreadingMixIn):
    """Server class that inherits ThreadingMixin for multithread"""
    def __init__(self, *,
                 server_address: Tuple[str, int],
                 RequestHandlerClass):
        """
        Server class constructor.

        Parameters
        ----------
        address : Tuple[`str`, `int`]
            Tuple containing the server IP address (e.g "127.0.0.1")
            and an int representing the server port (e.g 8080).

        handler :
            A request handling class supported by 
            the `ThreadingHTTPServer` class.
        """
        super().__init__(server_address, RequestHandlerClass)
