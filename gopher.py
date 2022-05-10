#! /usr/bin/python3
# Isaac Ganoung
import socket
from urllib.parse import urlparse

def parse_url(url):
    if len(url) <=9 or url[:9] != 'gopher://':
        parsed_url = urlparse("gopher://" + url)
    else:
        parsed_url = urlparse(url)
    if parsed_url.scheme != 'gopher':
        raise RuntimeError(f"Unknown connection type {parsed_url.scheme}")
    return parsed_url

def download_gopher(url):
    recv_buffer = b""
    parsed_url = parse_url(url)
    port = parsed_url.port
    if not port:
        port = 70
    with socket.create_connection((parsed_url.hostname,port)) as s:
        # loop while data != '.'
        s.send((parsed_url.path + "\r\n\r\n").encode('utf-8'))
        while True:
            data = s.recv(1024)
            if data == b'':
                break
            recv_buffer += data
            if data[-5:] == b'\r\n.\r\n':
                recv_buffer = recv_buffer[:-5]
                break
    return recv_buffer

def download_file(url):
    filename = url.split('/')[-1]
    with open(filename, "wb") as output_file:
        output_file.write(download_gopher(url))

TYPE = {
    b'i':'info',
    b'0':'text',
    b'1':'submenu',
    b'3':'error',
    b'4':'binhex',
    b'5':'dos',
    b'6':'uuencoded',
    b'7':'search',
    b'9':'binary',
    b'+':'mirror',
    b'g':'gif',
    b'I':'image',
    b':':'bitmap',
    b';':'movie',
    b'<':'sound',
    b'd':'doc',
    b'h':'html',
    b's':'sound'
}

def get_gopher_type(char):
    return TYPE.get(char.encode('utf-8'))

class gopher_line:
    def __init__(self,line):
        self.gopher_type = get_gopher_type(chr(line[0]))
        new_line = line[1:].split(b'\t')
        self.label = new_line[0]
        if new_line[1] != b'':
            self.path = new_line[1]
            if self.path[-1] == b'/':
                self.path = self.path[:-1]
        else:
            self.path = None
        self.server = new_line[2]
        self.port = int(new_line[3])
        self.number = None
        

def parse_gopher_buffer(gopher_buffer):
    new_buffer = []
    counter = 0
    line_map = {}
    for i in range(len(gopher_buffer)):
        line = gopher_buffer[i]
        if line == b'': # Empty line control
            continue
        temp_line = gopher_line(line)
        if temp_line.gopher_type != None and temp_line.gopher_type != 'info' and temp_line.gopher_type != 'error' and temp_line.gopher_type != 'html':
            temp_line.number = counter
            line_map[counter] = i
            counter += 1
        new_buffer.append(temp_line)
    return new_buffer,line_map

def goto_url(url):
    recv_buffer = download_gopher(url)
    return url,parse_gopher_buffer(recv_buffer.split(b'\r\n'))


def print_gopher_buffer(gopher_buffer):
    for line in gopher_buffer:
        if line.gopher_type == None or line.gopher_type == 'info' or line.gopher_type == 'search' or line.gopher_type == 'html': # Unsupported type or informational line
            print("\033[0;32m\t\t{}\033[0;0m".format(line.label.decode()))
        elif line.gopher_type == 'text':
            print("\033[0;34m{}\t🗎\t{}\033[0;0m".format(line.number,line.label.decode()))
        elif line.gopher_type == 'submenu' or line.gopher_type == 'mirror':
            print("\033[0;34m{}\t☰\t{}\033[0;0m".format(line.number,line.label.decode()))
        elif line.gopher_type == 'error':
            print("\033[0;31m\t\t{}\033[0;0m".format(line.number,line.label.decode()))
        elif line.gopher_type == 'binhex' or line.gopher_type == 'uuencoded': # Mac formats
            print("\033[0;34m{}\t\t{}\033[0;0m".format(line.number,line.label.decode()))
        elif line.gopher_type == 'dos': # DOS file
            print("\033[0;34m{}\t㍶\t{}\033[0;0m".format(line.number,line.label.decode()))
        elif line.gopher_type == 'binary': # Often used for PDFs
            print("\033[0;34m{}\tℬ\t{}\033[0;0m".format(line.number,line.label.decode()))
        elif line.gopher_type == 'gif' or line.gopher_type == 'bitmap' or line.gopher_type == 'image':
            print("\033[0;34m{}\t🖻\t{}\033[0;0m".format(line.number,line.label.decode()))
        elif line.gopher_type == 'movie':
            print("\033[0;34m{}\t📼\t{}\033[0;0m".format(line.number,line.label.decode()))
        elif line.gopher_type == 'sound':
            print("\033[0;34m{}\t🕬\t{}\033[0;0m".format(line.number,line.label.decode()))
        elif line.gopher_type == 'doc':
            print("\033[0;34m{}\t🖺\t{}\033[0;0m".format(line.number,line.label.decode()))
