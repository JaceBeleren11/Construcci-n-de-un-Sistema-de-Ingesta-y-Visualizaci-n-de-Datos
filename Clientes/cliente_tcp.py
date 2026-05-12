import socket
import time
import csv
import os

# Configuración del servidor
HOST = '127.0.0.1'
PORT = 12000
CSV_FILE = 'olist_orders_dataset.csv' # Asegúrate de tener el archivo en la ruta o ajusta la ruta

def run_tcp_client():
    # Comprobar si existe el archivo
    if not os.path.exists(CSV_FILE):
        print(f"Error: El archivo {CSV_FILE} no se encuentra en la ruta.")
        return

    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader) # Saltar el encabezado
            
            print(f"Iniciando conexión TCP al puerto {PORT}...")
            
            for row in csv_reader:
                # Creamos el socket TCP
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((HOST, PORT))
                
                # Convertimos la fila a cadena de texto separada por comas
                data = ','.join(row)
                
                # Enviamos los datos
                client_socket.sendall(data.encode('utf-8'))
                print(f"Enviado (TCP): {data[:50]}...")
                
                client_socket.close()
                time.sleep(1) # Pausa de 1 segundo
                
    except Exception as e:
        print(f"Conexión terminada o error: {e}")

if __name__ == "__main__":
    run_tcp_client()