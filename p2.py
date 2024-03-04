import concurrent.futures
import time

# Función que será ejecutada por el executor
def ejecutar_programa():
    while True:
        print("Ejecutando programa...")
        time.sleep(1)

# Función para iniciar el programa
def iniciar_programa(executor):
    print("Iniciando programa...")
    # Iniciar el programa utilizando el executor
    future = executor.submit(ejecutar_programa)
    return future

# Función para detener el programa
def detener_programa(future):
    print("Deteniendo programa...")
    # Cancelar la ejecución del futuro
    future.cancel()

if __name__ == "__main__":
    # Crear un executor ThreadPool
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Iniciar el programa
        future = iniciar_programa(executor)

        # Esperar un tiempo antes de detener el programa
        time.sleep(5)

        # Detener el programa
        detener_programa(future)

        # Esperar otro tiempo antes de iniciar el programa nuevamente
        time.sleep(5)

        # Iniciar el programa nuevamente
        future = iniciar_programa(executor)

        # Esperar un tiempo antes de finalizar el programa
        time.sleep(5)

        # Detener el programa
        detener_programa(future)

    print("Programa finalizado.")
