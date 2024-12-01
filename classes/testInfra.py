import RPi.GPIO as GPIO
import time
import threading
from queue import Queue
from infra import infra

def main():
    # Configuración del pin y tiempo de espera
    pin_infra = 7  # Cambiar al pin correcto
    sleep_time = 0.01

    # Cola para enviar el contador de eventos
    count_queue = Queue()

    # Crear una instancia de la clase infra
    myInfra = infra(pin_infra, sleep_time)

    # Crear un hilo para ejecutar la detección de infrarrojos
    infra_thread = threading.Thread(target=myInfra.start, args=(count_queue,))
    infra_thread.start()

    # Monitorear los eventos en el hilo principal
    try:
        count = 0
        while True:
            if not count_queue.empty():
                count += count_queue.get()  # Obtenemos el contador desde la cola
                print(f"Eventos detectados: {count}")
                if count >= 10:  # Detenemos el programa después de 10 eventos
                    myInfra.stop()
                    print("Evento límite alcanzado. Deteniendo el programa.")
                    break
            time.sleep(0.1)  # Un pequeño retraso para evitar un uso excesivo de la CPU
    except KeyboardInterrupt:
        print("Deteniendo el programa...")
        myInfra.stop()
        infra_thread.join()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
