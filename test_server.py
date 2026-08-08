#!/usr/bin/env python3
"""Tests for Crab Trap MUD web server.

Tests the HTTP handler by starting the server on a test port
and making real HTTP requests.
"""
import unittest
import http.client
import threading
import time
import os
import sys
from http.server import HTTPServer

# Ensure we can import server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from server import Handler, DIR


class TestCrabTrapServer(unittest.TestCase):
    """Test the Crab Trap MUD server via real HTTP requests."""

    @classmethod
    def setUpClass(cls):
        """Start the server on a test port in a background thread."""
        cls.port = 14064  # Different from production port 4064
        cls.server = HTTPServer(('127.0.0.1', cls.port), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.1)  # Give server time to start

    @classmethod
    def tearDownClass(cls):
        """Shut down the test server."""
        cls.server.shutdown()
        cls.server.server_close()

    def _get(self, path):
        """Make a GET request and return (status, headers, body)."""
        conn = http.client.HTTPConnection('127.0.0.1', self.port, timeout=5)
        conn.request('GET', path)
        resp = conn.getresponse()
        body = resp.read()
        conn.close()
        return resp.status, dict(resp.getheaders()), body

    def test_root_returns_200(self):
        """GET / should return 200."""
        status, _, _ = self._get('/')
        self.assertEqual(status, 200)

    def test_root_serves_html(self):
        """GET / should serve HTML content."""
        status, headers, body = self._get('/')
        self.assertEqual(status, 200)
        content_type = headers.get('Content-Type', '')
        self.assertIn('text/html', content_type)

    def test_index_html_returns_200(self):
        """GET /index.html should return 200."""
        status, _, _ = self._get('/index.html')
        self.assertEqual(status, 200)

    def test_index_html_content(self):
        """GET /index.html should serve the actual index.html file."""
        status, headers, body = self._get('/index.html')
        self.assertEqual(status, 200)
        # Should contain HTML tags
        self.assertIn(b'<html', body.lower())
        self.assertIn(b'</html>', body.lower())

    def test_unknown_path_returns_404(self):
        """GET /nonexistent should return 404."""
        status, _, body = self._get('/nonexistent')
        self.assertEqual(status, 404)
        self.assertEqual(body, b'404 Not Found')

    def test_404_content_type(self):
        """404 response should have text/plain content type."""
        status, headers, _ = self._get('/missing')
        self.assertEqual(status, 404)
        content_type = headers.get('Content-Type', '')
        self.assertIn('text/plain', content_type)

    def test_cache_control_header(self):
        """Index page should have Cache-Control: no-cache."""
        status, headers, _ = self._get('/')
        self.assertEqual(status, 200)
        cache_control = headers.get('Cache-Control', '')
        self.assertEqual(cache_control, 'no-cache')

    def test_root_and_index_same_content(self):
        """GET / and GET /index.html should serve identical content."""
        _, _, body_root = self._get('/')
        _, _, body_index = self._get('/index.html')
        self.assertEqual(body_root, body_index)

    def test_content_length_set(self):
        """Response should include content body."""
        status, headers, body = self._get('/')
        self.assertEqual(status, 200)
        self.assertTrue(len(body) > 0)


class TestServerModule(unittest.TestCase):
    """Test module-level constants and structure without starting server."""

    def test_dir_constant_exists(self):
        """DIR constant should be the directory of server.py."""
        self.assertTrue(os.path.isdir(DIR))
        self.assertTrue(os.path.exists(os.path.join(DIR, 'server.py')))

    def test_index_html_exists(self):
        """index.html should exist in DIR."""
        self.assertTrue(os.path.exists(os.path.join(DIR, 'index.html')))

    def test_handler_is_http_handler(self):
        """Handler should be a BaseHTTPRequestHandler subclass."""
        from http.server import BaseHTTPRequestHandler
        self.assertTrue(issubclass(Handler, BaseHTTPRequestHandler))

    def test_handler_has_do_get(self):
        """Handler should have a do_GET method."""
        self.assertTrue(hasattr(Handler, 'do_GET'))
        self.assertTrue(callable(getattr(Handler, 'do_GET')))

    def test_handler_has_log_message(self):
        """Handler should override log_message."""
        from http.server import BaseHTTPRequestHandler
        self.assertNotEqual(Handler.log_message, BaseHTTPRequestHandler.log_message)

    def test_handler_only_handles_get(self):
        """Handler should only implement do_GET (no POST, PUT, etc.)."""
        self.assertTrue(hasattr(Handler, 'do_GET'))
        self.assertFalse(hasattr(Handler, 'do_POST'))
        self.assertFalse(hasattr(Handler, 'do_PUT'))
        self.assertFalse(hasattr(Handler, 'do_DELETE'))


if __name__ == '__main__':
    unittest.main()
