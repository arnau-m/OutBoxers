import time
from gpiozero import DistanceSensor

class ultra:
    def __init__(self, trig, echo, sleep, distance):
        self.trig = trig #23
        self.echo = echo #24
        self.sleep = sleep #0.5
        self.distance = distance #1000
        self.startBool = True
        self.statBool = False
    def start(self):
        sensor = DistanceSensor(echo=self.echo, trigger=self.trig, max_distance=5)
        self.startBool = True

        while self.startBool:
            distance = sensor.distance * self.distance
            if distance > 300:
                print(distance)
                self.statBool = True
                time.sleep(3)
                
            time.sleep(self.sleep)
    def stop(self):
        self.startBool = False
    
    def getState(self):
        return self.statBool
    
    def setState(self):
        self.statBool = False

