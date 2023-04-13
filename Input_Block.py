

from threading import Thread
import mouse
import time
import keyboard 
from pynput.keyboard import Key, Controller, Listener
from termcolor import cprint




'''

- Jag kunde inte hitta en officiel lista, så har experimenterat fram nedan. 
    * Kan läsa mer här: https://github.com/boppreh/keyboard#keyboard.block_key

# NUMPAD NUMBERS: For "keyboard.block_key()", e.g "keyboard.block_key(71)" tar bort 7
    * 70: Tar bort INGEN
    * 71: Tar bort 7
    * 72: Tar bort 8
    * 73: Tar bort 9 
    * 74: Tar bort INGEN 
    * 75: Tar bort 4
    * 76: Tar bort 5 
    * 77: Tar bort 6 
    * 78: Tar bort INGEN 
    * 79: Tar bort 1
    * 80: Tar bort 2 
    * 81: Tar bort 3 
    * 82: Tar bort 0 

'''


import random

class Input_Blocker(): # Källa som använts för klassen: https://stackoverflow.com/questions/65801957/python-block-keyboard-mouse-input

    blockActive = False  

    objectThatIsBeingTrained = "None" # Used in the window on the screen to display which unit is being created. 
    knightHasBeenTrained = False  # Checks if a gold knight has been trained. If it has, no scouts should be trained. (This is hard-coded, since most units don't have the depndancy where if 1 unit isn't available, train the other)

    def Randomized_Sleep(inputDelay): # Takes an input-delay, makes it anywhere between 30% longer or 30% shorter, and then sleeps for this new ampount.   

        randomFactor = random.uniform(0.7, 1.3)
        randomFactor = round(randomFactor, 1) 
        newDelay = inputDelay*randomFactor
        time.sleep(newDelay)

        

    def Execute_KeyPress(targetUnit_or_Upgrade, quantity):
        ''' 
        Tillägg: OM programmet behöver kunna trycka på flera knappar samtidigt, använd detta:    
        with keyboard.pressed(Key.shift):
            keyboard.press('a')
            keyboard.release('a')

        SEQUEBCE FOR BUILDING THINGS: 

        1. Press B -> B is the CONTROL GROUP for Houses (Houses are great for this purpose, since they don't have any building commands, so any 
            button pressed after, e.g Q for "select all town centers", will be registred)
        2. Press the Building Button.
        3. Press the Training button 1 time for each unit that is supposed to be trained (if it is an upgrade, the quantity should be 1 by default)


        ''' 



        if Input_Blocker.blockActive == False:  # If we have reached this point, it means we didn't return in the last paragraph, so we are training a unit. Then we must disable the user input. 
            input_blocker_Thread = Thread(target=Input_Blocker.Disable_User_Input) # Startar en ny tråd som disablar all input. 
            input_blocker_Thread.start()  

        cprint("Training " + str(quantity) + " " + targetUnit_or_Upgrade.name, "grey", "on_white")
        
        Input_Blocker.objectThatIsBeingTrained = targetUnit_or_Upgrade.name # Updates the variable "objectThatIsBeingTrained" so that it can be displayed on the sceeen. 


        buildingButton = targetUnit_or_Upgrade.buildingHotkey
        trainingButton = targetUnit_or_Upgrade.trainingHotkey
        sleepBetween_keyUp_keyDown = 0.1 # Experiment: about 30 button-presses can be done within 5 seconds, so about 6 presses per second. As such, having a factor of 0.1+0.1 [button-press + delay-between-press] is EASILY doable! 
        sleepBetween_key_press = 0.05
        initial_delay = 0.05 # initial delay sattes tidigare till 0.5, men det är fortfarande rätt lång delay mellan sekvenserna med 0.05, så den sattes till 0.05. 

        # INITIAL DELAY -> This is to simulate that it takes the player some time to swtich between training each unit(upgrade) (without this delay it looks less realistic)
        Input_Blocker.Randomized_Sleep(initial_delay)

        # Press [b] 
        keyboard.press("b")
        Input_Blocker.Randomized_Sleep(sleepBetween_keyUp_keyDown) # Replaces: time.sleep(sleepBetween_keyUp_keyDown) 
        keyboard.release("b")

        Input_Blocker.Randomized_Sleep(sleepBetween_key_press)

        #Press [building button]
        keyboard.press(buildingButton)
        Input_Blocker.Randomized_Sleep(sleepBetween_keyUp_keyDown)
        keyboard.release(buildingButton)

        Input_Blocker.Randomized_Sleep(sleepBetween_key_press)

        #Press [training button] one time for each unit that is to be trained
        for i in range(quantity):
            keyboard.press(trainingButton)
            Input_Blocker.Randomized_Sleep(sleepBetween_keyUp_keyDown)
            keyboard.release(trainingButton)

            Input_Blocker.Randomized_Sleep(sleepBetween_key_press)

        Input_Blocker.objectThatIsBeingTrained == "--" # Resets the object that is being trained. 

        '''
        ==== INFO om key-presses ====
        # Denna video användses: https://www.youtube.com/watch?v=DTnz8wA6wpw
        # Fler keys han hittas här: https://pythonhosted.org/pynput/keyboard.html#pynput.keyboard.Key
        '''


    def Disable_User_Input(): 
        ''' 
        FUNCTION DESCRIPTION: 
        - The function blocks user imput while Input_Blocker.blockActive is true. 
        - Input_Blocker.blockActive is set to false in any of these situations: 
            1. When the failsafe-time has passed. 
            2. When the main-loop reaches its end
            3. When the user presses numpad0 inside the listening script. 
        
        '''

        print("BLOCKING KEYBOARD") # 
        timestamp_Start = time.time() # FAILSAFE: Används för att kontrollera att programmet inte 
        FAIL_SAFE_TIME = 10
        block_all_up_to = 150   
        key_to_not_block = 82 # Numpad 0 ska inte blockas. Denna har index 82.  
        for i in range(block_all_up_to+1): # ❗ NOTE: for i in range(5) only prints 0-4 - Note it is up to FOUR, not five. That's why +1 is added. Then range(5) counts to 5.  
            keyboard.block_key(i)
            if (i == key_to_not_block):
                keyboard.unblock_key(i)

        Input_Blocker.blockActive = True
        while Input_Blocker.blockActive == True: 
            mouse.move(1050,900, absolute=True, duration=0) # Disables the mouse by constantly moving it to a specific point on the screen 
            timeSinceStart = time.time() - timestamp_Start 
            
            if (timeSinceStart > FAIL_SAFE_TIME): # FAILSAFE: Funktionen stänger sig själv efter X antal sekunder.  
                cprint("A certain amount of time passed. TRIGGERING FAILSAFE. Turning off Input Blocker", "yellow") 
                Input_Blocker.blockActive = False 

            # print("Keys are blocked. Time since start: " + str(timeSinceStart))

        print("UNBLOCKING KEYBOARD") 
        for i in range(block_all_up_to):
            if (i != key_to_not_block): # The check is required since the unblock-function will return error if it tries to unblock a key that isnt blocked. 
                keyboard.unblock_key(i)      

      
    # ============ OLD FUNCTION ============

    '''
    def Block_Keyboard_During_Time(input_Time = 4): # <<< ANVÄNDS INTE: Syftet med funktionen är bara att besiva att Input_block kan exevkera knapptryck trots att keyboard är disablat. 

        print("BLOCKING KEYBOARD")
        time.sleep(1)

        block_all_up_to = 150   
        key_to_not_block = 82 # Numpad 0 ska inte blockas. Denna har index 82.  

        for i in range(block_all_up_to+1): # ❗ NOTE: for i in range(5) only prints 0-4 - Note it is up to FOUR, not five. That's why +1 is added. Then range(5) counts to 5.  

            keyboard.block_key(i)
            
            if (i == 82):
                keyboard.unblock_key(i)

        time.sleep(input_Time)

        # KEY PRESS  -> PROVES THAT keyboard.press WORKS during this time.  
        #keyboard.press("q")
        #time.sleep(1)
        #keyboard.release("q")

        print("UNBLOCKING KEYBOARD")   # # ❗❗❗ NOTERING: Funtkionen får error om man försöker använda unblock-key på en key som inte blockats. 
        for i in range(block_all_up_to):
            if (i != 82): # The check is required since the unblock-function will return error if it tries to unblock a key that isnt blocked. 
                keyboard.unblock_key(i)        
 
    def PressButtonsEverySecond(): # ANVÄNDS INTE: Syftet med funktionen är bara att besiva att Input_block kan exevkera knapptryck trots att keyboard är disablat. 
        # VIKTIGT: Kör funktionen i en egen thread så att följande körs.
        cprint("pressing q", "yellow")
        keyboard.press("q")
        time.sleep(1)
        keyboard.release("q")

        cprint("pressing q", "yellow")
        keyboard.press("q")
        time.sleep(1)
        keyboard.release("q")

        cprint("pressing q", "yellow")
        keyboard.press("q")
        time.sleep(1)
        keyboard.release("q")

        x = 4



class Lyssnare(): # DEBUG: Används endast för debug i Input_block

    @staticmethod
    def OnKeyDown(key):
        keystring = str(key)

    def OnKeyUp(self, key):

        keyString = str(key) # Konverterar till sträng 

        keyString = keyString.replace("'", "") # Utan denna rad kommer sifrora returneras som " '5' " och inte "5", vilket i det fallet skapar problem med konverteringen.
        # <---- VIKTIG NOTERING: Ovanstående rad FUNGERAR INTE FÖR KNAPPEN (') , eftersom att detta tecken replacas. 

        cprint("USER PRESSED" + str(key), "cyan") # <-- Debug: Här kan man 
        
        # CHECK FOR SPECIFIC CHAR:  
        if keyString == "<96>": # Numpad 0
            cprint("THE KEYBOARD BLOCK WAS DISABLED", "yellow")
            Input_Blocker.blockActive = False
    
    '''

'''

=== GAMLA FUNKTIONER === 

listener = Lyssnare() # <--  Skapar listener 
lyssnare = Listener(on_press=listener.OnKeyDown, on_release=listener.OnKeyUp)
lyssnare.start()

input_blocker_Thread = Thread(target=Input_Blocker.Disable_User_Input)
input_blocker_Thread.start()

buttonPresserThread = Thread(target=Input_Blocker.Disable_User_Input)
buttonPresserThread.start()

=== NYA FUNKTIONER === 
inputBlock_thread = Thread(target=Input_Blocker.Block_Keyboard_During_Time, args=([4]))
inputBlock_thread.start()

buttonPresserThread = Thread(target=Input_Blocker.PressButtonsEverySecond)
buttonPresserThread.start()

'''





