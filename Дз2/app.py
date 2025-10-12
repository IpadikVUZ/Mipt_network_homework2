import socket
import sys

HOST = '127.0.0.1'
PORT = 9999

def tcp_server():
    socket_listening = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    socket_listening.bind((HOST, PORT))
    socket_listening.setsockopt ( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    socket_listening.listen(1)
    print(f"TCP Server started on {HOST}:{PORT}")
    
    while True:

        client_socket, client_adress = socket_listening.accept()
        print(f"Connected from adress {client_adress}")

        try:

            with client_socket:

                while True:

                    buffer = bytearray()

                    while True:

                        chunk = client_socket.recv(1024)

                        if not chunk:
                            break

                        buffer.extend(chunk)

                        if len(chunk) < 1024:
                            break
                    
                    if not buffer:
                        print(f"Connection with client {client_adress} closed.")
                        break

                    received_message = buffer.decode('utf-8')
                    print(f"Got ( {len(received_message)} bytes): {received_message[:70]}..." )

                    answer = input("Enter answer: ")
                    client_socket.sendall(answer.encode('utf-8'))

        except ConnectionResetError:
            print(f"Connection with {client_adress} reset.")

        print("Server is ready for new connection.")

def tcp_client():

    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        socket_client.connect((HOST, PORT))

        while True:

            message = input("Enter message or 'exit' or 'large ( to test big file)': ")
            if message == 'exit':
                break
            
            if message == 'large':

                payload = 'Z' * 20000
                socket_client.sendall(payload.encode('utf-8'))

            else:

                socket_client.sendall(message.encode('utf-8'))
            
            buffer = bytearray()

            while True:

                data_part = socket_client.recv(1024)

                if not data_part:
                    break

                buffer.extend(data_part)

                if len(data_part) < 1024:
                    break
            
            print(f"Server answer: {buffer.decode('utf-8')}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        socket_client.close()

def udp_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_socket.bind((HOST, PORT))

    print(f"UDP Server started on {HOST}:{PORT}")
    
    while True:

        buffer, client_adress = server_socket.recvfrom(65535)

        received_message = buffer.decode('utf-8')

        print(f"Got: {received_message} from adress {client_adress} ")
        
        answer = input("Enter answer: ")
        server_socket.sendto(answer.encode('utf-8'), client_adress)

def udp_client():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_addr = (HOST, PORT)
    
    while True:

        message = input(">> Enter message or 'exit' to exit: ")
        if message == 'exit':
            break
        
        s.sendto(message.encode('utf-8'), server_addr)
        
        data, addr = s.recvfrom(65535)
        print(f"Response from {addr}: {data.decode('utf-8')}")
    
    s.close()

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Use app.py <role> <protocol>")
        sys.exit(1)

    role = sys.argv[1]
    protocol = sys.argv[2]

    if protocol == "tcp":
        if role == "server":
            tcp_server()
        elif role == "client":
            tcp_client()

    elif protocol == "udp":
        if role == "server":
            udp_server()
        elif role == "client":
            udp_client()