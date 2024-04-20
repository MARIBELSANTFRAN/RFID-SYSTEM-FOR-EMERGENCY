import socket
import pygame
import time
import threading

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Tamaño de la ventana
WIDTH, HEIGHT = 400, 300

# Crear la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Señalización de Emergencia")

# Cargar fuente
font = pygame.font.SysFont('calibri', 32)

# Función para alternar entre colores
def alternate_colors():
    while True:
        yield RED
        yield WHITE

# Función para mostrar la alerta visual
def show_alert():
    color_generator = alternate_colors()
    while True:
        # Obtener el color actual
        color = next(color_generator)

        screen.fill(color)
        if color == RED:
            message = "Vehículo de emergencia"
        else:
            message = "Despejar camino"
        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(1)

# Conectar con el servidor y recibir alertas
def receive_alerts():
    try:
        # Conectar con el servidor
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('192.168.137.1', 5000))
        print("Connected to server.")
        # Mostrar la alerta al conectarse al servidor
        show_alert()
    except Exception as e:
        print(f"Error receiving alert: {e}")
    finally:
        client_socket.close()
        print("Disconnected from server.")

# Función principal para recibir alertas
if __name__ == "__main__":
    receive_alerts()