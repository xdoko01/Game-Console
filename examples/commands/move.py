''' Move Console Command 

    Examples of usage:
        "move"         ... get usage instructions
        "move -h"      ... get usage instructions
        "move --help"  ... get usage instructions
        "move 200 300" ... move to the new position

'''

instructions = """
    Examples of usage:
        "move"         ... get usage instructions
        "move -h"      ... get usage instructions
        "move --help"  ... get usage instructions
        "move 200 300" ... move to the new position
"""

def initialize(register, module_name):
    '''Console Command registers itself at Console'''
    # Mandatory line
    register(fnc=cons_cmd_move, alias=module_name)

def cons_cmd_move(game_ctx, params):
    ''' Move Console Command implementation
    '''

    # Save all parameters passed from the Console in the list
    all_params = params.split()
    no_of_params = len(all_params) - 1 # exclude the script name

    # Show instructions if the last parametr indicates so
    if all_params[-1] in ('-h','--help', '?', 'help'):
        print(instructions)

    # Print all the parameters on the console
    else:
        try:
            game_ctx.move(move_x=all_params[1], move_y=all_params[2]) # omit the command name
            return None
        except Exception as E:
            print(str(E))
            return -1

