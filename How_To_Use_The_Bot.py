

'''
=== GENERAL THINGS TO KNOW FOR USING THE PROGRAM === 

== Bot Controls == 

    IMPORTANT: Since Numpad is used, the key "numlock" must be active for the bot to work! 

    Numpad: Assign Buildings: Press the numpad, followed by a regular number from the number panel (i.e NOT the numpad). 
    For example. [Numpad 3] + 4 assigns 4 stables. 
        1 = Town Centers
        2 = Markets 
        3 = Castles 
        4 = Barracks 
        5 = Archery Ranges 
        6 = Stables
        7 = Siege Workshops 

    Numpad 0: Toggles the bot on/off. This is the only button that the keyboard responds to if the bot is running. 
    "+" - Cycles between windows
    "-" - Toggles force_control, i.e if the bot is allowed to forcibly take control over the game (briefly) if the bot has not been run for a while. 
    "*" - Toggles uppgrades, i.e if the bot is allowed to train upgrades.


    Tweaking specific data about the game (this list might not be complete): 
        * Unique unit: Assign in the MainScript when the object "unique-unit" is created. 
        * Set Warning time and force-run time: "Listening"-class. 
        * Add/Modify unit / upgrade: "Units_And_Upgrades"-class.  



== Setup ===

- The bot is currently hardcoded to only work on a screen witg A screen with dimensions: 2560x1080
- The AoE2 mod: "16655_Better readable Ressource Panel" (Included in this folder)

== HOTKEYS TO ASSIGN TO MAKE THE PROGRAM WORK ==  



Q-T, A-H   and J-L are used for selecting buildings: 

    SELECT ALL: 
    Q = Town Centers    W = Blacksmiths         E = Markets     R = Universities
    A = Barracks        S = Archery Ranges      D = Stables     F = Siege Workshops
    GO TO: 
    J = Lumber Camp     K = Mill                L = Mining Camp 

Other commands: 

    ACCORDING TO TESTING: When a control group is selected, the unit that is currently selected will de-select, EVEN if the control group is empty. Houses are not needed. 

    * In the Group Commands tab on hotkeys: Add a hotkey for B. Then make sure that this hotkey always has HOUSES. (This is important because it ensures that the user deselects any unit that is selected)
    * For VILLAGER hotkeys: Make sure that the "Cancel" button for buildings is removed from the villager. (Otherwise the bot will not work properly if a villager is selected when the run starts)


==== KNOWN BUGS ====

Here i add bugs that I have decided not to fix (either because it is not necessary, or necause it's too difficult)

- HAVING KEYBOARD INPUT DISABLED: Occationally when disabling the bot in the middle of a run, the keyboard input will continue to be disabled. 
In my experience, this can be toggled by pressing the numpad 0 key 2 times (to toggle it on an off again). 




    == CASES WHERE THE BOT CAN BEHAVE STRANGELY == 

    - The bot doesn't know which upgrades that the player's civilization doesn't have access to. As such, it will occasionally
    research upgrades which it doesn't have, causing it to press the wrong hotkeys. 
        * Example: It will try researching Husbandry as Cumans (which they dont have). This will cause the bot to press X, which
        selects all idle workers. However this is not a problem since the bot will press escape right before executing any
        further button presses. 


    == CASES WHERE THE BOT CAN FAIL TO RESEARCH AN UPGRADE == 
    * If the bot attempts to research an upgrade and fails for any reason (e.g below) it will believe that that upgrade has been researched, and will not research it again.  

    - MOST IMPORTANT: Avoid turning off the bot while the menu is red (i.e the bot is executing). Doing this might result in an upgrade not being researched.

    - SCREENSHOT-FUNCTION OVERWRITING DATA: 
        The screenshot function [SF] run will every few seconds and update the player's resources. This function will NOT run if the player has initiated the bot.
        HOWEVER, if the player initiates the bot WHILE the SF is running, the SF will continue to run. This COULD theoretically cause the bot to overwrite the resources 
        that the player has. 
            Example: The player has 510 food and trains 4 villagers -> 310 food left. The SF then reads the player resources, causing it to RESET to 530 in the middle of the loop, 
            making the bot believe it has more food than it actually has. 

        This is however unlikely to be a problem because: The entire SF takes about 2 seconds to run. The wood/food/gold resources are read first, so they should be read in less than 0.5 seconds.

    - ACCIDENTLY SELECTING UNITS: The Keyboard-disable has a flaw: While it moves your mouse on the screen and blocks the keyboard, it does NOT block you from selecting 
    units right in the middle of a loop IF YOU HAVE LEFT-CLICKED TO DRAW A SELECTION-RECTANGLE RIGHT WHEN THE BOT STARTS. In this case, when you drop your selection-square, 
    you will select any units in that rectangle, which will interrupt the bot's selection of buildings. 

    - HAVING TOO FEW PRODUCTION BULDINGS: If you only have 1 blacksmith and the bot trains many military units, It may attempt
    to train upgrades in the blacksmith that are not yet available. Then the bot will believe that those upgrades have been trained,
    and will not research them at all. 

    - RESEARCHING A NEW AGE: If a new age is being researched, the bot will check for the red "research"-line. If it detects
    this line, it will not register the new age. The BUG is that a new age is researched RIGHT BEFORE the bot-loop starts, 
    the bot won't see the red line because it doesn't appear the first few seconds. However, this scenario is VERY UNLIKELY,
    so i have decided to skip this. 

    - NOT CORRECT READING OF RESOURCES: The bot does not always correctly read the player's resources. If it reads more resources than
    the player actually has, it may try to research upgrades which it can't afford (in which case these upgrades will never be researched). 

    - OPENING CHAT: If the user opens a chat, the bot will type into the chat instead of researching upgrades. 

    - ACCIDENTLY SELECTING WRONG BUILDINGS UNITS: If the bot tries to research an upgrade that uses the hotkeys z/x/c/v, 
    and this upgrade is already researched, the bot will instead use the hotkeys that were mentioned. For example, it might 
    select all military units. Then, it might press for example "D", which will set the battle stance of the selected unit,
    instead of selecting all stables. This is however an unlikely problem and not important to deal with. 



''' 





