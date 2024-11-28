''' Exit Console Command 

    Examples of usage:
        "exit"         ... exits the game
        "exit -h"      ... get usage instructions
        "exit --help"  ... get usage instructions
'''

instructions = """
    Examples of usage:
        "exit"         ... exits the game
        "exit -h"      ... get usage instructions
        "exit --help"  ... get usage instructions
"""

def initialize(register, module_name):
    '''Console Command registers itself at Console'''
    # Mandatory line
    register(fnc=cons_cmd_exit, alias=module_name)

def cons_cmd_exit(game_ctx, params):
    ''' Exit Console Command implementation
    '''

    # Save all parameters passed from the Console in the list
    all_params = params.split()
    no_of_params = len(all_params) - 1 # exclude the script name

    # Show instructions if the last parametr indicates so
    if all_params[-1] in ('-h','--help', '?', 'help'):
        print(instructions)

    # Print all the parameters on the console
    else:
        game_ctx.exit = True
        print(f'Exiting ...')
        return 0
