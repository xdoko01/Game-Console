'''
	Example of the use of the Console
	For showing/hiding console press F1
'''

import pygame

from  pygame_console import Console
from random import randint
from datetime import datetime

class TestObject:
    ''' Testing object that will be govern by console.
    Print moving square on the screen with the console
    '''

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.pos = [0,0]
        self.exit = False
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((255,255,255))

        ''' Console integration code - START
            ********************************
        '''
        # Generate random console config (no parameter) or specify the layout by nums 1 to 6
        console_config = self.get_console_config(1)

        # Create console based on the config - feel free to implement custom code to read the config directly from json
        self.console = Console(self, self.screen.get_width(), console_config)
        
        ''' Console integration code - END
            ********************************
        '''

    def update(self):
        while not self.exit:
            
            # Reset the screen
            self.screen.fill((125, 125, 0))

            # Move the square randomly
            self.pos[0] += randint(-2,2) 
            self.pos[1] += randint(-2,2)

            # Test of puting something to the console
            #self.console.write('position X: ' + str(self.pos[0]))

            if self.pos[0] > 500: self.pos[0] = 500
            if self.pos[0] < 100: self.pos[0] = 100
            if self.pos[1] > 500: self.pos[1] = 500
            if self.pos[1] < 100: self.pos[1] = 100
            
            # Process the keys
            events = pygame.event.get()
            for event in events:
                
                # Exit on closing of the window
                if event.type == pygame.QUIT: self.exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: self.exit = True
                elif event.type == pygame.KEYUP:						
                    # Toggle console on/off the console							
                    if event.key == pygame.K_F1: 						
                        # Toggle the console - if on then off if off then on
                        self.console.toggle()

            # Update the game situation - blit square on screen and position
            self.screen.blit(self.surf, (int(self.pos[0]), int(self.pos[1])))

            # Read and process events related to the console in case console is enabled
            self.console.update(events)	

            # Display the console if enabled or animation is still in progress
            self.console.show(self.screen)

            pygame.display.update()
            self.clock.tick(30)

    def move(self, move_x, move_y):
        ''' first argumet is movement on x-axis
            second argument is movement on y-axis
        ''' 
        #move_x, move_y = line.split(',')
        self.pos[0] += int(move_x) 
        self.pos[1] += int(move_y) 

    def cons_get_pos(self):
        ''' Example of function that can be passed to console to show dynamic
        data in the console
        '''
        return str(self.pos)
    
    def cons_get_time(self):
        ''' Example of function that can be passed to console to show dynamic
        data in the console
        '''
        return str(datetime.now())

    def cons_get_details(self):
        ''' Example of function that can be passed to console to show dynamic
        data in the console
        '''
        
        return str('Input text buffer possition: ' + str(self.console.console_input.buffer_position) + ' Input text position: ' + str(len(self.console.console_input.input_string)))

    def cons_get_input_spacing(self):
        return str('TextInput spacing: ' + str(self.console.console_input.line_spacing) + 
            ' Cursor pos: ' + str(self.console.console_input.cursor_position) +
            ' Buffer pos: ' + str(self.console.console_input.buffer_offset))

    def get_console_config(self, sample=None):
        
        # Select random console from 1 to 6
        if not sample: sample = randint(1,6)
        
        # Sample 1: Full console features + top animation with 2s timing
        if sample == 1:
            return {
                    'global' : {
                        'cmd_pckg_path': 'pygame_console.commands',
                        'script_path': 'pygame_console/scripts/',
                        'animation': ['TOP', 2000],
                        'layout' : 'INPUT_BOTTOM',
                        'padding' : (10,10,20,20),
                        'bck_color' : (125,125,125),
                        'bck_image' : 'pygame_console/backgrounds/quake.png',
                        'bck_image_resize' : True,
                        'bck_alpha' : 150,
                        'welcome_msg' : 'Sample 1: Full feature console + top animation with 2s timing\n***************\nType "exit" to quit\nType "help"/"?" for help\nType "? shell" for examples of python commands',
                        'welcome_msg_color' : (0,255,0),
                        },
                    'header' : {
                        'text' : 'Console v0.1. Position: {} Time: {} ',
                        'text_params' : [[None, 'cons_get_pos'], [None,'cons_get_time']],												
                        'layout' : ['SCROLL_LEFT_CONTINUOUS', 0, 2],
                        'padding' :(10,10,10,10),
                        'font_file' : 'pygame_console/fonts/IBMPlexMono-Regular.ttf',
                        'font_size' : 12,
                        'font_antialias' : True,
                        'font_color' : (255,255,255),
                        'font_bck_color' : None,
                        'bck_color' : (255,0,0),
                        'bck_image' : 'pygame_console/backgrounds/quake.png',
                        'bck_image_resize' : True,
                        'bck_alpha' : 100
                        },
                    'output' : {
                        'padding' : (10,10,10,10),
                        'font_file' : 'pygame_console/fonts/JackInput.ttf',
                        'font_size' : 16,
                        'font_antialias' : True,
                        'font_color' : (255,255,255),
                        'font_bck_color' : (55,0,0),
                        'bck_color' : (55,0,0),
                        'bck_alpha' : 120,
                        'buffer_size' : 100,
                        'display_lines' : 20,
                        'display_columns' : 100,
                        'line_spacing' : None
                        },
                    'input' : {
                        'padding' : (10,10,10,10),
                        'font_file' : 'pygame_console/fonts/JackInput.ttf',
                        'font_size' : 16,
                        'font_antialias' : True,
                        'font_color' : (255,0,0),
                        'font_bck_color' : None,
                        'bck_color' : (0,255,0),
                        'bck_alpha' : 75,
                        'prompt' : '>>>',
                        'max_string_length' : 10,
                        'repeat_keys_initial_ms' : 400,
                        'repeat_keys_interval_ms' :35
                        },
                    'footer' : {						
                        'text' : '{} ',
                        'text_params' : [[None, 'cons_get_input_spacing']],
                        'layout' : ['SCROLL_RIGHT_CONTINUOUS',100,1],
                        'padding' : (10,10,10,10),
                        'font_file' : 'pygame_console/fonts/IBMPlexMono-Regular.ttf',
                        'font_size' : 10,
                        'font_antialias' : True,
                        'font_color' : (255,255,255),
                        'font_bck_color' : None,
                        'bck_color' : (0,0,0),
                        'bck_image' : None,
                        'bck_image_resize' : True,
                        'bck_alpha' : 100
                        }
                    }

        # Sample 2: Full featured - no footer, no header + bottom animation with default timing and INPUT_TOP layout
        if sample == 2:
            return {
                    'global' : {
                        'cmd_pckg_path': 'commands',
                        'script_path': 'pygame_console/scripts/',
                        'animation' : ['BOTTOM'],
                        'layout' : 'INPUT_TOP',
                        'padding' : (10,10,20,20),
                        'bck_color' : (125,125,125),
                        'bck_image' : 'pygame_console/backgrounds/quake.png',
                        'bck_image_resize' : True,
                        'bck_alpha' : 150,
                        'welcome_msg' : 'Sample 2: Full featured, no footer, no header + bottom animation + Input top layout\n***************\nType "exit" to quit\nType "help"/"?" for help\nType "? shell" for examples of python commands',
                        'welcome_msg_color' : (0,255,0),
                        },
                    'output' : {
                        'padding' : (10,10,10,10),
                        'font_file' : 'pygame_console/fonts/JackInput.ttf',
                        'font_size' : 16,
                        'font_antialias' : True,
                        'font_color' : (255,255,255),
                        'font_bck_color' : (55,0,0),
                        'bck_color' : (55,0,0),
                        'bck_alpha' : 120,
                        'buffer_size' : 100,
                        'display_lines' : 20,
                        'display_columns' : 100,
                        'line_spacing' : None							
                        },
                    'input' : {
                        'padding' : (10,10,10,10),
                        'font_file' : 'pygame_console/fonts/JackInput.ttf',
                        'font_size' : 16,
                        'font_antialias' : True,
                        'font_color' : (255,0,0),
                        'font_bck_color' : None,
                        'bck_color' : (0,255,0),
                        'bck_alpha' : 75,
                        'prompt' : '>>>',
                        'max_string_length' : 10,
                        'repeat_keys_initial_ms' : 400,
                        'repeat_keys_interval_ms' :35
                        }
                    }
        
        # Sample 3: Mimimal - only header
        if sample == 3:
            return {
                'header' : {
                    'font_file' : 'pygame_console/fonts/IBMPlexMono-Regular.ttf',
                    'text' : 'Sample 3: Minimal - only header. Current Time: {} ',
                    'text_params' : [[None, 'cons_get_time']],												
                    'layout' : ['SCROLL_LEFT_CONTINUOUS', 0, 2],
                    }
                }

        # Sample 4: Mimimal - only header and footer
        if sample == 4:
            return {
                'header' : {
                    'font_file' : 'pygame_console/fonts/IBMPlexMono-Regular.ttf',
                    'text' : 'Sample 4: Minimal - only header and footer. Current Position: {} ',
                    'text_params' : [[None,'cons_get_pos']],												
                    'layout' : ['SCROLL_LEFT_CONTINUOUS', 0, 2]
                    },
                'footer' : {						
                    'text' : 'Sample 4: Minimal - only header and footer ',
                    'layout' : ['SCROLL_RIGHT_CONTINUOUS',100,1],
                    'font_file' : 'pygame_console/fonts/IBMPlexMono-Regular.ttf'
                    }
                }

        # Sample 5: Mimimal - only header and input, output on stdout
        if sample == 5:
            return {
                'header' : {
                    'font_file' : 'pygame_console/fonts/IBMPlexMono-Regular.ttf',
                    'text' : 'Sample 5: Minimal - only header and input, output on stdout. Current Pos: {} ',
                    'text_params' : [[None,'cons_get_pos']],												
                    'layout' : ['TEXT_CENTRE']
                    },
                'input' : {
                    'font_file' : 'pygame_console/fonts/JackInput.ttf'
                    }
                }

        # Sample 6: Mimimal - only input and output, with transparency and welcome msg
        if sample == 6:
            return {
                'global' : {
                    'cmd_pckg_path': 'commands',
                    'script_path': 'pygame_console/scripts/',
                    'layout' : 'INPUT_BOTTOM',
                    'padding' : (10,10,10,10),
                    'bck_alpha' : 150,
                    'welcome_msg' : 'Sample 6: Mimimal - only input and output, with transparency and welcome msg\n***************\nType "exit" to quit\nType "help"/"?" for help\nType "? shell" for examples of python commands',
                    'welcome_msg_color' : (0,255,0)
                    },
                'input' : {
                    'font_file' : 'pygame_console/fonts/JackInput.ttf',
                    'bck_alpha' : 0
                    },
                'output' : {
                    'font_file' : 'pygame_console/fonts/JackInput.ttf',
                    'bck_alpha' : 0,
                    'display_lines' : 20,
                    'display_columns' : 100
                    }
                }

# Initiate testing 'game'
t = TestObject()

# Enter the infinite loop - press Esc to exit or type 'exit' into the console
t.update()