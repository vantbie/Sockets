import socket
import select

def iniciar_servidor(host, port):
    #Crear el servidor principal
    #servidor = socket.socket(familia, tipo)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #servidor.setsockopt((nivel de red o de socket), opcion, valor) 
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Configura en el nivel del socket (SOL_SOCKET) la opción de reutilizar direcciones (SO_REUSEADDR) y actívala (1)
    
    #le asociamos un puerto
    servidor.bind((host, port)) #accede con una tupla
    
    #ponerlo a escuchar conexiones
    servidor.listen()
    
    servidor.setblocking(False) #pone el socket en modo no bloqueante.
    
    lista_sockets = [servidor]
    clientes = {}
    
    print(f"{servidor} concetado en {host}: {port}")
    
    try:
        #Entrar a un bucle para que ver los mensajes
        while True:
            # select: espera hasta que alguno de los sockets tenga datos (o nueva conexión)
            lectura, _, exepciones = select.select(lista_sockets, [], lista_sockets)
            
            for i in lectura:
                
                if i is servidor:
                    # nueva conexión entrante o sea un nuevo cliente
                    nuevo_cliente, direccion = servidor.accept()
                    nuevo_cliente.setblocking(False)
                    lista_sockets.append(nuevo_cliente)
                    clientes[nuevo_cliente] = {"buffer" : b"", "nombre": None}
                    print(f"{servidor} Nuevo Cliente conectado, con direccion: {direccion}")
                    
                else:
                    #datos desde un cliente ya existente
                    try:
                        datos = i.recv(1024) #tamaño del buffer
                        
                    except ConnectionError:
                        datos = b""
                    
                    if not datos:
                        #si es que el cliente se desconecto
                        origen = i.getpeername() #Devuelve una tupla (IP, puerto) para saber de donde es la conexion del cliente
                        print(f"{servidor} el cliente {clientes[i]["nombre"]} se desconecto: {origen}")
                        lista_sockets.remove(i)
                        del clientes[i] #elimina a ese cliente de la lista
                        i.close()
                    
                    else:
                        # aquí asumimos que los mensajes vienen por líneas '\n'
                        clientes[i]["buffer"] += datos
                        
                        while b"\n" in clientes[i]["buffer"]:
                            linea, clientes[i]["buffer"] = clientes_partir_por_saltos(clientes[i]["buffer"])
                            mensaje = linea.decode().strip() #convierte str a bytes
                            origen = i.getpeername()
                            
                            #si el cliente no tiene nombre, el primer mensaje es su nombre
                            if clientes[i]["nombre"] is None:
                                clientes[i]["nombre"] = mensaje
                                #print(f"[CLIENTE] {origen} -> {mensaje}")
                                i.sendall(f"Nombre registrado como: {mensaje}\n".encode()) #convierte bytes a str
                                continue
                            
                            nombre = clientes[i]["nombre"]
                            enviar = f"{nombre} ({origen[0]} : {origen[1]}) : {mensaje}\n".encode()
                            print(f"[MSG] {nombre} ({origen[0]} : {origen[1]}) -> {mensaje}")
                            
                            #broadcast a todos menos al remitente
                            for destino in list(clientes.keys()):
                                if destino is not i:
                                    try:
                                        destino.sendall(enviar)
                                    except Exception:
                                        # si falla el envio, eliminar el socket 
                                        lista_sockets.remove(destino)
                                        del clientes[destino]
                                        destino.close()
                    
            for i in exepciones:
                #limpieza rapida si hay exepciones en el select
                if i in lista_sockets:
                    lista_sockets.remove(i)
                
                if i in clientes:
                    del clientes[i]
                
                try:
                    i.close()
                except:
                    pass
    
    except KeyboardInterrupt:
        print(f"\n{servidor} cerrado por Ctrl+C")
    
    #cerrar todos los sockets abiertos para liberar los recursos del sistema.
    finally:
        for i in lista_sockets:
            try:
                i.close()
            except:
                pass

# pequeña función helper para separar la primera línea y dejar resto en buffer
def clientes_partir_por_saltos(bytes_del_buffer):
    linea, resto = bytes_del_buffer.split(b"\n", 1)
    return linea, resto

if __name__ == "__main__":
    iniciar_servidor(host = '0.0.0.0' , port = 8080)