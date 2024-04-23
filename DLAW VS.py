### Importing the Kivy modules as well as the regular expression module ###
from kivy.config import Config
Config.set('graphics','resizable', False)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang.builder import Builder
import re
### Registering our custom font ###
from kivy.core.text import LabelBase
LabelBase.register(name='kalam', 
                   fn_regular='Kalam/Kalam-Regular.ttf')

Builder.load_file('./calculator.kv')
Window.size = (325, 625)
### Defining constant Mortgage_Prompts, which is the list of prompts in order for the mortgage button ###
MORTAGE_PROMPTS = [
    "Enter the home's value",
    "Enter your down payment",
    "Enter the interest rate (as a decimal)",
    "Enter the term length (In years)",
    "Your monthly payment"
]
### Defining constant Tip_Prompts, which is the list of prompts in order for the mortgage button ###
TIP_PROMPTS = [
    "Enter the bill total",
    "Enter your desired tip percentage (as a decimal)",
    "You should leave the below tip"
]
### Defining a custom widget that initializes class variables to handle tab changes ###
class CalculatorWidget(Widget):
    tab_selected = 0
    mortage_values = []
    tip_values = []
### Tracking what tab we are currently on and outputing the correct prompts ###
    def change_tab(self, value):
        self.tab_selected = value
        self.mortage_values.clear()
        self.tip_values.clear()
        self.ids.input_box.text = ""

        match value:
            case 0:
                self.ids.input_prompt.text = ""
            case 1:
                self.ids.input_prompt.text = MORTAGE_PROMPTS[len(self.mortage_values)]
            case 2:
                self.ids.input_prompt.text = TIP_PROMPTS[len(self.mortage_values)]

    # Clear the screen
    def clear(self):
        self.ids.input_box.text = ""

    # Remove the last character
    def remove_last(self):
        prev_number = self.ids.input_box.text
        prev_number = prev_number[:-1]
        self.ids.input_box.text = prev_number

    # Getting the button value
    def button_value(self, number):
        prev_number = self.ids.input_box.text

        if "wrong equation" in prev_number:
            prev_number = ''

        if prev_number == '0':
            self.ids.input_box.text = ''
            self.ids.input_box.text = f"{number}"

        else:
            self.ids.input_box.text = f"{prev_number}{number}"

    # Getting the signs
    def sings(self, sing):
        prev_number = self.ids.input_box.text
        self.ids.input_box.text = f"{prev_number}{sing}"

    # Getting decimal value
    def dot(self):
        prev_number = self.ids.input_box.text
        num_list = re.split("\+|\*|-|/|%", prev_number)

        if ("+" in prev_number or "-" in prev_number or "*" in prev_number or "/" in prev_number or "%" in prev_number) and "." not in num_list[-1]:
            prev_number = f"{prev_number}."
            self.ids.input_box.text = prev_number

        elif '.' in prev_number:
            pass

        else:
            prev_number = f'{prev_number}.'
            self.ids.input_box.text = prev_number

    # Calculate the result
    def results(self):
        match self.tab_selected:
            case 0:
                self.calculate()
            case 1:
                self.calculate_mortage()
            case 2:
                self.calculate_tip()
    ### Evaluating the mathematical expression entered by the user in the input box and displays the result in the same input box. If an error occurs during an evaluation, it displays "Error" in the input box instead. ###    
    def calculate(self):
        prev_number = self.ids.input_box.text
        if(not prev_number): return
        try:
            result = eval(prev_number)
            self.ids.input_box.text = str(result)
        except:
            self.ids.input_box.text = "Error"
    ### Calculating Expected Monthly Mortgage Payment Function ###
    def calculate_mortage(self):
        def result():
            pricipal = self.mortage_values[0]
            down_payment = self.mortage_values[1]
            number_of_payments = int(self.mortage_values[3]) * 12
            monthly_interest_rate = self.mortage_values[2] / 12

            compound_factor = pow(1 + monthly_interest_rate, number_of_payments)
            monthly_emi = (
                (pricipal -down_payment) * monthly_interest_rate * compound_factor / (compound_factor - 1)
            )

            return round(monthly_emi, 2)

        mortage_input = self.ids.input_box.text
        try:
            if(self.tab_selected == 1 and len(self.mortage_values) < len(MORTAGE_PROMPTS) - 2):
                self.mortage_values.append(float(mortage_input))
                self.ids.input_box.text = ""
            elif(self.tab_selected == 1 and len(self.mortage_values) == len(MORTAGE_PROMPTS) - 2):
                self.mortage_values.append(float(mortage_input))
                self.ids.input_box.text = f"{result()}"
            else:
                self.change_tab(1)
        except:
            self.ids.input_box.text = "Error"

        self.ids.input_prompt.text = MORTAGE_PROMPTS[len(self.mortage_values)]
    ### Calculating suggested tip amount to leave based upon the user inputs ###
    def calculate_tip(self):
        def result():
            bill_total = self.tip_values[0]
            percentage = self.tip_values[1]
            tip_money = bill_total * percentage

            return round(tip_money, 2)

        tip_input = self.ids.input_box.text
        try:
            if(self.tab_selected == 2 and len(self.tip_values) < len(TIP_PROMPTS) - 2):
                self.tip_values.append(float(tip_input))
                self.ids.input_box.text = ""
            elif(self.tab_selected == 2 and len(self.tip_values) == len(TIP_PROMPTS) - 2):
                self.tip_values.append(float(tip_input))
                self.ids.input_box.text = f"{result()}"
            else:
                self.change_tab(2)
        except:
            self.ids.input_box.text = "Error"
        
        self.ids.input_prompt.text = TIP_PROMPTS[len(self.tip_values)]
       
    # Positive to negative
    def positive_negative(self):
        prev_number = self.ids.input_box.text
        if "-" in prev_number:
            self.ids.input_box.text = f"{prev_number.replace('-', '')}"
        else:
            self.ids.input_box.text = f"-{prev_number}"

### Changing the title of the application to DLAW ###
class CalculatorApp(App):
    def build(self):
        self.title = "DLAW"
        return CalculatorWidget()
### Executes script only if it is run directly ###
if __name__ == "__main__":
    CalculatorApp().run()
