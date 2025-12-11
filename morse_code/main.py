from machine import Pin

from morse_code import MorseGenerator

def set_pin(pin):
    pin.value(1)

def unset_pin(pin):
    pin.value(0)

if __name__ == "__main__":

    onboardLED = Pin(25, Pin.OUT)

    generator = MorseGenerator(bps=4)
    sequence = generator.generate("Hello world!")

    sequence.run(
        set=(lambda: set_pin(onboardLED)),
        unset=(lambda: unset_pin(onboardLED))
    )