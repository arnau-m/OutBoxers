import RPi.GPIO as GPIO
import time

class rotaryEncoder:
    def __init__(self, servo_pin, encoder_a, encoder_b, button_pin, servo_position):
        self.servo_pin = servo_pin
        self.encoder_a = encoder_a
        self.encoder_b = encoder_b
        self.button_pin = button_pin
        self.servo_position = servo_position
        self.startBool = True

    def start(self):  
        self.startBool = True
        if self.startBool:
            # Configuración de GPIO
            GPIO.setmode(GPIO.BOARD)  # Usamos numeración BOARD (basada en los pines físicos)

            # Configura los pines del encoder como entradas
            GPIO.setup(self.encoder_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.encoder_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Configura el botón como entrada

            # Configuración del servo (PWM en el pin 11)
            GPIO.setup(self.servo_pin, GPIO.OUT)
            servo = GPIO.PWM(self.servo_pin, 50)  # Frecuencia de 50Hz
            servo.start(0)  # Comienza con el pulso apagado

            # Inicializar el servo a 0 grados
            servo.ChangeDutyCycle(9)
            time.sleep(2)  # Esperamos 2 segundos

            # Variables para el control del encoder
            last_encoder_a = GPIO.input(self.encoder_a)
            servo_position = 9

            def read_encoder():
                nonlocal last_encoder_a, servo_position

                current_encoder_a = GPIO.input(self.encoder_a)
                if current_encoder_a != last_encoder_a:  # Si hubo un cambio en el estado de A
                    if GPIO.input(self.encoder_b) != current_encoder_a:
                        servo_position += 0.5  # Gira hacia atrás
                    else:
                        servo_position -= 0.5  # Gira hacia adelante

                    # Limita la posición del servo entre 0 y 180 grados (mapeado entre 2 y 12)
                    servo_position = max(2, min(12, servo_position))

                    # Actualiza el PWM del servo con la nueva posición
                    servo.ChangeDutyCycle(servo_position)

                last_encoder_a = current_encoder_a  # Actualiza el valor de A

            def stop_servo():
                nonlocal servo_position
                servo.ChangeDutyCycle(0)  # Detiene el PWM del servo
                servo_position = 9
                time.sleep(1)  # Espera un poco para que el servo se detenga

            # Bucle principal
            try:
                while True:
                    # Comprobar si el botón fue presionado
                    if GPIO.input(self.button_pin) == GPIO.LOW:  # El botón está presionado (activo en LOW)
                        stop_servo()  # Detener el servo si el botón se presiona
                    else:
                        read_encoder()  # Lee el encoder y ajusta la posición del servo

                    time.sleep(0.01)  # Ajuste de la frecuencia de muestreo
            except KeyboardInterrupt:
                stop_servo()
