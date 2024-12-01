from ina219 import INA219
from ina219 import DeviceRangeError
import time

class power:
    
    def __init__(self, kwh):
        # Configura el INA219
        SHUNT_OHMS = 0.1  # Valor de la resistencia shunt
        self.ina = INA219(shunt_ohms=SHUNT_OHMS, busnum=1)
        self.ina.configure()
        self.kwh = kwh

    def start(self):
        while True:
            try:
                self.kwh =+ self.kwh + self.ina.power() / 3600
                time.sleep(1)
            except DeviceRangeError as e:
                # Este error ocurre si la corriente excede el rango del sensor
                print(f"Error: {e}")
        
    def getPower(self):
        return self.kwh
        

