from machine import Pin
import time
from morse_code import MorseGenerator,MultiSequenceRunner

if __name__ == "__main__":

    yellow = Pin(18, Pin.OUT)
    green = Pin(19, Pin.OUT)
    red = Pin(20, Pin.OUT)

    generator = MorseGenerator()
    
    red_seq = generator.generate(
        "Hello world from RED",
        set=(lambda: red.value(1)),
        unset=(lambda: red.value(0))
    )
    red_seq.name = "Red"
    
    green_seq = generator.generate(
        "GREEN says Hello world",
        set=(lambda: green.value(1)),
        unset=(lambda: green.value(0))
    )
    green_seq.name = "Green"
    
    yellow_seq = generator.generate(
        "Deireann BUI dia duit ar domhan",
        set=(lambda: yellow.value(1)),
        unset=(lambda: yellow.value(0))
    )
    yellow_seq.name = "Yellow"
    
    runner = MultiSequenceRunner(bps=8)
    runner.add_sequence(red_seq)
    runner.add_sequence(green_seq)
    runner.add_sequence(yellow_seq)
    
    runner.run_sequences()
    
    print("Done")
    
    