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
        return f"UnsupportedSequence: {self.msg}"

    
class MorseSequence:
    def __init__(self, sequence: str, unit_length: float = 0.5):
        self.sequence = sequence
        self.unit_length = unit_length

    def run(self, set: function, unset: function, always_unset: bool = False):        
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

    def print(self):
        print(str(self))

    def __str__(self) -> str:
        return self.sequence.replace("_"," ").replace("|","   ")


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