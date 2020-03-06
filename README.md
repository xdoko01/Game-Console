# Game-Console
Full-featured game console based on pygame that can be integrated in your python game in order to execute python command/scripts/custom in-gamefunctions

![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/02_console01_start.png)

## Main Features
* fully configurable look&feel via json - fonts, pictures, commands, console layouts, paddings, scrolling text and more
* history of inputed commands available upon pressing up/down buttons
* scrollable output available upon pressing pgUp/pgDown buttons
* configurable transparency and wallpaper support
* optional header/footer text that can contain dynamic in-game values (time, fps, anything else)
* header/footer layouts supporting scrolling and more
* optional fluent animation during showing/hiding of the console
* support for running custom scripts (batches of console commands)
* support for colored texts, big inputs, big outputs
* easy integration into your existing code

## Running the code
All logic including example game is implemented in game_console.py file. Make sure you have pygame 1.9.4 installed and run the code.

* You will see pygame window with rectancle movind in random directions - simulation of game

* By pressing F1 button you can toggle on/off console

* By pressing Esc key or closing the window or typing 'quick'/'exit' will end the program

## How to use console features

### Python Commands
When instantiating Console class you need to specify reference to the main game class that you want to manage. Instance of this class is then referenced as 'game'. Using console, you can then use standard python code with this instance. Python commands must start either with 'shell' keyword or simple exclamation mark '!'.

Examples of couple python commands that can be used with the example game are below:

* <i>shell print('Hello world')</i>     # Prints Hello world on console
* <i>!print('Hello world')</i>      # Same as above
* <i>!game</i>      # Prints <__main__.TestObject object at 0xXXXXXXXX> i.e. reference to the main object that is govern by the console
* <i>!game.pos = [10,10]</i>      # Changes position of the game rectancle
* <i>!game.surf.fill((0,0,0))</i>     # Changes the color of the game rectancle from white to black
* <i>!game.console.padding.up = 30</i>      # Changes the space between upper console corner and first console element (header or other depending on console layout settings)
* <i>!game.cons_get_time()</i>      # Prints output of the function on the console output.
* <i>!1+1</i>     # Prints 2 on the output
* <i>![a for a in range(10)]</i>      # Prints list of values from 0 to 9 on the output
* <i>!import os</i>     # Prints 'invalid syntax'. Such python operations are not allowed from the console due to security reasons

![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/07_console01_cmd_py.png)

### Generic Commands

### Custom Commands

### Console Scripts

### Dynamic information in header/footer

## Changing console layout/configuration

## Hints for implementation of console into my own game
