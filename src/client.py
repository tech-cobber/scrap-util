import socket
import json
import click
from .http_format import Request

HOST = 'localhost'
PORT = 50007
PATH = '/keywords?url={0}'


@click.command()
@click.option("--url")
def keywords(url: str):
    socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_.settimeout(5)
    addr = (HOST, PORT)
    socket_.connect(addr)
    socket_.send(Request.GET(PATH.format(url), HOST))
    response = socket_.recv(2048)
    data = b''
    while response:
        data += response
        try:
            response = socket_.recv(2048)
        except socket.error:
            break
    data = data.decode()
    socket_.close()
    result = data.split('\r\n')[-2]
    json_obj = json.loads(result)
    print(f'\nMost common words\nurl: {url}')
    for key, value in json_obj.items():
        print(f'{key} - {value}')
    print()
