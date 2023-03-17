

import jmri

class AutomatExample(jmri.jmrit.automat.AbstractAutomaton) :

    def __init__(self, pb, lb, ln):
        self.penultimateBlock = pb
        self.lastBlock = lb
        self.locoNumber = ln

    def init(self):
        self.lastSensor = sensors.provideSensor(self.lastBlock)
        self.penultimateSensor = sensors.provideSensor(self.penultimateBlock)
        self.throttle = self.getThrottle(self.locoNumber, True)
        if (self.throttle == None) :
            print("Couldn't assign throttle!")

    def handle(self):
        if not self.throttle:
            print("abandoning running of train")
            return 0
        
        # Turn off debounce temporarily for penultimate sensor
        #penultimateSensorDebounce = self.penultimateSensor.getSensorDebounceGoingInActiveTimer()
        #print('Saving debounce setting ' + str(penultimateSensorDebounce))
        #self.penultimateSensor.setSensorDebounceGoingInActiveTimer(0)

        # Start the train
        print('Starting train')
        self.throttle.setIsForward(True)
        self.throttle.setSpeedSetting(0.4)
       
        # Wait for penultimate sensor in forward direction to trigger
        print('Waiting for penultimate sensor to go active')
        self.waitSensorActive(self.penultimateSensor)
        #print('Slow train to intermediate speed')
        #self.throttle.setSpeedSetting(0.2)

        # Wait for final sensor in forward direction to trigger
        print('Waiting last sensor to go active')
        self.waitSensorActive(self.lastSensor)
        print('Slow down train to crawl')
        self.throttle.setSpeedSetting(0.1)

        # Wait for penultimate sensor to go inactive
        print('Waiting for penultimate sensor to go inactive and then allow 500 msec')
        self.waitSensorInactive(self.penultimateSensor)

        # Wait half a second and then stop the train
        self.waitMsec(500)
        print('Set speed to 0')
        self.throttle.setSpeedSetting(0.0)

        # Restore the debounce setting for the penultimate sensor
        #self.penultimateSensor.setSensorDebounceGoingInActiveTimer(penultimateSensorDebounce)

        return 0

a = AutomatExample('LS17', 'LS22', 2203)
a.start()
