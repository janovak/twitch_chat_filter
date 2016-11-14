import socket
import sys

MAX_BUFFER_SIZE = 1024

def receive_message(mySocket):
    return mySocket.recv(MAX_BUFFER_SIZE)

def process_message(message, function):
    function(message)

def listen_to_chat(mySocket):
    while mySocket:
        message = receive_message(mySocket)
        process_message(message.decode('UTF-8'), print)

def join_channel(socket,
                 oauth,
                 nickname,
                 channel):
    message(socket, 'PASS', oauth)
    message(socket, 'NICK', nickname)
    message(socket, 'JOIN', '#' + channel)

def message(socket,
            msg_type,
            message,
            encoding = 'UTF-8'):
    socket.send(bytes(('%s %s\r\n' % (msg_type, message)), encoding))

def connect(socket,
            dest = 'irc.chat.twitch.tv',
            port = 6667):
    socket.connect((dest, port))

def main():
    channel = sys.argv[1]
    nickname = sys.argv[2]
    oauth = sys.argv[3]
    mySocket = socket.socket()
    if len(sys.argv) > 5:
        dest = sys.argv[4]
        port = sys.argv[5]
        connect(mySocket, dest, port)
    else:
        connect(mySocket)

    join_channel(mySocket, oauth, nickname, channel)
    listen_to_chat(mySocket)
    mySocket.close()

if __name__ == '__main__':
    main()
