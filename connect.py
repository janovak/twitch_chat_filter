import socket
from sys import argv

MAX_BUFFER_SIZE = 1024
MESSAGE_ENCODING = 'UTF-8'

def validate(message):
    return message is not '' and \
           message[0] == ':' and \
           '!' in message and \
           '@' in message and \
           '#' in message

def parse_nickname(message):
    if validate(message):
        return message.split(':')[1].split('!')[0]

def parse_username(message):
    if validate(message):
        return message.split('!')[1].split('@')[0]

def parse_host(message):
    if validate(message):
        return message.split('@')[1].split(' ')[0]

def parse_message_type(message):
    if validate(message):
        return message.split(' ')[1].split(' ')[0]

def parse_channel(message):
    if validate(message):
        return message.split('#')[1].split(' ')[0]

def parse_message_text(message):
    if validate(message) and parse_message_type(message) == 'PRIVMSG':
        return message.split(' :', 1)[1]

def parse_message_fields(message):
    return {'NICKNAME' : parse_nickname(message),
            'USERNAME' : parse_username(message),
            'HOST' : parse_host(message),
            'TYPE' : parse_message_type(message),
            'CHANNEL' : parse_channel(message),
            'TEXT' : parse_message_text(message)}

def recv_message(mySocket):
    return mySocket.recv(MAX_BUFFER_SIZE).decode(MESSAGE_ENCODING).strip()

def print_chat(message):
    print('%s: %s' % (parse_username(message), parse_message_text(message)))

def process_message(function, *args):
    function(*args)

def listen_to_chat(mySocket, filter):
    while mySocket:
        message = recv_message(mySocket)
        if filter.count(parse_username(message)) > 0 and parse_message_type(message) == 'PRIVMSG':
            *args, = [message]
            process_message(print_chat, *args)
        elif message == 'PING :tmi.twitch.tv':
            *args, = [mySocket, 'PONG', ' :tmi.twitch.tv']
            process_message(send_message, *args)

def join_channel(socket,
                 oauth,
                 nickname,
                 channel):
    send_message(socket, 'PASS', oauth)
    send_message(socket, 'NICK', nickname)
    send_message(socket, 'JOIN', '#' + channel)

def send_message(socket,
            msg_type,
            message):
    socket.send(bytes(('%s %s\r\n' % (msg_type, message)), MESSAGE_ENCODING))

def connect(socket,
            dest = 'irc.chat.twitch.tv',
            port = 6667):
    socket.connect((dest, port))

def main():
    channel = argv[1]
    nickname = argv[2]
    oauth = argv[3]
    mySocket = socket.socket()
    if len(argv) > 5:
        dest = argv[4]
        port = argv[5]
        connect(mySocket, dest, port)
    else:
        connect(mySocket)

    whitelist = list()
    with open('whitelistednames', 'r') as fd:
        whitelist = fd.read().splitlines()

    join_channel(mySocket, oauth, nickname, channel)
    listen_to_chat(mySocket, whitelist)

    mySocket.close()

if __name__ == '__main__':
    main()
