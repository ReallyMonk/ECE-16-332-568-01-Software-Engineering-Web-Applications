import socket


def get_file(filename):
    path = 'F:\Rutgers\\2ndSemester\SOFTWR ENGG WEB APPL\Homework\HWK6\\'
    f = open(path + filename)
    lines = f.readlines()
    res = ''
    for line in lines:
        res = res + line
    return res


s = socket.socket()
host = socket.gethostname()
port = 8000
s.bind((host, port))

s.listen(1)

while True:
    client, addr = s.accept()

    print('connected to: ', addr)
    client.send(('Welcome').encode())
    while True:
        cmd = client.recv(1024).decode()
        print(cmd)

        if cmd.startswith('GET'):
            cmd_info = cmd.split('|')
            content = get_file(cmd_info[1])
            client.send(content.encode())
            print('send back ' + cmd_info[1])
            continue
        elif cmd.startswith('BOUNCE'):
            cmd_info = cmd.split('|')
            client.send(cmd_info[1].encode())
            print('send back ' + cmd_info[1])
            continue
        elif cmd.startswith('EXIT'):
            if cmd == 'EXIT|now':
                client.send(('Server Closed').encode())
            else:
                cmd_info = cmd.split('|')[1]
                client.send(cmd_info.encode())
            s.close()
            print('Server Closed')
            break
        else:
            client.send(('CAN NOT DO THAT').encode())
            continue
        
    break