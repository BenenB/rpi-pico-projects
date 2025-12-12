import time


MORSE_KEY = {
    'a': '.-',    'b': '-...',  'c': '-.-.',  'd': '-..',
    'e': '.',     'f': '..-.',  'g': '--.',   'h': '....',
    'i': '..',    'j': '.---',  'k': '-.-',   'l': '.-..',
    'm': '--',    'n': '-.',    'o': '---',   'p': '.--.',
    'q': '--.-',  'r': '.-.',   's': '...',   't': '-',
    'u': '..-',   'v': '...-',  'w': '.--',   'x': '-..-',
    'y': '-.--',  'z': '--..',

    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.'
}


class UnsupportedCharacterException(Exception):
    def __init__(self, message: str = ""):
        self.msg = message

    def __str__(self):
        return f"UnsupportedCharacter: {self.msg}"


class BadSequenceException(Exception):
    def __init__(self, message: str = ""):
        self.msg = message

    def __str__(self):
        return f"BadSequence: {self.msg}"
    
class NoFunctionDefinedException(Exception):
    def __init__(self, message: str = ""):
        self.msg = message

    def __str__(self):
        return f"NoFunctionDefined: {self.msg}"

    
class MorseSequence:
    def __init__(self, sequence: str, unit_length: float = 0.5, set: function = None, unset: function = None, loop: bool = False):
        self.sequence = sequence
        self.unit_length = unit_length
        self.__generate_step_sequence()
        self.sequence_length = len(self.step_sequence)
        self.set_function = set
        self.unset_function = unset
        self.loop = loop

    def define_set_function(self, fn: function):
        self.set_function = fn

    def define_unset_function(self, fn: function):
        self.unset_function = fn
     
    def run(self, set: function = None, unset: function = None, always_unset: bool = False):
        if not set:
            if not self.set_function:
                raise NoFunctionDefinedException("set not defined")
            set = self.set_function

        if not unset:
            if not self.unset_function:
                raise NoFunctionDefinedException("unset not defined")
            unset = self.unset_function
        
        if not self.sequence:
            return
        
        for char in list(self.sequence):
            if char not in ".-_|":
                raise BadSequenceException(f"Found {char} in {self.sequence}")

            if char in ".-":
                set()
            
            if char in ".":
                time.sleep(self.unit_length * 1)
            elif char in "-_":
                time.sleep(self.unit_length * 3)
            elif char in "|":
                time.sleep(self.unit_length * 7)
            
            if char in ".-":
                unset()
                time.sleep(self.unit_length)
            elif always_unset:
                unset()

    def run_step(self, step: int, set: function = None, unset: function = None):
        if not set:
            if not self.set_function:
                raise NoFunctionDefinedException("set not defined")
            set = self.set_function

        if not unset:
            if not self.unset_function:
                raise NoFunctionDefinedException("unset not defined")
            unset = self.unset_function

        if step > self.sequence_length:
            if self.loop:
                step = step % self.sequence_length
            else:
                return True
        
        instruction = self.step_sequence[step]

        if instruction == "up":
            set()
        if instruction == "down":
            unset()

        return False


    def __generate_step_sequence(self):
        steps = []
        for char in list(self.sequence):
            if char == ".":
                steps.extend(["up","down"])
            if char == "-":
                steps.extend(["up","wait","wait","down"])
            if char == "_":
                steps.extend(["wait"] * 4)
            if char == "|":
                steps.extend(["wait"] * 8)

        self.step_sequence = steps

    def __str__(self) -> str:
        return self.sequence.replace("_"," ").replace("|","   ")
    
    def print(self):
        print(str(self))
    

class MultiSequenceRunner:
    def __init__(self, bps: float = 3):
        self.sequences = []
        if bps <= 0:
            raise ValueError(f"Generator bps must be greater than 0, recieved {bps}")
        self.unit_length = 1/bps

    def add_sequence(self, sequence: MorseSequence):
        self.sequences.append(sequence)

    def run_sequences(self):
        current_sequences = self.sequences.copy()
        current_step = 0
        
        while len(current_sequences):
            seqs_to_remove = []
            for i,seq in enumerate(current_sequences):
                if seq.run_step(current_step):
                    seqs_to_remove.append(i)
            
            if seqs_to_remove:
                current_sequences = [seq for i,seq in enumerate(current_sequences) if not i in seqs_to_remove ]

            current_step += 1

class MorseGenerator:
    def __init__(self, bps: float = 3):
        if bps <= 0:
            raise ValueError(f"Generator bps must be greater than 0, recieved {bps}")
        self.unit_length = 1/bps

    # public

    def generate(self, input: str) -> MorseSequence:        
        words = input.split()
        sequence = [ self.__convert_word(word) for word in words ]
        sequence = [ word for word in sequence if word ]

        return MorseSequence(sequence="|".join(sequence), unit_length=self.unit_length)
    
    # private

    def __convert_word(self, word: str) -> str:        
        char_array = list(word.lower())
        sequence = [ self.__convert_char(char) for char in char_array ]
        sequence = [ char for char in sequence if char ]

        return "_".join(sequence)
    
    def __convert_char(self, char: str, ignore_unsupported: bool = True) -> str:
        morse = MORSE_KEY.get(char, None)
        if not morse and not ignore_unsupported:
            raise UnsupportedCharacterException(f"'{char}'")
        
        return morse