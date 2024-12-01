import RPi.GPIO as GPIO
import time

class infra:
    def __init__(self, pin, sleep):
        self.pin = pin
        self.sleep = sleep
        self.startBool = True

    def start(self, count_queue, velocity_queue):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN)

        valAnt = GPIO.input(self.pin)
        self.startBool = True

        startTime = time.time()

        while self.startBool:
            val = GPIO.input(self.pin)
            if val != valAnt:
                time.sleep(self.sleep * 10)  # sleep = 0.01
                valAnt = val
                if val == 0:
                    endTime = time.time()
                    count_queue.put(1)  # Aumentamos el contador de eventos
                    velocity_queue.put((1/(endTime - startTime))*60)
                    print("Cambio detectado, contador actualizado.")
                    startTime = time.time()
    def stop(self):
        self.startBool = False
