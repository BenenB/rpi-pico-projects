import time
from machine import Pin, ADC, PWM

ADC_MIN = 400
ADC_VAR = 300
ADC_MAX = 65535

if __name__ == "__main__":

    yellow = PWM(Pin(18))
    yellow.freq(1000)

    green = PWM(Pin(19))
    green.freq(1000)

    red = PWM(Pin(20))
    red.freq(1000)
    
    potentiometer = ADC(Pin(27))
    
    while True:
        
        reading = potentiometer.read_u16()
        if reading <= ADC_MIN + ADC_VAR:
            led_varying, led_pwr = 0,0
        else:
            led_varying = int((reading*3)/ADC_MAX)
            led_pwr = (reading*3) % ADC_MAX
        
        
        print(f"read: {reading}\tled: {led_varying}\tpwr: {led_pwr}")
        time.sleep(0.1)
        
        if led_varying == 0:
            red.duty_u16(led_pwr)
            green.duty_u16(0)
            yellow.duty_u16(0)
        elif led_varying == 1:
            red.duty_u16(ADC_MAX)
            green.duty_u16(led_pwr)
            yellow.duty_u16(0)
        elif led_varying == 2:
            red.duty_u16(ADC_MAX)
            green.duty_u16(ADC_MAX)
            yellow.duty_u16(led_pwr)
        else:
            red.duty_u16(ADC_MAX)
            green.duty_u16(ADC_MAX)
            yellow.duty_u16(ADC_MAX)



