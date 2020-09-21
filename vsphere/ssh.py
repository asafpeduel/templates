import paramiko
import os

host = os.getenv('VM_IP')
password = os.getenv('SSH_PASS')
username = "env0"
ssh_port = 22

server_port = 8000
command = f'''python -c "
import SimpleHTTPServer
import SocketServer

PORT = {server_port}
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(('', PORT), Handler)

httpd.serve_forever()
" > /dev/null 2>&1 &
'''

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, ssh_port, username, password)

ssh.exec_command(f'sudo kill -9 $(sudo lsof -t -i:{server_port})')

transport = ssh.get_transport()
channel = transport.open_session()

channel.exec_command(command)

print(f'serving at https://{host}:{server_port}')