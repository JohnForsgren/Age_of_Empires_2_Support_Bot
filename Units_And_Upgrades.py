

from termcolor import cprint # Webpage for Cprint: https://pypi.org/project/termcolor/





class Unit: # FÖRSLAG på en unit-klass, för att samla data i ett script 

    '''
    
    MAP OF WHERE UPGRADES ARE MANAGED WITHIN THE CODE 

    === General Functions === 
    - See the class "UNIT_Train_If_Applicable", which manages all of this. 

    === Object-specific (All of these must be in place for a specific unit to train) === 
    - Unit Class -> Contains all data for the nits. 
    - Unit Object Definition: 
        * The unit must be defined in the main loop, e.g through 'knight=Unit("knight")'
        * The unit must be recruited in the main loop through the function " UNIT_Train_If_Applicable(knight, listener.stables)"
        - 🔯 As far as i know, there are no other object-specific references to the unit.
            * <<< 🔯🔯The above text can easily be verified by simply searching on "archer" and see at how many places it appears.  

    - Upgrade Class -> Contains all data for the upgrades, EXCEPT which TYPE(s) of unit has to be present to train the upgrade. 
    - "UPGRADE_Requirements_Age_AlreadyResearched_EnoughUnits": 
        * Check the requirements for Age, AlreadyResearched and Enough units.
        * Also determined which TYPE OF UNIT is needed. 
    - Upgrade Object definition: Done after the main-loop-function is defined in the main script.  
    - Lägg in uniten i CalculateCurrentCost_PER_SECOND så att det ska räknas ut. 

    
    
    
    '''

    trainingTime_compensationFactor = 0.7 # Variable that takes into account that the bot is not always active, so the effective training time should be a bit shorter so that the bot queues units (rather than perfectly trying to queue 1 unnit per time)

    def __init__(self, nameF):
        self.name = nameF
        self.lastCreation = 0
        self.trainingTime = 0
        self.wood = 0 
        self.food = 0 
        self.gold = 0 
        self.stone = 0 # NOTE: No units cost stone; this definition is just used since stone is used for upgrades, and the resource-check-function (which runs both on units and upgrades) checks for stone. 
        self.age = 1

        self.unitType = "NOT DEFINED" # The type of unit. Used in the UnitCounter-class to keep track on how many units have been trained. 
        # NOTE: The buildingHotkey and trainingHotkey MUST be in lowercase; otherwise they are not registred in game. 
        self.buildingHotkey = "XXX" # Hotkey for selecting the buildings, e.g "Select all Town Centers" = q. 
        self.trainingHotkey = "XXX" # Hotkey for training the unit once the building is selected.  
        self.AssignUnitData()
        
        
    def AssignUnitData(self): 


        # ECONOMIC UNITS 
        if self.name == "villager":
            self.trainingTime = 25  
            self.food = 50 
            self.age = 1
            self.buildingHotkey = "q"  
            self.trainingHotkey = "q"


        elif self.name == "trade_chart":
            self.trainingTime = 51 
            self.wood = 100 
            self.gold = 50 
            self.age = 2
            self.buildingHotkey = "e"   
            self.trainingHotkey = "q"
            

        # CASTLE - PRIMARILY UNIQUE UNITS 
        elif self.name == "trebuchet": 
            self.trainingTime = 50 
            self.wood = 225
            self.gold = 225
            self.age = 4
            self.unitType = "siege_weapon"
            self.buildingHotkey = "g" 
            self.trainingHotkey = "w"


        elif self.name == "janissary":
            self.trainingTime = 17 
            self.food = 60 
            self.gold = 55 
            self.age = 3
            self.unitType = "archer"
            self.buildingHotkey = "g" 
            self.trainingHotkey = "q"


        elif self.name == "kipchak":
            self.trainingTime = 20 
            self.wood = 60 
            self.gold = 35 
            self.age = 3
            self.unitType = "cavalry_archer"
            self.buildingHotkey = "g" 
            self.trainingHotkey = "q"

        elif self.name == "cataphract":
            self.trainingTime = 20 
            self.wood = 60 
            self.gold = 35 
            self.age = 3
            self.unitType = "cavalry_archer"
            self.buildingHotkey = "g" 
            self.trainingHotkey = "q"
            

        elif self.name == "ballista_elephant":
            self.trainingTime = 25 
            self.food = 100 
            self.gold = 80
            self.age = 3
            self.unitType = "cavalry" # Balliste elephants can be counted as cavalry since they are affected by cav upgrades. 
            self.buildingHotkey = "g" 
            self.trainingHotkey = "q"

        elif self.name == "mameluke":
            self.trainingTime = 23
            self.food = 55
            self.gold = 85
            self.age = 3
            self.unitType = "cavalry"
            self.buildingHotkey = "g" 
            self.trainingHotkey = "q"

        elif self.name == "war_elephant":
            self.trainingTime = 25
            self.food = 170
            self.gold = 85
            self.age = 3
            self.unitType = "cavalry"
            self.buildingHotkey = "g" 
            self.trainingHotkey = "q"

        elif self.name == "mangudai":
            self.trainingTime = 26
            self.wood = 55
            self.gold = 65
            self.age = 3
            self.unitType = "cavalry_archer"
            self.buildingHotkey = "g" 
            self.trainingHotkey = "q"

        elif self.name == "genoese_crossbowman":
            self.trainingTime = 18
            self.wood = 45
            self.gold = 40
            self.age = 3
            self.unitType = "archer"
            self.buildingHotkey = "g" 
            self.trainingHotkey = "q"

        elif self.name == "gbeto":
            self.trainingTime = 17
            self.food = 50
            self.gold = 40
            self.age = 3
            self.unitType = "infantry"
            self.buildingHotkey = "g" 
            self.trainingHotkey = "q"

        elif self.name == "INSERT_UU_HERE":
            self.trainingTime = 0
            self.food = 0
            self.gold = 0
            self.age = 3
            self.unitType = "INSERT_UNIT_TYPE_HERE"
            self.buildingHotkey = "g" 
            self.trainingHotkey = "q"


        # BARRACKS 
        elif self.name == "militia":
            self.trainingTime = 21 
            self.food = 45 # Egentligen är detta 60 utan supplies, men OFTAST har man Supplies. I övrigt är det bättre att spendera för mycket än för lite, därav 45.  
            self.gold = 20
            self.age = 1
            self.unitType = "infantry"
            self.buildingHotkey = "a" 
            self.trainingHotkey = "q"

        # ARCHERY RANGE 
        elif self.name == "archer":
            self.trainingTime = 27
            self.wood = 25 
            self.gold = 45 
            self.age = 2
            self.unitType = "archer"
            self.buildingHotkey = "s" 
            self.trainingHotkey = "q"

        elif self.name == "cavalry_archer":
            self.trainingTime = 34 
            self.wood = 40 
            self.gold = 60 
            self.age = 2
            self.unitType = "cavalry_archer"
            self.buildingHotkey = "s" 
            self.trainingHotkey = "e"


        # STABLES 
        elif self.name == "knight":  
            self.trainingTime = 30 
            self.food = 60 
            self.gold = 75
            self.age = 3
            self.unitType = "cavalry"
            self.buildingHotkey = "d" 
            self.trainingHotkey = "w"

        elif self.name == "scout_cavalry":  
            self.trainingTime = 30 
            self.food = 80
            self.age = 2
            self.unitType = "cavalry"
            self.buildingHotkey = "d" 
            self.trainingHotkey = "q"

        # SIEGE WORKSHOP          
        elif self.name == "battering ram": 
            self.trainingTime = 36 
            self.wood = 160
            self.gold = 75
            self.age = 3
            self.unitType = "siege_weapon"
            self.buildingHotkey = "f" 
            self.trainingHotkey = "q"
        
        elif self.name == "mangonel": 
            self.trainingTime = 46 
            self.wood = 160
            self.gold = 135
            self.age = 3
            self.unitType = "siege_weapon"
            self.buildingHotkey = "f" 
            self.trainingHotkey = "w"

        elif self.name == "scorpion":
            self.trainingTime = 0 
            self.wood = 75
            self.gold = 75
            self.age = 3
            self.unitType = "siege_weapon"
            self.buildingHotkey = "f" 
            self.trainingHotkey = "e"


        #OTHER
        else: 
            cprint("ERROR - UNIT NAME NOT FOUND for unit " + self.name, "red") 


        self.trainingTime *= Unit.trainingTime_compensationFactor # Compensates for the fact that the bot is not always running, so it must queue units more often than their reqular training times. 
        self.trainingTime /= 1.7 # Compensates for the fact that the game speed is faster - See comment below. 
        '''
        OVANSTÅENDE är ett tillägg för training time: Om en villager har 25s training time är det värt att lägga in en buffer på ca 5 sekunder för att: 
            1. Kompensera för att botten inte alltid kommer kunna köa units perfekt (eftersom en annan loop kan vara aktiv)
            2. Göra botten mer realistisk (minska sannolikhet för att förlora rank)
        '''


