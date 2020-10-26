
"""
Automated server tests

The server must be running at
127.0.0.1:8080 in order to be tested.
"""

from http.client import HTTPConnection
from urllib.parse import urlencode
import unittest


SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 8080

# Creating our HTTP connections to the server
conn = HTTPConnection(SERVER_ADDRESS, SERVER_PORT)


class TestPOST(unittest.TestCase):
    """Test POST requests into the server"""

    def test_bytes_limit(self):
        """The server refuses any POST requests larger than 100kb."""
        conn.request("POST", "/post", 
                     urlencode({"new_paste_content":'X'*101_000}))
        r = conn.getresponse()

        self.assertEqual(r.reason, "Max POST size: 100000 bytes")
        self.assertEqual(r.status, 422)
    
    def test_wrong_endpoint(self):
        """POST requests are only allowed on the /paste endpoint."""
        conn.request("POST", '/', urlencode({"new_paste_content":'X'}))
        r = conn.getresponse()

        self.assertEqual(r.reason, "POST requests are only allowed on /paste")
        self.assertEqual(r.status, 501)
    
    def test_invalid_request(self):
        """
        The POST request must contain a field
        called `new_paste_content`
        """
        conn.request("POST", "/post", urlencode({"wrong_field":'X'}))
        r = conn.getresponse()

        self.assertEqual(r.status, 422)
        self.assertEqual(r.reason, "Invalid POST request. "
                                   "POST request must contain "
                                   "a 'new_paste_content' field")

    def test_sucessful_post(self):
        """
        A successful POST is made on the /paste endpoint,
        contains the `new_paste_content` field, and contains
        less than 100.000 characters.

        This method tests both GET and POST server methods.
        """
        test_variable = "GET test!"

        conn.request("POST", "/paste",
                     urlencode({"new_paste_content":test_variable}))
        r = conn.getresponse()

        url = r.headers.get("Location")

        # Assert redirect occured
        self.assertEqual(r.status, 301)

        # Requesting the posted
        conn.request("GET", f"/{url}")
        r = conn.getresponse()

        self.assertEqual(r.status, 200)
        self.assertTrue(test_variable in r.read().decode())


class TestGET(unittest.TestCase):
    """Test GET requests into the server"""

    def test_get_home(self):
        """Simple GET request on home"""
        conn.request("GET", '/')
        r = conn.getresponse()

        self.assertEqual(r.status, 200)
        self.assertTrue("MinimalPaste" in r.read().decode())

    def test_get_not_found(self):
        """GET request on non-existing endpoint"""
        conn.request("GET", "/secretendpoint")
        r = conn.getresponse()

        self.assertEqual(r.status, 404)
        self.assertEqual(r.reason, "URL not found")


if __name__ == '__main__':
    unittest.main()
