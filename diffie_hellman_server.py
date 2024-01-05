# Diffie Hellman Key Exchange Algorithm
import os
import secrets
import socket
import argparse
import threading

parser = argparse.ArgumentParser(description="Server Arguments Parser")
parser.add_argument('--host', metavar='HostIP', type=str, nargs='?', default=socket.gethostbyname(socket.gethostname()))
parser.add_argument('--port', metavar='PortNum', type=int, nargs='?', default=5050)
args = parser.parse_args()

HEADER = 8
ADDR = (args.host, args.port)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!X-X!"


# Public Key
G = 3
P = secrets.randbits(2048)
print(P)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
	server.bind(ADDR)
except Exception as e:
	raise SystemExit(f"[ERROR] Could not bind server to Host: {args.host} on Port: {args.port}\n" + str(e))


def send(sock, data):
	data = str(data).encode(FORMAT)
	send_length = str(len(data)).encode(FORMAT)
	send_length += b' ' * (HEADER - len(send_length))
	sock.send(send_length)
	sock.send(data)
	

def mod_calculation(base, exponent, mod):
	product = 1
	while exponent > 0:
		if exponent & 1:
			product = (product * base) % mod
		exponent = exponent >> 1
		base = base ** 2 % mod
	return product


def handle_client(conn, addr):
	print(f"[NEW CONNECTION] IP: {addr[0]} on PORT: {addr[1]}\n")
	send(conn, P)

	secret = int.from_bytes(os.urandom(32), 'big')  # 32 bytes
	print(f"[SECRET] Secret Exponent: {secret}" + "\n" * 2)
	diffie = mod_calculation(G, secret, P)
	# print(diffie)
	print(f"[RESULT OF B ^ X mod M] {diffie}")
	send(conn, diffie)

	client_diffie_length = int(conn.recv(HEADER).decode(FORMAT))
	client_diffie = int(conn.recv(client_diffie_length).decode(FORMAT))
	print("\n" * 3 + f"[RECEIVED] Client's Diffie Value: {client_diffie}")

	private_key = mod_calculation(client_diffie, secret, P)
	print("\n" * 3 + "[PRIVATE KEY] Private Key Received: " + "\n" * 3)
	print(private_key)
	conn.close()


def start():
	server.listen(5)  # Listen for new connections - Backlog(Buffer) is 5 connections
	print(f"[LISTENING] Server is listening on {ADDR[0]}")
	try:
		while True:
			conn, addr = server.accept()
			thread = threading.Thread(target=handle_client, args=(conn, addr))  # Creates a new thread with client
			thread.start()
			print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
	except KeyboardInterrupt:
		server.shutdown(socket.SHUT_RDWR)
		server.close()
		raise SystemExit("[SHUTDOWN] Gracefully shutting down server")


if __name__ == '__main__':
	print("[STARTING] server is starting...")
	start()
