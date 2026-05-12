import socket
import time
import random

HOST = '127.0.0.1'
PORT = 12001

def run_udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Iniciando cliente UDP al puerto {PORT}...")
    
    try:
        while True:
            # Simulamos datos de telemetría (ej. temperatura, humedad, ID de sensor)
            sensor_id = random.randint(1, 100)
            temperatura = round(random.uniform(15.0, 45.0), 2)
            estado = random.choice(["OK", "WARNING", "CRITICAL"])
            
            data = f"Sensor_{sensor_id},{temperatura},{estado}"
            
            # Enviamos el paquete
            client_socket.sendto(data.encode('utf-8'), (HOST, PORT))
            print(f"Enviado (UDP): {data}")
            
            time.sleep(0.5) # Envío cada 0.5 segundos
    except KeyboardInterrupt:
        print("\nCliente UDP detenido.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    run_udp_client()