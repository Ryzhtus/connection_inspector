import sys
import time
import socket
import urllib.request
import site_queue


def tcp_test(host: str, port: int):
    connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = connection_socket.connect_ex((host, port))

    if result == 0:
        return True
    else:
        return False


def http_test(url: str):
    if url == 'localhost':
        return 0
    else:
        full_url = 'http://www.' + url

        start_time = time.time()
        status = urllib.request.urlopen(full_url)
        end_time = time.time()

        speed = end_time - start_time

        if status.getcode() == 200:
            return 200
        else:
            return status.getcode()


def url_parser(site_name: str):
    site_ip = socket.gethostbyname(site_name)
    colon_pos = site_ip.find(':')

    if colon_pos == -1:
        host = site_ip
        port = int(80)
    else:
        host = site_ip[:colon_pos]
        port = int(site_ip[colon_pos:])

    return host, port


def countdown(t: int):
    for remaining in range(t, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.flush()


sites = site_queue.SiteQueue()

print("Hello! Enter the site name (or names) you want to check")
print("When it's over, write \"Ctrl + C\" to start checking  >>")

try:
    while True:
        site_name = input(str()).lower()
        host, port = url_parser(site_name)
        sites.add(site_name, host, port)
except KeyboardInterrupt:
    pass

print()
print('Set time (in minutes) for re-connection to a site if it\'s not answering:')

try_time = int(input())
try_time = try_time * 60

while not sites.is_empty():
    for i in range(0, sites.__len__()):
        current = sites.dequeue()

        if tcp_test(current[1], current[2]):
            print('TCP connection to', current[0], 'was successful')
        else:
            print('TCP connection to', current[0], 'was not successful')
            sites.add(current[0], current[1], current[2])

        status_code = http_test(current[0])
        if status_code == 200:
            print('HTTP connection to', current[0], 'was successful. Site is online!')
        else:
            print('HTTP connection to', current[0], 'was not successful. Error status:', status_code)
            if not sites.is_in(current[0]):
                sites.add(current[0], current[1], current[2])

    if not sites.is_empty():
        countdown(try_time)


print('Program is done.')