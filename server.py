import socket

HOST = '127.0.0.1'
PORT = 8000

# AF_INET: 伺服器與伺服器間串接, SOCK_DGRAM: UDP免連線訊息傳輸通道
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind((HOST, PORT))

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

while True:
    indata, addr = s.recvfrom(1024)
    print('recvfrom ' + str(addr) + ': ' + indata.decode())

    outdata = 'echo ' + indata.decode()
    s.sendto(outdata.encode(), addr)
s.close()
