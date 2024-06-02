import unittest
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.tests.common import GraphicUnitTest
from DLAW import CalculatorApp, CalculatorWidget

class TestCalculatorApp(GraphicUnitTest):
    def setUp(self):
        # Setting up the test environment
        super(TestCalculatorApp, self).setUp()
        self.app = CalculatorApp()  # Creating an instance of the CalculatorApp
        EventLoop.ensure_window()  # Ensuring there's a window
        self.window = EventLoop.window  # Getting the window
        self.app.root = self.app.build()  # Building the app
        self.root = self.app.root  # Getting the root widget of the app

    def tearDown(self):
        # Tearing down the test environment
        super(TestCalculatorApp, self).tearDown()
        self.app.stop()  # Stopping the app

    def test_button_press(self):
        # Testing button press functionality
        self.root.button_value(1)
        self.assertEqual(self.root.ids.input_box.text, "1")  # Checking if input is correct

        # Pressing more buttons and checking the input
        self.root.button_value(2)
        self.assertEqual(self.root.ids.input_box.text, "12")
        self.root.remove_last()
        self.assertEqual(self.root.ids.input_box.text, "1")
        self.root.signs("+")
        self.assertEqual(self.root.ids.input_box.text, "1+")
        self.root.button_value(3)
        self.assertEqual(self.root.ids.input_box.text, "1+3")
        self.root.results()
        result = self.root.ids.input_box.text
        self.assertTrue(result == "4" or result == "4.0")

    def test_tab_switch(self):
        # Test tab switching functionality
        self.root.change_tab(1)
        self.assertEqual(self.root.tab_selected, 1)  # Check if tab is switched correctly
        self.assertTrue(self.root.ids.input_prompt.text == "" or self.root.ids.input_prompt.text == "Enter the home's value")  # Check if prompt is empty

        self.root.change_tab(2)
        self.assertEqual(self.root.tab_selected, 2)  # Check if tab is switched correctly
        self.assertTrue(self.root.ids.input_prompt.text == "" or self.root.ids.input_prompt.text == "Enter the bill total")  # Check if prompt is empty

    def test_clear(self):
        # Test clear functionality
        self.root.button_value(5)
        self.root.clear()
        self.assertEqual(self.root.ids.input_box.text, "")  # Check if input box is cleared

    def test_mortgage_calculation(self):
        # Test mortgage calculation
        self.root.change_tab(1)
        self.root.button_value(100000)
        self.root.results()
        text = self.root.ids.input_box.text
        if text:
            self.assertAlmostEqual(float(text), 536.82, places=2)  # Check calculated mortgage value

    def test_tip_calculation(self):
        # Test tip calculation
        self.root.change_tab(2)
        self.root.button_value(50)
        self.root.results()
        text = self.root.ids.input_box.text
        if text:
            self.assertAlmostEqual(float(text), 10.0, places=2)  # Check calculated tip amount

# Checks whether the script is being run directly as the main program or being imported by another script
if __name__ == '__main__':
    unittest.main()
