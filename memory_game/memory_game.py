import time
import random


class MemoryGameLight:
    def __init__(self, on: function, off: function):
        if not (on and off):
            raise ValueError("An 'on' and 'off' function must be defined for each light")
        self.on = on
        self.off = off

class MemoryGameSwitch:
    def __init__(self, status: function):
        if not status:
            raise ValueError("A 'status' function must be defined for each switch")
        self.status = status
    

class MemoryGameConfig:
    def __init__(self, leds: list[MemoryGameLight], switches: list[MemoryGameSwitch], configure: bool = True):
        if len(leds) != len(switches):
            raise ValueError("The number of switches must match the number of lights")
        self.leds = leds
        self.switches = switches
        self.configured = False
        self.light_map = {}
        self.button_map = {}
        if configure:
            self.configure_switches()

    def configure_switches(self):
        self.clear_leds()
        self.configured = False
        print("Setup buttons for memory game\nPress the button you want to use for each light as they activate...")
        for i,led in enumerate(self.leds):
            led.on()
            selected = None
            while selected is None:
                switch = self.listen_for_all_switches()
                #print(switch)
                if self.switches[switch] in self.button_map.values():
                    print("You cannot use the same button for multiple lights")
                else:
                    selected = switch
                self.wait_for_clear()
            led.off()
            self.light_map[i] = led
            self.button_map[i] = self.switches[selected]
            #print(f"configured {i}")
        print("Setup complete")
        self.configured = True

    def listen_for_all_switches(self):
        if len(self.switches) < 1:
            raise ValueError("No switches to listen for")
        
        switch_tuples = None
        if self.configured:
            switch_tuples = list(self.button_map.items())
        else:
            switch_tuples = list(enumerate(self.switches))
            
            
        while True:
            for i,sw in switch_tuples:
                if sw.status():
                    return i
            time.sleep(0.1)
                
    def wait_for_clear(self):
        while any([sw.status() for sw in self.switches]):
            continue
        
    def clear_leds(self):
        [led.off() for led in self.leds]
                
class MemoryGame:
    def __init__(self, config: MemoryGameConfig, starting_level: int = 3, starting_bps: int = 2, tempo_mod: int = 5):
        self.config = config
        self.starting_level = starting_level
        self.starting_bps = starting_bps
        self.tempo_mod = tempo_mod
        self.options = len(config.switches)
        
    
    def play(self):
        if not self.config.configured:
            raise ValueError(f"Game controller not configured")
        self.level = self.starting_level
        self.lives = 1
        
        while self.lives > 0:
            result = self.run_level(self.level)
            if result:
                self.level_complete(1 + self.level - self.starting_level)
                self.level += 1
            else:
                self.lives -= 1
                if self.lives > 0:
                    self.lose_life()
        
        self.game_over()
                
    def run_level(self, level: int):
        true_level = level - self.starting_level
        if true_level < 0:
            raise ValueError("Level is less than starting level")
        
        if (true_level % self.tempo_mod):
            print(f"Level: {true_level + 1}")
        else:
            print(f"Level: {true_level + 1} -- tempo increased!")
            
        tempo_bumps = int(true_level/self.tempo_mod)
        
        sequence_length = level - (2 * tempo_bumps)
        bps = self.starting_bps + tempo_bumps
        
        unit_length = 1/bps
        
        sequence = [ random.randint(0,self.options-1) for i in range(sequence_length) ]
        
        time.sleep(1)
        
        for i in sequence:
            led = self.config.light_map.get(i)
            if not led:
                raise ValueError(f"No led found for light {i}")
            led.on()
            time.sleep(unit_length)
            led.off()
            time.sleep(unit_length)
            
        for i in sequence:
            player_input = self.config.listen_for_all_switches()
            self.config.light_map.get(player_input).on()
            self.config.wait_for_clear()
            self.config.light_map.get(player_input).off()
            if player_input != i:
                time.sleep(0.3)
                return False
            
        return True
    
    def level_complete(self, level: int):
        print(f"Finished level {level}")
    
    def lose_life(self):
        print(f"Uh oh! Lives remaining {self.lives}")
    
    def game_over(self):
        print("Game Over!")
            
        
                
                
            
        
        
        
        
        
        

