import unittest
import sys
import io
import os
from unittest.mock import patch, MagicMock

# Import the tested class
#from pgconsole import CommandLineProcessor

# If running directly from the repo for testing, you might need to adjust sys.path:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pgconsole import CommandLineProcessor 


# Mock the external str_to_package_module function
def mock_str_to_package_module(parent_module, absolute_path):
    # This mock simulates loading a module and its initialize function
    mock_module = MagicMock()
    # Define a default initialize behavior for the mock module
    # The actual initialize in your commands package should call the passed register_command
    mock_module.initialize.side_effect = lambda register_fnc, name: register_fnc(MagicMock(name=f"cmd_fnc_{name}"), name)
    return mock_module

# Patch pygame.time.get_ticks() globally for these tests, always return 0 ticks
patch_pygame_get_ticks = patch('pygame.time.get_ticks', side_effect=0)

# Patch the external str_to_package_module function
patch_str_to_package_module = patch('pgconsole.str_to_package_module', side_effect=mock_str_to_package_module)


class TestCommandLineProcessor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start global patches
        patch_pygame_get_ticks.start()
        patch_str_to_package_module.start()

    @classmethod
    def tearDownClass(cls):
        # Stop global patches
        patch_pygame_get_ticks.stop()
        patch_str_to_package_module.stop()

    def setUp(self):

        # Mock app and output objects
        self.mock_app = MagicMock(name='mock_app')
        self.mock_output = MagicMock(name='mock_output')
        self.mock_output.font_color_error = (255, 0, 0) # Define mock colors
        self.mock_output.font_color_info = (0, 255, 0)
        self.mock_output.write.reset_mock() # Clear calls from previous tests

        # Use StringIO for capturing stdout/stdin that cmd.Cmd might use
        self.mock_stdin = io.StringIO()
        self.mock_stdout_capture = io.StringIO()

        # Instantiate the processor
        self.processor = CommandLineProcessor(
            app=self.mock_app,
            input=self.mock_stdin,
            output=self.mock_output,
            cmd_pckg_path="mock_cmd_package", # Dummy package path
            script_path="mock_script_path" # Dummy script path
        )

        # Reset internal command storage
        self.processor._cmd_scripts = {}

    def tearDown(self):
        # Restore sys.stdout just in case
        sys.stdout = sys.__stdout__

    # Initialization Tests
    def test_initialization(self):
        """Test if the CommandLineProcessor initializes correctly."""
        self.assertIs(self.processor.app, self.mock_app)
        self.assertIs(self.processor.output, self.mock_output)
        self.assertIs(self.processor.input, self.mock_stdin)
        self.assertEqual(self.processor.cmd_pckg_path, "mock_cmd_package")
        self.assertEqual(self.processor.script_path, "mock_script_path")
        self.assertIsInstance(self.processor._cmd_scripts, dict)
        self.assertEqual(len(self.processor._cmd_scripts), 0)

    # Command Registration Tests
    def test_register_command_success(self):
        """Test successful registration of a command."""
        command_fnc = self.processor.register_command("testcmd")
        self.assertIsNotNone(command_fnc)
        self.assertIn("testcmd", self.processor._cmd_scripts)
        self.assertIsInstance(self.processor._cmd_scripts["testcmd"], MagicMock)

    def test_register_command_module_not_found(self):
        """Test registration when the command module is not found."""
        with patch('pgconsole.str_to_package_module', side_effect=ValueError("Module not found")):
            with self.assertRaisesRegex(ValueError, 'Error during loading of py script command module "mock_cmd_package.nonexistent_cmd".'):
                self.processor.register_command("nonexistent_cmd")
            # Ensure output.write was not called for this error, as it raises.
            self.mock_output.write.assert_not_called()

    def test_register_command_module_initialize_error(self):
        """Test registration when command module's initialize method fails."""
        
        # Prepare the mock module with failing initialize function
        mock_module = MagicMock()
        mock_module.initialize.side_effect = ValueError("Init failed")

        # Run test so that str_to_package fails with initiation
        with patch('pgconsole.str_to_package_module', return_value=mock_module):
            with self.assertRaises(ValueError):
                self.processor.register_command("failing_init_cmd")
            
            # Check if error message was written to output
            self.mock_output.write.assert_called_once_with(
                'Error during initiating/registering of command module "mock_cmd_package.failing_init_cmd".',
                color=self.mock_output.font_color_error
            )

    def test_get_command_already_registered(self):
        """Test getting a command that is already registered."""
        
        # Manually pre-register a command
        mock_fnc = MagicMock(name="already_registered_cmd_fnc")
        self.processor._cmd_scripts["precmd"] = mock_fnc
        
        retrieved_fnc = self.processor.get_command("precmd")
        self.assertIs(retrieved_fnc, mock_fnc)

    def test_get_command_not_registered(self):
        """Test getting a command that is not yet registered (should register it)."""
        retrieved_fnc = self.processor.get_command("newcmd")
        self.assertIsNotNone(retrieved_fnc)
        self.assertIn("newcmd", self.processor._cmd_scripts)

    # Basic `cmd.Cmd` Overrides Tests ---
    def test_emptyline(self):
        """Test that emptyline does nothing."""
        # emptyline is called by cmd.Cmd's cmdloop, or can be called directly
        # It should just pass
        result = self.processor.emptyline()
        self.assertIsNone(result) # Should return None or implicitly nothing
        self.mock_output.write.assert_not_called() # No output on empty line

    def test_default_calls_do_py_script(self):
        """Test that default method calls do_py_script with the line."""
        # Patch do_py_script to confirm it's called
        with patch.object(self.processor, 'do_py_script') as mock_do_py_script:
            self.processor.default("some_line arg1")
            mock_do_py_script.assert_called_once_with("some_line arg1")

    def test_do_list(self):
        """Test do_list command."""
        self.processor._cmd_scripts = {"cmd1": MagicMock(), "cmd2": MagicMock()}
        self.processor.do_list("")
        
        self.assertEqual(self.mock_output.write.call_count, 2)
        # Check first call
        self.mock_output.write.call_args_list[0].assert_called_with(
            f"Registered commands: {self.processor._cmd_scripts.keys()}", # Uses a dict_keys object, so compare directly
            color=self.mock_output.font_color_info
        )
        # Check second call
        self.mock_output.write.call_args_list[1].assert_called_with(
            f"See the {self.processor.cmd_pckg_path} package for list of all scripted commands",
            color=self.mock_output.font_color_info
        )

    def test_do_EOF(self):
        """Test do_EOF command (CTRL-D behavior)."""
        with patch.object(self.processor, 'do_py_script') as mock_do_py_script:
            mock_do_py_script.return_value = -1 # Simulate py_script returning a value to exit
            result = self.processor.do_EOF("")
            mock_do_py_script.assert_called_once_with("exit")
            self.assertEqual(result, -1) # Expect it to return the value from do_py_script

    # do_shell Tests
    def test_do_shell_prints_output(self):
        """Test do_shell executes Python code and captures print output."""
        sys.stdout = self.mock_stdout_capture # Redirect real stdout for this test
        self.processor.do_shell("print('Hello from shell')")
        self.mock_output.write.assert_called_once_with("Hello from shell\n")
        self.mock_output.write.reset_mock() # Clear mock calls for next assertion if any

    def test_do_shell_accesses_app_object(self):
        """Test do_shell can access the app object."""
        self.mock_app.some_property = "initial"
        self.processor.do_shell("game.some_property = 'changed'")
        self.assertEqual(self.mock_app.some_property, "changed")
        self.mock_output.write.reset_mock()

    # do_py_script Tests
    def test_do_py_script_success(self):
        """Test successful execution of a python script command."""
        mock_py_script_fnc = MagicMock(name="mock_py_script_fnc")
        # Ensure get_command returns our mock_py_script_fnc
        with patch.object(self.processor, 'get_command', return_value=mock_py_script_fnc) as mock_get_command:
            sys.stdout = self.mock_stdout_capture
            self.processor.do_py_script("my_script_name param1 param2")
            
            mock_get_command.assert_called_once_with("my_script_name")
            mock_py_script_fnc.assert_called_once_with(game_ctx=self.mock_app, params="my_script_name param1 param2")
            self.mock_output.write.assert_called_once_with("") # Expect empty string if script does not print
            self.mock_output.write.reset_mock()
            self.assertEqual(sys.stdout, sys.__stdout__) # stdout restored

            # Test with script printing something
            self.mock_stdout_capture.seek(0)
            self.mock_stdout_capture.truncate(0) # Clear StringIO
            mock_py_script_fnc.reset_mock()
            mock_py_script_fnc.side_effect = lambda game_ctx, params: print("Script output!")
            
            self.processor.do_py_script("my_script_name")
            #self.assertEqual(self.mock_stdout_capture.getvalue(), "Script output!\n")
            self.mock_output.write.assert_called_once_with("Script output!\n")

    def test_do_py_script_handles_exception(self):
        """Test do_py_script handles exceptions during script execution."""
        mock_py_script_fnc = MagicMock(name="mock_py_script_fnc")
        mock_py_script_fnc.side_effect = RuntimeError("Script failed!")
        with patch.object(self.processor, 'get_command', return_value=mock_py_script_fnc):
            result = self.processor.do_py_script("failing_script")
            self.assertEqual(result, -1)
            self.mock_output.write.assert_called_once_with(
                "Script failed!",
                color=self.mock_output.font_color_error
            )
            self.assertEqual(sys.stdout, sys.__stdout__) # stdout restored even on error

    def test_do_py_script_get_command_error(self):
        """Test do_py_script handling error from get_command (e.g., module not found)."""
        with patch.object(self.processor, 'get_command', side_effect=ValueError("No such module")):
            result = self.processor.do_py_script("nonexistent_script")
            self.assertEqual(result, -1)
            self.mock_output.write.assert_called_once_with(
                "No such module",
                color=self.mock_output.font_color_error
            )

    # do_script Tests
    def test_do_script_help(self):
        """Test do_script with -h or --help prints instructions."""
        self.processor.do_script("-h")
        self.mock_output.write.assert_called_once_with(unittest.mock.ANY, color=self.mock_output.font_color_info)
        # Check if the content contains expected instructions
        self.assertIn("Examples of usage:", self.mock_output.write.call_args[0][0])
        self.mock_output.write.reset_mock()

        self.processor.do_script("--help")
        self.mock_output.write.assert_called_once_with(unittest.mock.ANY, color=self.mock_output.font_color_info)


if __name__ == '__main__':
    unittest.main()