class Upgrade:

    '''
    MAP OF WHERE UPGRADES ARE MANAGED WITHIN THE CODE 

        - Upgrade Class -> Contains all data for the upgrades, EXCEPT which TYPE(s) of unit has to be present to train the upgrade. 

        === EACH OBJECT MUST BE INCLUDED AT THESE PLACES ===
        1. Object defined in MainScipt  
            -> wood1 = Upgrade("wood1")
        2. Function "UPGRADE_Requirements_Age_AlreadyResearched_EnoughUnits" 
            -> if upgrade == "wood1" and (SCREENSHOT_DATA.villagersWood) > upgrade.unitsRequired: return True
        3. Object train-function called in main-script
            -> UPGRADE_Research_If_Applicable(wood1)
    
 
    '''

    # STATIC VARIABLES
    upgradesToCheck = ["melee_weapon", "infantry_armor", "cavalry_armor", "archer_weapon", "archer_armor", "food", "wood", "gold", "stone", "tc_chart"]  
    recentlyResearchedUpgrades = []
    time_while_upgradePath_is_disabled = 60

    '''
    THEORY ON STATIC VARIABLES: 
    QUESTION: Is it possible to have static class variables or methods in Python? What syntax is required to do this?
    ANSWER: Yes. The absence of the keyword "static" might be misleading, but any object initialised inside the class (just one indent inside the class, and not in the constructor) is static
    
    '''


    def __init__(self, nameF):
        self.name = nameF
        self.isReseached = False
        self.food = 0 
        self.wood = 0 
        self.gold = 0 
        self.stone = 0 
        self.age = 1
        self.unitsRequired = 0 # VIKTIGT: Denna variabel lagrar inte TYPEN av den unit som krävs. 
        self.buildingHotkey = "XXX" # The variable used to select the BUILDING for the upgrade. 
        self.trainingHotkey = "XXX" # The variable used to RESEARCH the upgrade. 
        self.AssignUpgradeData()
        self.SetAlreadyResearcedUpgrades() # Set upgrades that are usually researched when the bot begins, such as the first lumber and farming upgrades. 
        

    def SetAlreadyResearcedUpgrades(self): # Add upgrades here that are typically already researched when the bot starts. 

        if self.name == "wood1":
            self.isReseached = True
        if self.name == "loom":
            self.isReseached = True
        

    def AssignUpgradeData(self): 

        # Upgrade data can be found here: https://ageofempires.fandom.com/wiki/Technology_(Age_of_Empires_II)

        if self.name == "wood1":
            self.food = 100 
            self.wood = 50 
            self.age = 2
            self.unitsRequired = 0  # Hand Axe ska researchas direkt.
            self.buildingHotkey = "j" 
            self.trainingHotkey = "q" 
        elif self.name == "wood2":
            self.food = 150 
            self.wood = 100 
            self.age = 3
            self.unitsRequired = 25  
            self.buildingHotkey = "j" 
            self.trainingHotkey = "q" 
        elif self.name == "wood3":
            self.food = 150 
            self.wood = 100
            self.age = 4 
            self.unitsRequired = 20  
            self.buildingHotkey = "j" 
            self.trainingHotkey = "q" 

        elif self.name == "food1": 
            self.food = 75
            self.wood = 75
            self.age = 2 
            self.unitsRequired = 10
            self.buildingHotkey = "k" 
            self.trainingHotkey = "q" 
        elif self.name == "food2": 
            self.food = 125
            self.wood = 125 
            self.age = 3
            self.unitsRequired = 30
            self.buildingHotkey = "k" 
            self.trainingHotkey = "q" 
        elif self.name == "food3": 
            self.food = 250
            self.wood = 250
            self.age = 4
            self.unitsRequired = 40
            self.buildingHotkey = "k" 
            self.trainingHotkey = "q" 

        elif self.name == "gold1": 
            self.food = 100
            self.wood = 75
            self.age = 2 
            self.unitsRequired = 10
            self.buildingHotkey = "l" 
            self.trainingHotkey = "q" 
        elif self.name == "gold2": 
            self.food = 200
            self.wood = 150
            self.age = 3
            self.unitsRequired = 15
            self.buildingHotkey = "l" 
            self.trainingHotkey = "q" 

        elif self.name == "stone1": 
            self.food = 100
            self.wood = 75
            self.age = 2
            self.unitsRequired = 10
            self.buildingHotkey = "l" 
            self.trainingHotkey = "w" 
        elif self.name == "stone2": 
            self.food = 200
            self.wood = 150
            self.age = 3
            self.unitsRequired = 12
            self.buildingHotkey = "l" 
            self.trainingHotkey = "w" 

        elif self.name == "tc_chart1":  # WHEELBARROW 
            self.food = 175
            self.wood = 50
            self.age = 2
            self.unitsRequired = 30 # NOTE: This includes BOTH Farmers and Lumberjacks 
            self.buildingHotkey = "q" 
            self.trainingHotkey = "s" 
        elif self.name == "tc_chart2": # HAND CHART  
            self.food = 300
            self.wood = 200
            self.age = 3
            self.unitsRequired = 50
            self.buildingHotkey = "q" 
            self.trainingHotkey = "s" 

        elif self.name == "caravan": 
            self.food = 200
            self.wood = 150
            self.age = 3
            self.unitsRequired = 12
            self.buildingHotkey = "e" 
            self.trainingHotkey = "w" 

        elif self.name == "loom":  
            self.gold = 50
            self.age = 3  # NOTE: Loom is classed as a castle-age upgrade since the bot should not train it before that. If needed before castle age, the user can get it easily. 
            self.unitsRequired = 0 # No units are needed for loom . 
            self.buildingHotkey = "q" 
            self.trainingHotkey = "a" 

        # === BLACKSMITH UPGRADES ===
        elif self.name == "melee_weapon1": 
            self.food = 150
            self.gold = 0
            self.age = 2 
            self.unitsRequired = 10 # Includes COMBINED infantry and cavalry. 
            self.buildingHotkey = "w" 
            self.trainingHotkey = "q" 
        elif self.name == "melee_weapon2": 
            self.food = 220
            self.gold = 120 
            self.age = 3
            self.unitsRequired = 10 
            self.buildingHotkey = "w" 
            self.trainingHotkey = "q" 
        elif self.name == "melee_weapon3":
            self.food = 275
            self.gold = 225
            self.age = 4
            self.unitsRequired = 10
            self.buildingHotkey = "w" 
            self.trainingHotkey = "q" 

        elif self.name == "infantry_armor1": 
            self.food = 100
            self.gold = 0 
            self.age = 2
            self.unitsRequired = 5
            self.buildingHotkey = "w" 
            self.trainingHotkey = "w" 
        elif self.name == "infantry_armor2": 
            self.food = 200
            self.gold = 100
            self.age = 3
            self.unitsRequired = 5
            self.buildingHotkey = "w" 
            self.trainingHotkey = "w" 
        elif self.name == "infantry_armor3": 
            self.food = 300
            self.gold = 150
            self.age = 4
            self.unitsRequired = 20
            self.buildingHotkey = "w" 
            self.trainingHotkey = "w" 

        elif self.name == "cavalry_armor1": 
            self.food = 150
            self.gold = 0
            self.age = 2 
            self.unitsRequired = 5
            self.buildingHotkey = "w" 
            self.trainingHotkey = "e" 
        elif self.name == "cavalry_armor2": 
            self.food = 250
            self.gold = 150
            self.age = 3
            self.unitsRequired = 10
            self.buildingHotkey = "w" 
            self.trainingHotkey = "e" 
        elif self.name == "cavalry_armor3":
            self.food = 350
            self.gold = 200
            self.age = 4
            self.unitsRequired = 15
            self.buildingHotkey = "w" 
            self.trainingHotkey = "e" 

        elif self.name == "archer_weapon1": 
            self.food = 100
            self.gold = 50
            self.age = 2
            self.unitsRequired = 5 # NOTE: APPLIES BOTH TO ARCHERS AND CAV ARCHERS 
            self.buildingHotkey = "w" 
            self.trainingHotkey = "a" 
        elif self.name == "archer_weapon2": 
            self.food = 200
            self.gold = 100
            self.age = 3
            self.unitsRequired = 10 
            self.buildingHotkey = "w" 
            self.trainingHotkey = "a" 
        elif self.name == "archer_weapon3":
            self.food = 300
            self.gold = 200
            self.age = 4
            self.unitsRequired = 15 
            self.buildingHotkey = "w" 
            self.trainingHotkey = "a" 

        elif self.name == "archer_armor1": # NOTE: APPLIES BOTH TO ARCHERS AND CAV ARCHERS 
            self.food = 100
            self.gold = 0 
            self.age = 2
            self.unitsRequired = 5
            self.buildingHotkey = "w" 
            self.trainingHotkey = "s" 
        elif self.name == "archer_armor2": 
            self.food = 150
            self.gold = 150
            self.age = 3
            self.unitsRequired = 10
            self.buildingHotkey = "w" 
            self.trainingHotkey = "s" 
        elif self.name == "archer_armor3":
            self.food = 250
            self.gold = 250
            self.age = 4
            self.unitsRequired = 15
            self.buildingHotkey = "w" 
            self.trainingHotkey = "s" 

        
        # == ARCHERY RANGE AND STABLE UPGRADES ==
        elif self.name == "thumb_ring": 
            self.food = 300
            self.wood = 250
            self.age = 3
            self.unitsRequired = 30 # Thumb ring is expensive, so the requirement should be high. 
            self.buildingHotkey = "s" 
            self.trainingHotkey = "z" 
        elif self.name == "parthian_tactics": 
            self.food = 200
            self.gold = 250
            self.age = 4
            self.unitsRequired = 5 # Parthian tactics is relatively cheap in Imperial age, so 5 cav archers is enough. 
            self.buildingHotkey = "s" 
            self.trainingHotkey = "c" 
        elif self.name == "ballistics": 
            self.wood = 300
            self.gold = 175
            self.age = 3
            self.unitsRequired = 25 # Ballistics need a high unit requirement since the player may not build a university until late in castle age.
            self.buildingHotkey = "r" 
            self.trainingHotkey = "r"   
        elif self.name == "chemistry": 
            self.food = 300
            self.gold = 200
            self.age = 4
            self.unitsRequired = 40
            self.buildingHotkey = "r" 
            self.trainingHotkey = "t" 
        
        elif self.name == "bloodlines": 
            self.food = 150
            self.gold = 100
            self.age = 2
            self.unitsRequired = 10 # NOTE: Applies to both Cavalry and Cavalry Archers 
            self.buildingHotkey = "d" 
            self.trainingHotkey = "z" 
        elif self.name == "husbandry": 
            self.food = 150
            self.age = 3
            self.unitsRequired = 5 
            self.buildingHotkey = "d" 
            self.trainingHotkey = "x" 


        # CASTLE UPGRADES: 
        

        elif self.name == "conscription": 
            self.food = 150
            self.gold = 150
            self.age = 4
            self.unitsRequired = 0 # Conscription has no unit requirements. 
            self.buildingHotkey = "g" 
            self.trainingHotkey = "c" 

        # OTHER UPGRADES: 
        elif self.name == "imperial_age": 
            self.food = 1000
            self.gold = 800
            self.age = 3
            self.unitsRequired = 80  # Imperial age should require something like 80 villagers. 
            self.buildingHotkey = "q" 
            self.trainingHotkey = "z" 




        else:
            cprint("BUG - THE FOLLOWING UPGRADE WAS NOT FOUND: " + self.name, "red")


        '''
        OTHER UPGRADES:  
        * Crossbowman, Arbalester, Cavalier and Paladin upgrades are NOT worth adding -> User can train these when needed.
        
        '''




