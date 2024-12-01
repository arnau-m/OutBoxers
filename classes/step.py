#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# Definir la clase Step
class step:

    def __init__(self, in1, in2, in3, in4):
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4
        
        # Velocidad de paso
        self.step_sleep = 0.001

        # Número de pasos para mover -30 grados
        self.step_count = int(((-30 * 4096) / 360))  # Aproximadamente -343 pasos

        # Definir la dirección para mover -30 grados (True = antihorario)
        self.direction = True  # False para sentido horario, True para antihorario

        # Secuencia del motor paso a paso
        self.step_sequence = [[1, 0, 0, 1],
                              [1, 0, 0, 0],
                              [1, 1, 0, 0],
                              [0, 1, 0, 0],
                              [0, 1, 1, 0],
                              [0, 0, 1, 0],
                              [0, 0, 1, 1],
                              [0, 0, 0, 1]]

        # Configuración de pines
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        GPIO.setup(in3, GPIO.OUT)
        GPIO.setup(in4, GPIO.OUT)

        # Inicialización de los pines
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)

        self.motor_pins = [in1, in2, in3, in4]
        self.motor_step_counter = 0

    def cleanup(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)

    def start(self):
        self.direction = True
        # Movimiento principal
        try:
            # Mover -30 grados (sentido antihorario)
            for i in range(abs(self.step_count)):  # Usamos abs() para asegurar que los pasos sean positivos
                for pin in range(0, len(self.motor_pins)):
                    GPIO.output(self.motor_pins[pin], self.step_sequence[self.motor_step_counter][pin])

                if self.direction == True:
                    self.motor_step_counter = (self.motor_step_counter - 1) % 8
                elif self.direction == False:
                    self.motor_step_counter = (self.motor_step_counter + 1) % 8
                else:  # Programación defensiva
                    print("La dirección debe ser True (antihorario) o False (horario)")
                    exit(1)

                time.sleep(self.step_sleep)

            # Esperar 1 segundo
            time.sleep(1)

            # Volver a la posición inicial (+30 grados en sentido horario)
            self.direction = False  # Cambiar la dirección a horario

            for i in range(abs(self.step_count)):  # Mover +30 grados (sentido horario)
                for pin in range(0, len(self.motor_pins)):
                    GPIO.output(self.motor_pins[pin], self.step_sequence[self.motor_step_counter][pin])

                if self.direction == True:
                    self.motor_step_counter = (self.motor_step_counter - 1) % 8
                elif self.direction == False:
                    self.motor_step_counter = (self.motor_step_counter + 1) % 8
                else:  # Programación defensiva
                    print("La dirección debe ser True (antihorario) o False (horario)")
                    exit(1)

                time.sleep(self.step_sleep)

        finally:
            print("Fin step")
