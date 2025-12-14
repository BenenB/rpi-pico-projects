from machine import Pin
from memory_game import MemoryGame,MemoryGameController,MemoryGameLight,MemoryGameSwitch

if __name__ == "__main__":

    yellow = Pin(18, Pin.OUT)
    green = Pin(19, Pin.OUT)
    red = Pin(20, Pin.OUT)
    
    button_1 = Pin(11, Pin.IN, Pin.PULL_DOWN)
    button_2 = Pin(12, Pin.IN, Pin.PULL_DOWN)
    button_3 = Pin(13, Pin.IN, Pin.PULL_DOWN)
    
    
    switch_1 = MemoryGameSwitch((lambda: button_1.value()))
    switch_2 = MemoryGameSwitch((lambda: button_2.value()))
    switch_3 = MemoryGameSwitch((lambda: button_3.value()))
    
    light_1 = MemoryGameLight(
        on=(lambda: yellow.value(1)),
        off=(lambda: yellow.value(0))
    )
    
    light_2 = MemoryGameLight(
        on=(lambda: green.value(1)),
        off=(lambda: green.value(0))
    )
    
    light_3 = MemoryGameLight(
        on=(lambda: red.value(1)),
        off=(lambda: red.value(0))
    )
    
    config = MemoryGameController(
        leds = [light_1, light_2, light_3],
        switches = [switch_1, switch_2, switch_3]
    )
    
    game = MemoryGame(config)
    
    game.play()
    
    