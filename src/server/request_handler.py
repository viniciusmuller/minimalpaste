from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qsl
from typing import Tuple

from utils.templater import create_template
from database.database import Database


db = Database()

class HTTPRequestHandler(BaseHTTPRequestHandler):
    """Custom class to handle POST and GET requests to the server."""

    def _set_headers(self, *, 
                     status_code: int = 200,
                     header: Tuple[str, str] = ("Content-type", "text/html")
                     ) -> None:
        """
        Set the response headers.

        Parameters
        ----------
        status_code : `int`
            Integer containing the header status code.
        
        header : Tuple[`str`, `str`]
            Tuple containing keyword and value for http header.
            e.g ("Location", "/")
        """
        self.send_response(status_code)
        self.send_header(*header)
        self.end_headers()

    def do_GET(self) -> None:
        """
        Method used by `BaseHTTPRequestHandler` to handle
        the GET requests to the server.

        POST requests are only supported if the request contains
        a field called new_paste_content.

        If it contains, the server creates a new paste and 
        redirects the user to the created paste page. 
        """

        endpoint = self.path[1:]

        # Request to home (e.g '/')
        if not endpoint:
            self._set_headers()
            # Creating page containing POST form
            page = create_template()
            # Serving the page
            self.wfile.write(page.encode())

        # Existing endpoint
        elif endpoint in db.endpoints:
            self._set_headers()
            # Retrieving the content from the database and feeding it
            # into the create_template function to create a HTML page
            # containing the content
            content = db.read_content(endpoint)
            page = create_template(content)
            # Serving the page
            self.wfile.write(page.encode())

        # Endpoint not found (404)
        else:
            self.send_error(404, "URL not found")

    def do_POST(self) -> None:
        """
        Method used by `BaseHTTPRequestHandler` to handle
        the POST requests to the server.

        POST requests are only supported if the request contains
        a field called `new_paste_content`.

        If it contains, the server creates a new paste and 
        redirects the user to the paste page.
        """

        # Reading the request content
        post_len = int(self.headers["Content-Length"])
        post_data = self.rfile.read(post_len)

        # Parsing the query string into a dictionary
        query = dict(parse_qsl(post_data.decode()))
        content = query.get("new_paste_content")

        if post_len >= 100_000:
            self.send_error(422, "Max POST size: 100000 bytes")

        # Wrong POST endpoint
        elif content and self.path != "/paste":
            self.send_error(501, "POST requests are only allowed on /paste")

        # Supported POST request, add to the database
        elif content:
            paste_url = db.create_paste(content)

            # Redirect client to new paste URL
            self._set_headers(status_code=301,
                              header=("Location", paste_url))

        # Invalid POST request
        elif content is None:
            self.send_error(422, "Invalid POST request. "
                                 "POST request must contain "
                                 "a 'new_paste_content' field")
