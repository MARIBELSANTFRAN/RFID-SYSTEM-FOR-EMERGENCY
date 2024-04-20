import socket
import threading

# Lista para guardar los sockets de los clientes conectados
clients = {}

# Función para manejar las conexiones de los clientes
def handle_client(client_socket, addr):
    # Añadir el socket del cliente a la lista
    clients[client_socket] = addr
    print(f"Connection established with {addr}")

    try:
        # Enviar mensaje de alerta al cliente
        client_socket.send("Señalizacion de emergencia".encode())
    except Exception as e:
        print(f"Error sending alert to client {addr}: {e}")

    while True:
        try:
            # Recbir mensaje del cliente
            message = client_socket.recv(1024).decode()
            if not message:
                print(f"Connection with {addr} closed.")
                break
            print(f"Message from {addr}: {message}")
        except Exception as e:
            print(f"Connection with client {addr} lost because: {e}")
            break
        finally:
            # Cerrar conexión con el cliente
            client_socket.close()
            del clients[client_socket]

# Función principal para iniciar el servidor
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.137.1', 5000))
    server_socket.listen(4)
    
    print("Server started. Waiting for connections...")
    
    while True:
        client_socket, addr = server_socket.accept()
        # Iniciar un nuevo hilo para manejar la conexión con el cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

# Iniciar el servidor
if __name__ == "__main__":
    start_server()
