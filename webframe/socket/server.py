# -*- coding: UTF-8 -*-
import socket  # 导入 socket 模块


def f1():
    return b'f1'


def f2():
    return b'f2'


routers = [
    ('/xxx', f1),
    ('/ooo', f2),
]


def run():
    sock = socket.socket()
    host = socket.gethostname()
    port = 8080
    sock.bind((host, port))
    sock.listen(10)
    while True:
        client, addr = sock.accept()
        data = sock.recv(1024)
        data = str(data)
        headers, bodies = data.split('\r\n\r\n')
        temp_list = headers.split('\r\n')
        method, url, protocol = temp_list[0].split('')
        print 'Connect sucess!!', addr
        client.send('Welcome!!')
        func_name = None
        for item in routers:
            if item[0] == url:
                func_name = item[1]
                break
        if func_name():
            response = func_name()
        else:
            response = b"404"
        sock.send(response)
        client.close()


if __name__ == '__main__':
    run()
