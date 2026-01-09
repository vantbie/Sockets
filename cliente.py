import socket
import threading #El cliente usa threading para recibir y escribir a la vez.
#import sys

def escuchar_servidor(socket_cliente):
    #Hilo receptor 
    try: 
        while True:
            datos = socket_cliente.recv(1024)
            
            if not datos:
                print("\n[cliente] se desconecto")
                break
            
            mensaje =  datos.decode()
            print(mensaje)
    except Exception as e:
        print("\n[recv] Error: ", e)
    
    finally:
        try:
            socket_cliente.close()
        
        except:
            pass
        
def iniciar_cliente(ip_servidor, puerto):
    #creamos el socket del cliente
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #conectamos el socket con el servidor
    try:
        socket_cliente.connect((ip_servidor, puerto)) #inicia el handshake TCP con la IP/puerto del servidor.
        
    except Exception as e:
        print("No se pudo conectar: ", e)
        return
    
    nombre = input("Nombre: ").strip()
    
    if not nombre:
        nombre = "anonimo"
    socket_cliente.sendall((f"/name {nombre}\n").encode())  # envía comando de nombre al servidor
    
    #crear el hilo receptor 
    hilo = threading.Thread(target = escuchar_servidor, args = (socket_cliente,), daemon=True) #daemon=True significa que el hilo se terminará automáticamente cuando el proceso principal finalice.
    hilo.start()
    
    #leer el teclado y enviar
    try:
        while True:
            linea = input()
            
            if linea.lower() == "salir":
                print("[cliente] Cerrando conexion...")
                
                try:
                    socket_cliente.shutdown(socket.SHUT_RDWR) # Corto ambos lados, adiós, SHUT_RDWR → indica que se cierran ambas direcciones (envío y recepción).
                
                except:
                    pass
                
                socket_cliente.close()
                break
            
            #asegurar terminador de lineas
            if not linea.endswith("\n"): #Revisa si una cadena termina con cierto texto.
                linea += "\n"
            
            try:
                socket_cliente.sendall(linea.encode())
            
            except BrokenPipeError: # Error al enviar datos a un socket cerrado
                print("[cliente] Conexion perdida al enviar")
                break
            
            except Exception as e:
                print("[send] Error: ", e)
                break
    
    except KeyboardInterrupt:
        print("[cliente] Interrupcion por teclado. Cerrando...")
        
        try:
            socket_cliente.close()
        
        except:
            pass

if __name__ == "__main__":
    iniciar_cliente("127.0.0.1", 8080)            
        
