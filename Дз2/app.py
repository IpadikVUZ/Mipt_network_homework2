import socket
import sys
import argparse
import struct


def send_message(sock, message):
    encoded_message = message.encode('utf-8')
    prefix = struct.pack('!I', len(encoded_message))
    sock.sendall(prefix + encoded_message)

def receive_message(sock):
    prefix_data = receive_all(sock, 4)
    if not prefix_data:
        return None
    
    message_length = struct.unpack('!I', prefix_data)[0]
    
    return receive_all(sock, message_length).decode('utf-8')

def receive_all(sock, n):
    buffer = bytearray()
    while len(buffer) < n:
        packet = sock.recv(n - len(buffer))
        if not packet:
            return None
        buffer.extend(packet)
    return buffer

def tcp_server(host, port):
    socket_listening = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_listening.bind((host, port))
    socket_listening.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_listening.listen(5)
    print(f"TCP Server started on {host}:{port}")
    
    while True:
        client_socket, client_adress = socket_listening.accept()
        print(f"Connected from adress {client_adress}")
        try:
            with client_socket:
                while True:
                    received_message = receive_message(client_socket)
                    
                    if received_message is None:
                        print(f"Connection with client {client_adress} closed.")
                        break

                    print(f"Got ( {len(received_message)} bytes): {received_message[:70]}...")

                    answer = input("Enter answer: ")
                    send_message(client_socket, answer)

        except ConnectionResetError:
            print(f"Connection with {client_adress} reset.")
        print("Server is ready for new connection.")

def tcp_client(host, port):
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_client.connect((host, port))
        print(f"Successfully connected to {host}:{port}")
        while True:
            message = input("Enter message or 'exit' or 'large': ")
            if message.lower() == 'exit':
                break
            
            payload = message
            if message.lower() == 'large':
                payload = 'Z' * 300000
            
            send_message(socket_client, payload)
            
            server_answer = receive_message(socket_client)
            if server_answer is None:
                print("Server closed the connection.")
                break
            
            print(f"Server answer: {server_answer}")

    except ConnectionRefusedError:
        print(f"Error: Connection refused. Is the server running on {host}:{port}?")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        socket_client.close()

def udp_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"UDP Server started on {host}:{port}")
    
    while True:
        buffer, client_adress = server_socket.recvfrom(65535)
        received_message = buffer.decode('utf-8')
        print(f"Got: {received_message} from adress {client_adress} ")
        answer = input("Enter answer: ")
        server_socket.sendto(answer.encode('utf-8'), client_adress)

def udp_client(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (host, port)
    
    try:
        while True:
            message = input(">> Enter message or 'exit' to exit: ")
            if message.lower() == 'exit':
                break
            s.sendto(message.encode('utf-8'), server_addr)
            data, addr = s.recvfrom(65535)
            print(f"Response from {addr}: {data.decode('utf-8')}")
    finally:
        s.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('role', choices=['server', 'client'])
    parser.add_argument('protocol', choices=['tcp', 'udp'])
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=9999)
    
    args = parser.parse_args()

    if args.protocol == "tcp":
        if args.role == "server":
            tcp_server(args.host, args.port)
        elif args.role == "client":
            tcp_client(args.host, args.port)
    elif args.protocol == "udp":
        if args.role == "server":
            udp_server(args.host, args.port)
        elif args.role == "client":
            udp_client(args.host, args.port)