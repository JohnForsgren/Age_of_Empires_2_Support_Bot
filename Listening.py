"""
Listens to user input
"""

from pynput.keyboard import Key, Controller, Listener
from termcolor import cprint
import time

from Input_Block import Input_Blocker


class ListenerClass:
    """ Listens to data input """

    def __init__(self):

        self.town_centers = 0
        self.castles = 0
        self.siege_workshops = 0
        self.barracks = 0
        self.archery_ranges = 0
        self.stables = 0
        self.markets = 0

        self.botActive = False # This variable only represents if the bot is CURRENTLY RUNNING; it does NOT necessarily mean that the USER has pressed the button that starts the bot. 
        self.researchUpgrades = True 
        self.force_take_control = False; # Determines wheter the bot is allowed to forcibly take control. 
        self.prev_input = 0
        self.windowToDisplay = 1 # Variable that determines which window to display to the user [used in the changeText()-function in tkinter]

        # Variables managing the ITERATION  
        self.TIMESTAMP_LastIteration = time.time() # Is assigned time.time() in order to not have the first iteration happen at time "14000k". 
        self.time_LEFT_UNTIL_NEXT_ITERATION = 0
        self.timePerIteration = 5  # This used to be used for the time between each automatic iteration. But now, the program has changed to run itself. 

        self.warning1_time = 15 # Time until the first warning: Window changes to yellow color. Indicates that the user is recomended to run the bot. 
        self.warning2_time = 30 # Time until the second warning: Window changes to red color. Indicates that the bot will soon take over. 
        self.force_run_time = 35 # Time until the bot takes over the controls forcibly (IF the variable for forcible-control is set to true).

        ''' 
        === WHAT TIME PER ITERATION IS IDEAL? === 

        PERSPECTIVE 1: Lower than 14 seconds 
        - GIVEN that the training time i villagers is 25/1.7 = 14.7, the time per iteration should ideally NOT be any higher than 12-14 seconds, 
        considering that the screenshot-time takes 2-3 seconds. So if the time per iteration is higher than 14, the bot will NOT be able to queue villagers properly!


        PERSPECTIVE 2: Higher than 14 seconds
        - Because the bot interrupts the user, having a long delay is better. The problem described in perspective 1 can be dealt with by simply adding more buildings
        (e.g if the player has 2 TC:s and a loop time of 30 seconds, he can simply assign that he has 4 TC:s to the bot)

        PERSPECTIVE 3: 10 seconds or lower 
        - If the bot is programmed to not disable user input unless it is executing button presses, having a delay of 10 seconds or lower could work. The advantages of this is that: 
            * The bot will be able to more accurately queue units from the buildings (compared to a bot with a 30 second delay per iteration) 
            * WIth a more accurate queue system, it will be easier to calculate the exact amount of units needed. 

        
        '''


        # DEBUG 
        self.DEBUG_timeStamp_Start = time.time() # # Logs the time when the program started, allowing the user to see how long the bot has run. 
        self.DEBUG_total_running_time = 0 # Holds the current running time of the bot. 


    def UpdateWindowMode(self): # Updates the window mode. This changes the text on the window shown to the user.  
        self.windowToDisplay += 1

        if (self.windowToDisplay > 5):
            self.windowToDisplay = 1



    def ReturnBaseData(self): # Returns a long string with all base data. Only returns the variables that have a value over 0. 
        sträng = "\n"
        if (self.town_centers > 0):
            sträng += "town_centers: "    + str(self.town_centers) + "\n"
        if (self.markets > 0):
            sträng += "markets: "        + str(self.markets) + "\n"
        if (self.castles > 0):
            sträng += "castles: "        + str(self.castles) + "\n"
        if (self.barracks > 0):
            sträng += "barracks: "       + str(self.barracks) + "\n"
        if (self.archery_ranges > 0):
            sträng += "archery_ranges: "  + str(self.archery_ranges) + "\n"
        if (self.stables > 0):
            sträng += "stables: "        + str(self.stables) + "\n"
        if (self.siege_workshops > 0):
            sträng += "siege_workshops: " + str(self.siege_workshops) + "\n"
        return sträng


    def PrintVariables(self):
        
        print(self.ReturnBaseData())

    

    def OnKeyUp(self, key):
        '''
        LIST: All numbers are on the numpad. They assign amount for each of the buildings. The program will then aim to have constant production from these buildings.  
        1 = Town Centers
        2 = Markets
        3 = Castles 
        4 = Barracks 
        5 = Archery Ranges 
        6 = Stables 
        7 = Siege Worshops 
        
        * = Toggle upgrades on/off 
        + = Change the window to display.  

        = Endast 1 siffra behövs här; funktionen kommer aldrig behöva använda mer än 9 av någon byggnad (Om man mot förmodan har ekonomi 
        för fler än 9 av samma byggnad är det bättre att sprida produktionen över 2 eller fler olika byggnader).  

        '''

        keyString = str(key) # Konverterar till sträng 

        keyString = keyString.replace("'", "") # Utan denna rad kommer sifrora returneras som " '5' " och inte "5", vilket i det fallet skapar problem med konverteringen.
        # <---- VIKTIG NOTERING: Ovanstående rad FUNGERAR INTE FÖR KNAPPEN (') , eftersom att detta tecken replacas. 

        #cprint("USER PRESSED" + str(key), "cyan") # <-- Debug 
        
        # CHECK FOR SPECIFIC CHAR:  
        if keyString == "<96>": # Numpad 0
            self.botActive = not self.botActive # Toggles the variable botActive. 
            cprint("botactive is set to: " + str(self.botActive), "yellow")
            Input_Blocker.blockActive = False # Removes the blocking of user input. This is automatically set to true whenever the funciton the trains an unit/upgrade is run.  

            cprint("Numpad 0 pressed. Disables any active Input_Blocks", "cyan")
            cprint("Toggle bot. The new value is" + str(self.botActive), "cyan")

        if keyString == "+":
            cprint("UPDATES WINDOW", "cyan")
            self.UpdateWindowMode()
        if keyString == "*":
            self.researchUpgrades = not self.researchUpgrades
            cprint("TOGGLES UPGRADES. The new value is" + str(self.botActive) , "cyan")
        if keyString == "-":
            self.force_take_control = not self.force_take_control
            cprint("TOGGLES force_take_control. The new value is" + str(self.force_take_control) , "cyan")
            
            

        # === USER ASSIGNING AMOUNTS OF BUILDINGS ===
        if self.prev_input == "<97>" and self.CanConvertToInt(keyString): # Numpad 1
            self.town_centers = int(keyString)
        elif self.prev_input == "<98>" and self.CanConvertToInt(keyString): # Numpad 2 
            self.markets = int(keyString)
        elif self.prev_input == "<99>" and self.CanConvertToInt(keyString): # Numpad 3 
            self.castles = int(keyString)
        elif self.prev_input == "<100>" and self.CanConvertToInt(keyString): # Numpad 4 
            self.barracks = int(keyString)
        elif self.prev_input == "<101>" and self.CanConvertToInt(keyString): # Numpad 5 
            self.archery_ranges = int(keyString)
        elif self.prev_input == "<102>" and self.CanConvertToInt(keyString): # Numpad 6    
            self.stables = int(keyString)
        elif self.prev_input == "<103>" and self.CanConvertToInt(keyString): # Numpad 6    
            
            self.siege_workshops = int(keyString)

        self.prev_input = keyString # Lagrar värdet för nästa iteration  

        if key == Key.enter:
            self.PrintVariables() 
    print("START")

    @staticmethod
    def CanConvertToInt(inputF):
        if (inputF.isnumeric()):
            return True
    
    @staticmethod
    def OnKeyDown(key):
        keystring = str(key)


        








