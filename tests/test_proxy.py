import unittest
import socket
from threading import Thread
from proxy.proxy_server import start_proxy
from proxy.request_handler import extract_target_host

class TestProxyServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_thread = Thread(target=start_proxy, daemon=True)
        cls.server_thread.start()
    
    def test_extract_target_host(self):
        request = b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
        host, port = extract_target_host(request)
        self.assertEqual(host, "example.com")
        self.assertEqual(port, 80)
    
    def test_proxy_connection(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 7777))
        client.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
        response = client.recv(4096)
        self.assertTrue(len(response) > 0)
        client.close()

if __name__ == "__main__":
    unittest.main()