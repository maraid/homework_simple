import socket
import re
import argparse
import storage

parser = argparse.ArgumentParser(description="Run key-value server")
parser.add_argument('--port', type=int,
                    help='port, where the server will be accessible at. '
                         '(default: 8181)',
                    default=8181)
parser.add_argument('--persistent', type=str,
                    help='If this argument is set, '
                         'the given file will be used to store data')

args = parser.parse_args()
port = args.port
if args.persistent:
    db = storage.SQLiteWrapper(args.persistent)
else:
    db = storage.SQLiteMock()

ok = b'HTTP/1.1 200 OK\nContent-Length: %d\nContent-Type: text/plain \n\n%s'
empty_content = b'\nContent-Length: 0\nContent-Type: text/plain \n\n'
teapot = b'HTTP/1.1 418 I\'m a teapot' + empty_content

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', 8181))
    s.listen()
    print("Listening...")
    while True:
        conn, addr = s.accept()
        if match := re.search(rb'^GET /(.*)/(.*) ', conn.recv(1024)):
            cmd, word = match.groups()
            if cmd == b'store':
                if len(splt := word.split(b':')) == 2:
                    db.store(splt[0], splt[1])
                    conn.send(ok % (len(splt[1]), splt[1]))
                else:
                    conn.send(teapot)
            elif cmd == b'get':
                try:
                    conn.send(ok % (len(r := db.get(word)), r))
                except KeyError:
                    conn.send(b'HTTP/1.1 404 Not Found' + empty_content)
            elif cmd == b'find':
                conn.send(ok %
                          (len(tmp := (b', '.join(db.find(word)))),
                           tmp))
            else:
                conn.send(teapot)
        else:
            conn.send(teapot)
