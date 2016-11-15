import socket
from sys import argv

MAX_BUFFER_SIZE = 1024
MESSAGE_ENCODING = 'UTF-8'

def validate(message):
    metadata = message.split(' :')[0]
    return message[0] == ':' and \
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
        return message.split(' :', 1)[1].strip()

def parse_message_fields(message):
    return {'NICKNAME' : parse_nickname(message),
            'USERNAME' : parse_username(message),
            'HOST' : parse_host(message),
            'TYPE' : parse_message_type(message),
            'CHANNEL' : parse_channel(message),
            'TEXT' : parse_message_text(message)}

def receive_message(mySocket):
    return mySocket.recv(MAX_BUFFER_SIZE).decode(MESSAGE_ENCODING)

def print_chat(message):
    print('%s: %s' % (message['USERNAME'], message['TEXT']))

def process_message(message, function):
    function(message)

def listen_to_chat(mySocket, filter):
    while mySocket:
        message = parse_message_fields(receive_message(mySocket))
        if filter.count(message['USERNAME']) > 0 and message['TYPE'] == 'PRIVMSG':
            process_message(message, print_chat)

def join_channel(socket,
                 oauth,
                 nickname,
                 channel):
    message(socket, 'PASS', oauth)
    message(socket, 'NICK', nickname)
    message(socket, 'JOIN', '#' + channel)

def message(socket,
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
        fd.close()

    join_channel(mySocket, oauth, nickname, channel)
    listen_to_chat(mySocket, whitelist)

    mySocket.close()

if __name__ == '__main__':
    main()
