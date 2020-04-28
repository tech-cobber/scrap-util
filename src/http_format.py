from dataclasses import dataclass, field


@dataclass
class Request:
    ''' HTTP rquest '''
    method: str
    url: str
    protocol: str
    headers: dict = field(default_factory=dict)
    content: bytes = b''

    @classmethod
    def GET(cls, path: str, host: str) -> bytes:
        return f'GET {path} HTTP/1.1\r\n\
Host: {host}\r\n\
Connection: keep-alive\r\n\r\n'.encode('utf8')


@dataclass
class Response:
    ''' HTTP response '''
    status: int
    detail: str
    headers: dict = field(default_factory=dict)
    content: bytes = b''


def parse(request: str) -> Request:
    ''' Parses decoded request string\
         and makes http_format.Request object '''
    request_list = request.split('\r\n')
    headers = [parameter.split(': ')
               for parameter in request_list[1::] if parameter]
    headers = {key: value for key, value in headers}
    try:
        method, url, protocol = request_list[0].split(' ')
    except ValueError:
        print(request_list[0].split(' '))
        return Request('ERROR', '', '')
    return Request(method, url, protocol, headers)
