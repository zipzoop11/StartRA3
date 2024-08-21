import subprocess
import time
import os

from http.server import HTTPServer, SimpleHTTPRequestHandler
cwd = os.getcwd()


hosts_file_path = 'C:\Windows\system32\drivers\etc\hosts'
with open(hosts_file_path,'rb') as hosts_file:
    print("Getting current hosts file content")
    hosts_file_contents = hosts_file.readlines()


backup_filename = os.path.join(cwd,f'hosts.{time.time()}')
print(f"Backup up old content to '{backup_filename}'")

with open(backup_filename,'wb') as backup_file:
    backup_file.write(b''.join(hosts_file_contents))

print('Adding "files.ea.com" to HOSTS file...')
with open(hosts_file_path,'wb') as hosts_file:
    hosts_file_contents.append('127.0.0.1 files.ea.com'.encode('utf-8'))
    hosts_file.write(b''.join(hosts_file_contents))
print('Flushing DNS cache...')
subprocess.call(['ipconfig','/flushdns'])


print("Spawning the webserver. Exit with ctrl-c")
httpd = HTTPServer(('127.0.0.1', 80), SimpleHTTPRequestHandler)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("Got stopped, doing cleanup...")
    with open(hosts_file_path,'wb') as hosts_file:
        with open(backup_filename,'rb') as backup:
            print("Restoring backup")
            hosts_file.write(backup.read())
    os.remove(backup_filename)