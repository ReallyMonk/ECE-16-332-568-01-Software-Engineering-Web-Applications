import socket

s = socket.socket()
host = socket.gethostname()
port = 8000

s.connect((host, port))

print(s.recv(1024).decode())
'''
s.close
'''

while True:
    cmd = input('Your command: ')
    if cmd.startswith('GET') or cmd.startswith('get'):
        cmd_info = cmd.split()
        filename = cmd_info[1] + '.txt'
        s.send(('GET|' + filename).encode())
        print(s.recv(1024).decode())
    elif cmd.startswith('BOUNCE') or cmd.startswith('bounce'):
        msg = cmd[7:]
        s.send(('BOUNCE|' + msg).encode())
        print(s.recv(1024).decode())
    elif cmd.startswith('EXIT') or cmd.startswith('exit'):
        if cmd == 'EXIT' or cmd == 'exit':
            s.send(('EXIT|now').encode())
        else:
            cmd_info = cmd[5:]
            s.send(('EXIT|' + cmd_info).encode())
        print(s.recv(1024).decode())
        s.close()
        break