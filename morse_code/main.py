from machine import Pin
import time
from morse_code import MorseGenerator,MultiSequenceRunner

def set_pin(pin):
    pin.value(1)

def unset_pin(pin):
    pin.value(0)

if __name__ == "__main__":

    onboardLED = Pin(25, Pin.OUT)
    yellow = Pin(18, Pin.OUT)
    green = Pin(19, Pin.OUT)
    red = Pin(20, Pin.OUT)

    generator = MorseGenerator()
    
    red_seq = generator.generate("Hello world from RED")
    red_seq.define_set_function((lambda: set_pin(red)))
    red_seq.define_unset_function((lambda: unset_pin(red)))
    red_seq.loop = False
    
    green_seq = generator.generate("GREEN says Hello world")
    green_seq.define_set_function((lambda: set_pin(green)))
    green_seq.define_unset_function((lambda: unset_pin(green)))
    green_seq.loop = False
    
    yellow_seq = generator.generate("Deireann BUI dia duit ar domhan")
    yellow_seq.define_set_function((lambda: set_pin(yellow)))
    yellow_seq.define_unset_function((lambda: unset_pin(yellow)))
    yellow_seq.loop = False
    
    runner = MultiSequenceRunner(bps=8)
    runner.add_sequence(red_seq)
    runner.add_sequence(green_seq)
    runner.add_sequence(yellow_seq)
    
    runner.run_sequences()
    
    print("Done")
    
    