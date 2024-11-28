''' Test Console Command 

    Examples of usage:
        "test"         ... get usage instructions
        "test -h"      ... get usage instructions
        "test --help"  ... get usage instructions
        "test 1 2 p=x" ... write any input parameters to the console
'''

instructions = """
    Examples of usage:
        "test"         ... get usage instructions
        "test -h"      ... get usage instructions
        "test --help"  ... get usage instructions
        "test 1 2 p=x" ... write any input parameters to the console
"""

def initialize(register, module_name):
    '''Console Command registers itself at Console'''
    # Mandatory line
    register(fnc=cons_cmd_test, alias=module_name)
    # Optional names for the console command
    register(fnc=cons_cmd_test, alias='TEST')

def cons_cmd_test(game_ctx, params):
    ''' Test Console Command implementation
    '''

    # Save all parameters passed from the Console in the list
    all_params = params.split()
    no_of_params = len(all_params) - 1 # exclude the script name

    # Show instructions if the last parametr indicates so
    if all_params[-1] in ('-h','--help', '?', 'help') or no_of_params < 1:
        print(instructions)

    # Print all the parameters on the console
    else:
        print(f'Parameters: {all_params}')
        print(f'Game handler details: {game_ctx.__dir__()}')
        return 0
