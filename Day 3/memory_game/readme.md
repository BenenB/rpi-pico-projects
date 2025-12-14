### Configuration

Using the components and setup from 12 days of codemas day 3:
https://thepihut.com/blogs/raspberry-pi-tutorials/maker-advent-calendar-day-3-bashing-buttons

This example is set up with the input pins on virtual pins 11, 12 & 13 which correspond to physical pins 15, 16 & 17
This is the only deviation from the example in the article

This project requires the file `memory_game.py` to be preloaded onto the device so that it can be imported by `main.py`
 - Connect your device and then open the `memory_game.py` file in thonny
 - With te file open select 'Save As', this will prompt you to choose the storage device (Computer or Connected Device)
 - Choose Connected Device and name the file `memory_game.py`


### Design

The code assumes very little about the existing setup, for example:

 - The order of the buttons is not assumed to correspond to the order of the lights
   - instead it asks you to assign a button to each light as you configure the game controller

 - The game logic is designed to be independent from the logic controlling the physical board
   - This is accomplished by creating classes to represent the functionality of the lights/buttons
   - These classes accept functions to operate them as parameters in their constructors
   - You can see this with the lambda functions in `main.py`