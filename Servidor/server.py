import socket
import threading
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Obtener la ruta del directorio donde está este script (server.py)
basedir = os.path.abspath(os.path.dirname(__file__))
# Unir esa ruta con el nombre de tu archivo de credenciales
ruta_env = os.path.join(basedir, "Credenciales.env")

# Cargar el archivo usando la ruta completa
load_dotenv(ruta_env)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

HOST = '127.0.0.1'
TCP_PORT = 12000
UDP_PORT = 12001

def save_to_supabase(origin, content):
    """Inserta los datos recibidos en la tabla central"""
    try:
        data = {
            "origen": origin,
            "contenido": content
        }
        response = supabase.table("datos_central").insert(data).execute()
        print(f"Guardado en BD [{origin}]: {content[:30]}...")
    except Exception as e:
        print(f"Error al guardar en Supabase: {e}")

def handle_tcp():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, TCP_PORT))
    server_socket.listen(5)
    print(f"Servidor TCP escuchando en el puerto {TCP_PORT}...")
    
    while True:
        try:
            client_socket, address = server_socket.accept()
            data = client_socket.recv(4096).decode('utf-8')
            if data:
                save_to_supabase("TCP", data)
            client_socket.close()
        except Exception as e:
            print(f"Error en TCP: {e}")

def handle_udp():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, UDP_PORT))
    print(f"Servidor UDP escuchando en el puerto {UDP_PORT}...")
    
    while True:
        try:
            data, address = server_socket.recvfrom(4096)
            message = data.decode('utf-8')
            save_to_supabase("UDP", message)
        except Exception as e:
            print(f"Error en UDP: {e}")

if __name__ == "__main__":
    # Iniciar hilos separados para TCP y UDP
    tcp_thread = threading.Thread(target=handle_tcp)
    udp_thread = threading.Thread(target=handle_udp)
    
    tcp_thread.daemon = True
    udp_thread.daemon = True
    
    tcp_thread.start()
    udp_thread.start()
    
    print("Servidores iniciados correctamente. Presiona Ctrl+C para salir.")
    
    # Mantener el programa principal activo
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Apagando servidores...")