# Game-Console
Full-featured game console based on pygame that can be integrated in your python game in order to execute python command/scripts/custom in-gamefunctions

![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/02_console01_start.png)

## Main Features
* fully configurable look&feel via json - fonts, pictures, commands, console layouts, paddings, scrolling text and more
* history of inputed commands available upon pressing up/down buttons
* scrollable output available upon pressing pgUp/pgDown buttons and/or mouse wheel
* configurable transparency and wallpaper support
* optional header/footer text that can contain dynamic in-game values (time, fps, anything else)
* header/footer layouts supporting scrolling and more
* optional fluent animation during showing/hiding of the console
* commands implemented as a separate python scripts
* support for running custom scripts (batches of console commands) with parameters
* support for colored texts, big inputs, big outputs
* easy integration into your existing code

## Running the code
All console logic is implemented in the `pygame_console` package. Example game with console implementation is in `example_game.py`.
Folders `console_commands`, `console_scripts` and `console_configs` contain configurable console logic tailored for given game. Those can be further modified/extended to implement more logic / commands / scripts into the console.

Make sure you have pygame >= 1.9.4 installed and run the code.

* You will see pygame window with rectancle moving in random directions - simulation of game

* By pressing F1 button you can toggle on/off console

* By pressing Esc key or closing the window or typing 'exit' will end the program

## How to use console features

### Python Commands
When instanciating Console class you need to specify reference to the main game class that you want to manage. Instance of this class is then referenced as 'game'. Using console, you can then use standard python code with this instance. Python commands must start either with 'shell' keyword or simple exclamation mark '!'.

Examples of couple python commands that can be used with the example game are below:

* <code>shell print('Hello world')</code>     # Prints Hello world on console
* <code>!print('Hello world')</code>      # Same as above
* <code>!game</code>      # Prints <__main__.TestObject object at 0xXXXXXXXX> i.e. reference to the main object that is govern by the console
* <code>!game.pos = [10,10]</code>      # Changes position of the game rectancle
* <code>!game.surf.fill((0,0,0))</code>     # Changes the color of the game rectancle from white to black
* <code>!game.console.padding.up = 30</code>      # Changes the space between upper console corner and first console element (header or other depending on console layout settings)
* <code>!game.cons_get_time()</code>      # Prints output of the function on the console output.
* <code>!1+1</code>      # Prints 2 on the output
* <code>![a for a in range(10)]</code>      # Prints list of values from 0 to 9 on the output
* <code>!import os</code>     # Prints 'invalid syntax'. Such python operations are not allowed from the console due to security reasons

![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/07_console01_cmd_py.png)

### Custom Commands
With game-console you can specify your own commands. For implementing new command called for example <i>dummy</i> that takes one parameter and prints it on the console in the blue color, you need to perform following steps:

* create a new python file `dummy.py` and place it to `console_commands` package (or other package specified by the console `global` configuration that can be changed)
* see the existing example python files in the `console_commands`package for reference. 
  * The python file must contain `initialize` function (you can copy&paste it from example commmands). This function is called automatically when the command is first used. It manages registration of the command with the console.
  * The python file must contain also other function (with any name) that implements the command and is passed `game_ctx` (reference to the game - same as when calling `!game`) and params (command parameters)
* It is good idea to return some value in case of failure. This is important if your custom command is part of some console script (read further).

There are already several custom functions implemented in the example game <code>exit</code>, <code>move</code>, and <code>test</code>. The <code>move</code> function takes 2 parameters delimited and changes position of the main game rectancle. The <code>exit</code> command exists the game. The <code>list</code> command shows information about registered commands.

![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/03_console01_cmd_input.png)

### Generic Commands
All the non-python shell commands can be listed by typing <code>help</code> or simply <code>?</code> on the command line. The example of generic command can be <code>exit</code> that simply quicks the game. Also by typing <code>help move</code> or simply <code>?move</code> will list description of the command.

![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/08_console01_cmd_gen.png)

### Console Scripts
Python, Custom and Generic commands can be combined together into the file (one command on each line) and can be executed as a script.

Example of invoking such simple script is below:

<code>script example1.scr</code>

![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/09_console01_cmd_script.png)

If there is an error on some line of the script, you are notified on the console with the error message - see below. The error code corresponds to the return value returned in the exception statement in the code of your custom function.

![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/10_console01_cmd_script_err.png)

Console scripts also support parameters. See below the example using parameters for `example3.scr` script. Also, console script can be called from other console script.

<code>script example3.scr x=100 y=200 color=128 name=MyBrick</code>

The body of the script using those parameters is then looking as follows:

<code>
move $x $y
!print('I have moved the brick named $name')
!game.surf.fill((0, $color,0))
!print('I have colored the brick with $color')
!print("All done!")
</code>

The parameters are represented as keys starting with `$` in the source of the console script.

![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/12_console01_cmd_script_params.png)

### Dynamic information in header/footer
As mentioned above, header or footer can display dynamic data. Those data are gained as a resulf of calling of some function of the main game class. In the example game, you will see <i>time</i> and game object <i>position</i> as some of the examples of such dynamic values.

If you want to have dynamic values in your console, you need to do the following:

* Implement functions that return the requested values in string time somewhere in your game class or alternativelly in some separate module. In case of our example game there are functions <code>cons_get_pos()</code> and <code>cons_get_time()</code>. Check the code for details.
* Specify the function in configuration json. See the folder `console_configs` for examples of different configurations. Also, see below parameters `text` and `text_params` where the functions and its placement in the scrolling text is defined.

![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/11_dynamic_text_config.png)

## Changing console layout/configuration
A mentioned in the list of features, console enables heavy configuration. I suggest you to see example console configs in the `console_configs` directory and get inspiration from 6 configurations that are predifined there.
Below you can see the pictures of those configurations in the game.

### Sample Layout 1
* Scrolling dynamic text in the header and footer
* Transparency of all console parts + wallpaper
* Animation upon displaying hidding of the console set to 2s
* Different fonts for different console parts

![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/ConsoleConf01.png)

### Sample Layout 2
* Header and footer omitted by configuration
* Transparency of all console parts + wallpaper
* Animation upon displaying hidding of the console - from the bottom - default time 100ms
* Command line input is above console output part
* Different fonts for different console parts

![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/ConsoleConf02.png)

### Sample Layout 3
* Totaly minimalistic - only header with dynamic text shown
* No transparency, no wallpapers

![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/ConsoleConf03.png)

### Sample Layout 4
* Minimalistic - only header and footer with dynamic text shown
* No transparency, no wallpapers
* Header and footer are scrolling by different speed

![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/ConsoleConf04.png)

### Sample Layout 5
* Minimalistic - only input and header with dynamic text shown
* No transparency, no wallpapers

![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/ConsoleConf05.png)

### Sample Layout 6
* Minimalistic - only input and output with transparency

![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/ConsoleConf06.png)

## How to integrate console into the game
 
 * Prepare configuration JSON. Use sample configuration dicts in `console_configs` directory for inspiration
 * import Console class from pygame_console package and instantiate it
 * For switching console on/off call <code>toggle()</code> function
 * For reading the input keys and process them by console call <code>update()</code> function
 * For showing the console use <code>show()</code> function. Animation effect is processed internally.
 
 ![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/Integr01.png)
 ![screenshot](https://github.com/xdoko01/Game-Console/blob/master/pygame_console/docs/Integr02.png)

 
