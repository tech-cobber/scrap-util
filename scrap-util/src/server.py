from urllib.parse import ParseResult, urlparse
from .http_format import parse, Request
from .handlers import handle_keywords
import socket

HOST = 'localhost'
PORT = 50007
MAXSIZE = 1024


def keywords(url: ParseResult) -> str:
    '''Find Top-10 keywords on the page'''

    if '&' in url.query:
        status = 'HTTP/1.1 300 Multiple Choice'
        header = 'Content-Type: application/vnd.api+json'
        page: str = url.query.split('&')[0].split('=')[1]
    else:
        status = 'HTTP/1.1 200 OK'
        header = 'Content-Type: application/vnd.api+json'
        page: str = url.query.split('=')[1]
    print(urlparse(page))
    content: str = handle_keywords(urlparse(page))
    response = '\r\n'.join([status, header, content])
    return response + '\r\n'


class Application:

    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.routes = {
            '/keywords': keywords,
        }

    def run(self, host: str, port: int) -> None:
        # TODO epoll
        print(f'Running on {HOST}:{PORT}...')
        with self.server:
            self.server.settimeout(5)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((HOST, PORT))
            self.server.listen()
            while True:
                try:
                    client, _ = self.server.accept()
                    with client:
                        request = client.recv(MAXSIZE)
                        response = self.handle(request.decode('utf-8'))
                        client.sendall(response)
                except socket.error:
                    print("...")

    def handle(self, request: str) -> bytes:
        ''' Routes request and returnes encoded response '''

        request_obj: Request = parse(request)
        if not request_obj.method == 'GET':
            return 'HTTP/1.1 405 Method Not Allowed\n\n'.encode()
        url: ParseResult = urlparse(request_obj.url)
        response = self.routes[url.path](url)
        return response.encode()


if __name__ == "__main__":
    try:
        app = Application()
        app.run(HOST, PORT)
    except KeyboardInterrupt:
        print(f'Shutting down...')
