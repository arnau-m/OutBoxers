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
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Datos de conexión al IoT Hub
CONNECTION_STRING = "HostName=ra-develop-bobstconnect-01.azure-devices.net;DeviceId=LAUZHACKPI4;SharedAccessKey=TFLRpk7EvnFijUvH9aS2xzfks1xRRBxSiAIoTHaJfDw="
ARCHIVO_CSV = 'count.csv'
EQUIPMENT_ID = "lauzhack-pi4"
DATASOURCE = "10.0.4.103:80"



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

    def send_machine_event(self, event_type, job_id, job_output_unit_count, total_output_unit_count, production_time, machine_speed, power, timestamp):
        event_data =[ 
            {
                "type": event_type,
                "datasource": "10.0.4.103:80",
                "equipmentId": self.machine_id,
                "jobId": job_id,
                "jobOutputUnitCount": job_output_unit_count,
                "totalOutputUnitCount": total_output_unit_count,
                "totalProductionTime": production_time,
                "machinespeed": machine_speed,
                "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "totalworkingenergy": power
            }
        ]
            
        event_json = json.dumps(event_data)
        message = Message(event_json)
        message.content_type = "application/json"
        message.content_encoding = "utf-8"
        message.custom_properties["messageType"] = "MachineEvent"
        
        print(event_data)
        print("Enviando evento de máquina...")
        self.device_client.send_message(message)
        print("Evento de máquina enviado con éxito.")

    def send_message_to_iot_hub(self, event_data):
        try:
            json_data = json.dumps(event_data)
            machine_event_message = Message(json_data)
            machine_event_message.content_type = "application/json"
            machine_event_message.content_encoding = "utf-8"
            machine_event_message.custom_properties["messageType"] = "MachineEvent"
            logging.info(f"Sending JSON message to IoT Hub: {json_data}")
            self.device_client.send_message(machine_event_message)
            logging.info("Message sent successfully!")
        except Exception as e:
            logging.error(f"Failed to send message to IoT Hub: {e}")

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
    
    
    # Connect to IoT Hub
    logging.info("Connecting to IoT Hub...")
    device.connect()
    logging.info("Connected successfully!")

    # Set initial timestamp for the day before, at midnight
    start_timestamp = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    start_timestamp = start_timestamp.replace(hour=0, minute=0, second=0, microsecond=0)

    # Simulation loop for the entire day, incrementing by 10 minutes
    job_id = "CerealBox-1"
    job_output_count = 0
    production_time = 0

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
        while start_timestamp.hour < 24:

            # Create a start production event
            start_event = device.send_machine_event(
                "startProducing",
                job_id,
                job_output_count,
                count,
                production_time,
                speed,
                power,
                start_timestamp
            )
            device.send_message_to_iot_hub(start_event)
            
            if not count_queue.empty():
                count += count_queue.get()
                job_output_count += 1
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

            # Simulate production for 1 minutes
            production_duration = 60  # 600 seconds = 1 minutes
            production_time += production_duration

            # Move timestamp forward by 10 minutes
            start_timestamp += datetime.timedelta(minutes=1)

            # Create a stop production event after 1 minutes of production
            stop_event = device.send_machine_event(
                "stopProducing",
                job_id,
                job_output_count,
                count,
                production_time,
                speed,
                power,
                start_timestamp
            )
            device.send_message_to_iot_hub(stop_event)

            # Move timestamp forward by another 1 minutes for the next cycle
            start_timestamp += datetime.timedelta(minutes=1)

            # Wait a short time to simulate processing delay (to avoid flooding)
            time.sleep(2) 

    except KeyboardInterrupt:
        print("Interrupción por teclado, cerrando.")
