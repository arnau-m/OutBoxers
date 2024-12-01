#!/usr/bin/python3
from step import step  # Asegúrate de que el archivo step.py esté en el mismo directorio o en el PATH

# Definir los pines que usarás
in1 = 13  # Pin 11
in2 = 12  # Pin 12
in3 = 15  # Pin 13
in4 = 37  # Pin 15

# Crear una instancia del motor paso a paso
motor = step(in1, in2, in3, in4)

# Iniciar el movimiento
motor.start()
