# Challenge 3: Sistema de Chat con Sockets (TCP)

Este proyecto implementa un protocolo de comunicación en tiempo real utilizando **Python** y librerías estándar de red. El objetivo es establecer una arquitectura Cliente-Servidor funcional y resiliente a fallos.

## 📂 Descripción de Archivos

* **`servidor.py`**: Script principal que gestiona la red. Acepta conexiones, administra la lista de usuarios y distribuye los mensajes.
* **`cliente.py`**: Interfaz de terminal para el usuario. Se conecta al servidor y permite enviar/recibir mensajes simultáneamente.

## ⚙️ Funcionamiento Técnico

### 1. Servidor (Lógica No Bloqueante)
El servidor no atiende a los clientes uno por uno, sino a todos simultáneamente mediante la librería `select`.
* **Gestión de Conexiones:** Utiliza `select.select` para monitorear múltiples sockets a la vez. Esto permite detectar actividad (nuevos mensajes o conexiones) sin detener la ejecución del programa.
* **Broadcast:** Al recibir un mensaje, el servidor recorre su diccionario de clientes conectados y reenvía los datos a todos los sockets activos, excepto al remitente.
* **Limpieza de Recursos:** Si un cliente se desconecta (recibe bytes vacíos), el servidor lo elimina de la lista y cierra el socket para liberar memoria.

### 2. Cliente (Concurrencia)
El cliente debe realizar dos tareas opuestas al mismo tiempo: esperar mensajes del servidor y esperar que el usuario escriba en el teclado.
* **Multithreading:** Se implementa un hilo secundario (`threading.Thread`) que se dedica exclusivamente a escuchar (`recv`) los mensajes entrantes.
* **Hilo Principal:** El proceso principal se mantiene libre para capturar la entrada del teclado (`input`) y enviarla al servidor.

---

## 📝 Informe del Desafío

### ¿Quién eres después de este reto?
Un desarrollador con comprensión del nivel bajo de la red (Sockets y TCP). Entiendo cómo se establecen las conexiones, cómo se transmiten los bytes y la importancia de gestionar los estados de conexión manualmente sin depender de frameworks web.

### ¿Cómo sobrevivió tu aplicación?
La aplicación logra estabilidad mediante dos mecanismos:
1.  **Manejo de Excepciones:** Bloques `try/except` en los ciclos principales del servidor y cliente para capturar errores de red (como `BrokenPipeError` o desconexiones abruptas) sin detener el programa.
2.  **I/O Asíncrono:** El uso de `select` en el servidor evita que un cliente con mala conexión bloquee el chat para los demás usuarios.

### ¿Qué aprendiste cuando todo se rompió?
* La necesidad de decodificar y codificar (`encode`/`decode`) los mensajes al pasar de texto a bytes.
* La importancia de cerrar correctamente los sockets (`socket.close()`) en bloques `finally` para no dejar recursos del sistema operativo ocupados.
* Cómo sincronizar procesos de lectura y escritura usando hilos.

---
**Estado:** Finalizado ✅ 
