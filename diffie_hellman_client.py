import os
import secrets
import socket
import argparse

parser = argparse.ArgumentParser(description="Server Arguments Parser")
parser.add_argument('--host', metavar='HostIP', type=str, nargs='?', default=socket.gethostbyname(socket.gethostname()))
parser.add_argument('--port', metavar='PortNum', type=int, nargs='?', default=5050)
args = parser.parse_args()

HEADER = 8
ADDR = (args.host, args.port)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!X-X!"


# Client secret
secret = int.from_bytes(os.urandom(32), 'big')  # 32 bytes --> 256 bits
print(f"[SECRET] Secret Exponent: {secret}" + "\n" * 3)


def mod_calculation(base, exponent, mod):
	product = 1
	while exponent > 0:
		if exponent & 1:
			product = (product * base) % mod
		exponent = exponent >> 1
		base = base ** 2 % mod

	return product


def send(sock, data):
	data = str(data).encode(FORMAT)
	send_length = str(len(data)).encode(FORMAT)
	send_length += b' ' * (HEADER - len(send_length))
	sock.send(send_length)
	sock.send(data)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Public Key
G = 3
P_length = int(client.recv(HEADER).decode(FORMAT))
P = int(client.recv(P_length).decode(FORMAT))

# Client Diffie
diffie = mod_calculation(G, secret, P)
# print(f"[RESULT OF B ^ X mod M] {diffie}")

server_diffie_length = int(client.recv(HEADER).decode(FORMAT))
server_diffie = int(client.recv(server_diffie_length).decode(FORMAT))
print(f"[RECEIVED] Server Diffie Value: {server_diffie}")
send(client, diffie)

private_key = mod_calculation(server_diffie, secret, P)
print("\n" * 3 + "[PRIVATE KEY] Private Key Received: ")
print(private_key)

client.close()




