import time
import datetime
import csv 
import json
import threading
from queue import Queue  # Para comunicación entre hilos
from azure.iot.device import IoTHubDeviceClient, Message
from rotaryEncoder import rotaryEncoder
from infra import infra
from ultra import ultra
from step import step
from power import power

# Datos de conexión al IoT Hub
CONNECTION_STRING = "HostName=ra-develop-bobstconnect-01.azure-devices.net;DeviceId=LAUZHACKPI4;SharedAccessKey=TFLRpk7EvnFijUvH9aS2xzfks1xRRBxSiAIoTHaJfDw="
ARCHIVO_CSV = 'count.csv'

def guardar_variable(nombre_archivo, nombre_variable, valor):
    with open(nombre_archivo, mode='w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow([nombre_variable, valor])

def cargar_variable(nombre_archivo):
    try:
        with open(nombre_archivo, mode='r') as archivo_csv:
            lector = csv.reader(archivo_csv)
            for fila in lector:
                return fila[1]  # Devuelve el valor de la variable (como string)
    except FileNotFoundError:
        return None  # Si no existe el archivo, se devuelve None

class IoTDevice:
    def __init__(self, connection_string, machine_id):
        self.device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
        self.machine_id = machine_id

    def connect(self):
        self.device_client.connect()

    def send_telemetry(self, count, speed, power, count_waste):
        telemetry_data = {
            "telemetry": {
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "datasource": "10.0.4.103:80",
                "machineid": self.machine_id,
                "totaloutputunitcount": count,
                "machinespeed": speed,
                "totalworkingenergy": power,
                "totalmaterialwasted": count_waste,
            }
        }
        telemetry_json = json.dumps(telemetry_data)
        message = Message(telemetry_json)
        message.content_type = "application/json"
        message.content_encoding = "utf-8"
        message.custom_properties["messageType"] = "Telemetry"
        
        print("Enviando telemetría...")
        self.device_client.send_message(message)
        print(telemetry_data)
        print("Telemetría enviada con éxito.")

    async def send_machine_event(self, event_type, job_id, total_output_unit_count, machine_speed, power):
        event_data = {
            "type": event_type,
            "equipmentId": self.machine_id,
            "jobId": job_id,
            "totalOutputUnitCount": total_output_unit_count,
            "machinespeed": machine_speed,
            "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "totalworkingenergy": power
        }
        event_json = json.dumps([event_data])
        message = Message(event_json)
        message.content_type = "application/json"
        message.content_encoding = "utf-8"
        message.custom_properties["messageType"] = "MachineEvent"
        
        print("Enviando evento de máquina...")
        self.device_client.send_message(message)
        print("Evento de máquina enviado con éxito.")

# Ejecución
if __name__ == "__main__":
    speed = 0
    count_waste = 0
    device = IoTDevice(CONNECTION_STRING, "lauzhack-pi4")
    myInfra = infra(7, 0.01)
    myUltra = ultra(23, 24, 0.5, 1000)
    myStep = step(13, 12, 15, 37)
    myRotEncoder = rotaryEncoder(11, 29, 35, 22, 9)
    myPower = power(0)
    
    

    device.connect()

    # Crear una cola para comunicación entre hilos
    count_queue = Queue()
    velocity_queue = Queue()
    
    # Crear hilos
    first_thread = threading.Thread(target=myRotEncoder.start)
    first_thread.start()

    second_thread = threading.Thread(target=myInfra.start, args=(count_queue, velocity_queue,))
    second_thread.start()  
    
    third_thread = threading.Thread(target=myPower.start)
    third_thread.start()
    
    fourth_thread = threading.Thread(target=myUltra.start)
    fourth_thread.start()

    # Monitorear eventos del sensor infrarrojo
    try:
        count = cargar_variable(ARCHIVO_CSV)
        if count == None: count=0
        count = int(count)
        #power = cargar_variable(ARCHIVO_CSV)
        #if power == None: power=0
        #count = int(power)
        power = 0
        objective = 0
        while True:

            if not count_queue.empty():
                count += count_queue.get()
                guardar_variable(ARCHIVO_CSV, "count", count)
                print(f"Objeto detectado, cuenta actual: {count}")
                if myUltra.getState():
                    print("La caja saldra")
                    objective = count + 2
                    myUltra.setState()
                if count == objective:
                    myStep.start()
                    count_waste += 1
                    print("Caja fuera")
                    
            if not velocity_queue.empty():
                speed = velocity_queue.get()
                print(f"Velocidad actual: {speed}")
                #Obterni energia
                power = myPower.getPower()
                print(f"Potencia consumida (kWh): {power}")
                # Enviar telemetria
                device.send_telemetry(count, speed, power, count_waste)
            
            

            time.sleep(0.1)  # Evitar uso intensivo de CPU

    except KeyboardInterrupt:
        print("Interrupción por teclado, cerrando.")
