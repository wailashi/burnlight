import subprocess
import wiringpi2

OUT = 'out'
IN = 'in'

wiringpi2.wiringPiSetupSys()


class Pin:

    def __init__(self, pin, mode):
        self.pin = pin
        self.mode = mode
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

    def is_on(self):
        if wiringpi2.digitalRead(self.pin) == 1:
            return True
        else:
            return False


class Channel:

    def __init__(self, input_pin, output_pin):
        """

        :type input_pin: Pin
        :type output_pin: Pin
        """
        self.input = input_pin
        self.output = output_pin

    def on(self):
        self.output.on()

    def off(self):
        self.output.off()

    def set(self, state):
        self.output.set(state)

    def is_valid(self):
        if self.output.is_on() == self.input.is_on():
            return True
        else:
            return False


channels = {1: Channel(Pin(17, IN), Pin(4, OUT))}
