import subprocess
import wiringpi2

OUT = 'out'
IN = 'in'

wiringpi2.wiringPiSetupSys()

class Pin(object):

    def __init__(self, pin, mode):
        self.set_mode(pin, mode)

    def set_mode(self, pin, mode):
        subprocess.call(['gpio', 'export', str(pin), str(mode)], shell=False)
        self.pin = pin
        self.mode = mode

    def on(self):
        wiringpi2.digitalWrite(self.pin, 1)

    def off(self):
        wiringpi2.digitalWrite(self.pin, 0)

    def set(self, state):
        if state == 'ON':
            self.on()
        elif state == 'OFF':
            self.off()
        else:
            raise ValueError


    def isOn(self):
        if wiringpi2.digitalRead(self.pin) == 1:
            return True
        else:
            return False


class Channel(object):

    def __init__(self, input, output):
        self.input = input
        self.output = output


    def on(self):
        self.output.on()


    def off(self):
        self.output.off()


    def set(self, state):
        self.output.set(state)


    def isValid(self):
        if self.output.isOn() == self.input.isOn():
            return True
        else:
            return False


channels = {1 : Channel(Pin(17, IN), Pin(4, OUT))}
