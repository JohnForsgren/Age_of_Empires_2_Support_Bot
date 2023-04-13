# === PYTHON IMPORTS ===
import time
from threading import Timer, Thread
from pynput.keyboard import Key, Controller, Listener
from termcolor import cprint


# === OWN IMPORTS === 
from Read_Screenshot_Data import Screenshot_Data
from Listening import ListenerClass  # Funktionen ListenerClass körs genom variabeln "listener" nedan. 
from Variables import * # Funktionen körs direkt genom att bara skriva "Tid.[variabelnamn]"
from Units_And_Upgrades import Unit, Upgrade
from Input_Block import Input_Blocker


# === GAME-SPECIFIC-VARIABLES === 
UNIQUE_UNIT_NAME = "mangudai" # <-- ASSIGN at the start of the game 
#  Denna variabel kan bytas ut till andra unique units i fliken nedan:  0
''' OTHER UNIQUE UNITS:  ballista_elephant  genoese_crossbowman  kipchak  mameluke      mangudai         war_elephant   gbeto      '''



# == DEBUG === 
logger = logging.getLogger('MainScript')  # Definierar en logger som vet att vi är i MainScript

# ==== KOD FÖR ATT EXEKVERA KNAPPTRYCK ==== 1363000


keyboard = Controller() 

def Execute_KeyPress_For_UNIT_or_UPGRADE(targetUnit, quantity=1):

    '''
    EXPLAINATION: The whole function that executes key press was moved to the Input_blocker, since the input blocker would
    otherwise block python's own simulations. 
    '''

    Input_Blocker.Execute_KeyPress(targetUnit, quantity) 

def UNIT_Train_If_Applicable(targetUnit, quantity):
    '''
    === MAP FOR TRAINING A UNIT ===  
    - The function checks the following parameters in the following orders. 
    - If any parameter is false, the function terminates and returns "False" and does nothing. 
    UNIT: 
        * (R) 0. CHECKS: 1. Bot is Active? 2. User Population Cap? 3. User has enough production buildings? -> These are checked directly in the main-loop. 
        * (R) 1. CHECK: LAST CREATION TIME -> If the unit has not been trained recently (depending on its production time and the bot's queue-overlap); train the unit.  
        * (R) 2. CHECK: ENOUGH RESOURCES?  -> Done through the function "UNIT_AND_UPGRADE_RESOURCE_Requirement"
        * ACTION: UNIT IS TRAINED:
            * (R) Trivial: The unit Type [in Variables --> UnitCounter --> CountUnitTrain] is incremented by 1. 
            * (R) The lastCreation-variable (time) is updated. 
            * (R) A thread for the function "Execute_KeyPress_For_UNIT_or_UPGRADE" is executed. 
    '''


    if listener.botActive == False: # This line immediately terminates the function if the user has switched-off the bot in the middle of a loop.  
        return

    if quantity == 0: # Important so that the function doesn't make any unecessary key presses. This function is often run with quantity 0, since it is run for all buildings, even those with quantity 0. 
        logger.info("Training 0 " + targetUnit.name)
        return

    # === CHECK: AGE? === 0BQQQQBQZBQQQQ0
    if SCREENSHOT_DATA.age < targetUnit.age:
        cprint("User did not have the sufficient age to train unit: " + targetUnit.name, "yellow")
        logger.info("User did not have the sufficient age to train unit: " + targetUnit.name)
        return False

    # === CHECK: CREATION TIME === 
    if time.time() - targetUnit.lastCreation < targetUnit.trainingTime: 
        logger.info(targetUnit.name + " was not trained because it had been recently trained.")
        return

    # === CHECK: ENOUGH RESOURCES? === 
    if (UNIT_AND_UPGRADE_RESOURCE_Requirement(targetUnit, quantity)):

        targetUnit.lastCreation = time.time()
        unitCounter.CountUnitTrain(targetUnit.unitType, quantity) # Counts that the unit has been trained. 


        # == Initiates the Thread ==
        thread = Thread(target=Execute_KeyPress_For_UNIT_or_UPGRADE, args=([targetUnit, quantity])) # Notera att en tråd INTE startar om man har paranteser "Brekfast()"; skriv BARA funktionen "Brekfast"
        thread.start() # Startar tråden
        thread.join() # Väntar tills tråden är klar.  

        


def UPGRADE_Research_If_Applicable(upgrade):   

    '''
     === MAP FOR RESEARCHING AN UPGRADE === 0

        1. CHECK: ALREADY BOUGHT? - Has the upgrade already been bought? 
        2. CHECK: AGE - Is the Appropriate age unlocked? [This is done by if-statements in between the upgrades, that return the function if false]
        3. CHECK: ENOUGH UNITS? - Does the player have enough units to train the upgrade? 
        4. CHECK: ENOUGH RESOURCES?  -> Done through the function "UNIT_AND_UPGRADE_RESOURCE_Requirement" (Same as for Units)
        5. CHECK: LOWER-TIER UPGRADE NOT RESEARCHED RECENTLY? -> E.g in case melee weapon 1 in the blacksmith has been researched recentlym we can't research melee weapon 2. 
        6. ACTION: UPGRADE IS RESEARCHED: 
            * Upgrade is added to list of researched upgrades. 
            * A thread for the function "Execute_KeyPress_For_UNIT_or_UPGRADE" is executed. 

            

    '''

    if listener.botActive == False: # This line immediately terminates the function if the user has switched-off the bot in the middle of a loop.  
        return

    # ===== CHECKS: (1). ALREADY BOUGHT? (2). AGE? (3). ENOUGH UNITS? ===== 
    if UPGRADE_Requirements_Age_AlreadyResearched_EnoughUnits(upgrade) == False:
        return
    

    # ===== CHECK: (4). ENOUGH RESOURCES? ===== 
    if UNIT_AND_UPGRADE_RESOURCE_Requirement(upgrade) == False: 
        return

    # ==== CHECK (5). LOWER-TIER UPGRADE NOT RESEARCHED RECENTLY? ===== 
    if CheckRecentlyResearchedUpgrades(upgrade) == False: 
        return

    
    # ===== ACTION: UPGRADE IS RESEARCHED: ===== 
    upgrade.isReseached = True # (R) Add upgrade to list of researched upgrades.

    # ==== SPECIFIC VARIABLES TO UPDATE ==== 
    if (upgrade.name == "conscription"): # Reduce unique unit's creation time if conscription is researched. 
        UpdateUnitData("conscription") 


    # cprint("RESEARCING UPGRADE " + upgrade.name, "yellow", "on_blue") 
    # = Initiates the Thread =
    thread = Thread(target=Execute_KeyPress_For_UNIT_or_UPGRADE, args=([upgrade])) # Notera att en tråd INTE startar om man har paranteser "Brekfast()"; skriv BARA funktionen "Brekfast"
    thread.start() # Startar tråden
    thread.join() # Väntar tills tråden är klar.  



def UPGRADE_Requirements_Age_AlreadyResearched_EnoughUnits(upgrade): # Checks if the user has sufficient upgrades, if he has, the resources are drained and the function RETURNS TRUE The function does NOT trigger the function that actually trains the upgrade. 

    '''
    OVERVIEW: The function checks for: 

    - Already-researched requirement: Checks in the beginning. 
    - Unit requirement: Most if-statements checks if the player has enough units for the upgrade
    - Age requirement: The upgrades are placed under an if-statement referring to their age. For example "if SCREENSHOT_DATA.age < 4 -> Return False"
        
    
    '''

    # === CHECK: ALREADY RESEARCHED? ===  
    if upgrade.isReseached == True:
        #cprint("The following upgrade was not researched because it had already been researched: " + upgrade.name, "yellow")
        return False

    # === CHECK: AGE? === 
    if SCREENSHOT_DATA.age < upgrade.age: 
        #cprint("User did not have the sufficient age to research upgrade: " + upgrade.name, "yellow")
        return False

    
    # === CHECK: UNIT REQUIREMENT MET? ===  
    _______INSERT_VARIABLE_____ = 0  # Dummy Variable -> remove  
        

    if upgrade.name == "wood1" and SCREENSHOT_DATA.villagersWood >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "wood2" and SCREENSHOT_DATA.villagersWood >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "wood3" and SCREENSHOT_DATA.villagersWood >= upgrade.unitsRequired:
        return True

    elif upgrade.name == "food1" and SCREENSHOT_DATA.villagersFood >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "food2" and SCREENSHOT_DATA.villagersFood >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "food3" and SCREENSHOT_DATA.villagersFood >= upgrade.unitsRequired:
        return True

    elif upgrade.name == "gold1" and SCREENSHOT_DATA.villagersGold >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "gold2" and SCREENSHOT_DATA.villagersGold >= upgrade.unitsRequired:
        return True

    elif upgrade.name == "stone1" and SCREENSHOT_DATA.villagersStone >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "stone2" and SCREENSHOT_DATA.villagersStone >= upgrade.unitsRequired:
        return True

    elif upgrade.name == "tc_chart1" and (SCREENSHOT_DATA.villagersWood + SCREENSHOT_DATA.villagersFood) >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "tc_chart2" and (SCREENSHOT_DATA.villagersWood + SCREENSHOT_DATA.villagersFood) >= upgrade.unitsRequired:
        return True

    elif upgrade.name == "caravan" and unitCounter.trade_chart > upgrade.unitsRequired:
        return True

    elif upgrade.name == "loom": # Loom has no requirements (Besides being in castle age)
        return True

    # === BLACKSMITH UPGRADES === 
    elif upgrade.name == "melee_weapon1" and (unitCounter.infantry + unitCounter.cavalry) >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "melee_weapon2" and (unitCounter.infantry + unitCounter.cavalry) >= upgrade.unitsRequired:
        return True 
    elif upgrade.name == "melee_weapon3" and (unitCounter.infantry + unitCounter.cavalry) >= upgrade.unitsRequired:
        return True 

    elif upgrade.name == "infantry_armor1" and unitCounter.infantry >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "infantry_armor2" and unitCounter.infantry >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "infantry_armor3" and unitCounter.infantry >= upgrade.unitsRequired:
        return True

    elif upgrade.name == "cavalry_armor1" and unitCounter.cavalry >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "cavalry_armor2" and unitCounter.cavalry >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "cavalry_armor3" and unitCounter.cavalry >= upgrade.unitsRequired:
        return True

    elif upgrade.name == "archer_weapon1" and (unitCounter.archer + unitCounter.cavalry_Archer) >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "archer_weapon2" and (unitCounter.archer + unitCounter.cavalry_Archer) >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "archer_weapon3" and (unitCounter.archer + unitCounter.cavalry_Archer) >= upgrade.unitsRequired:
        return True

    elif upgrade.name == "archer_armor1" and (unitCounter.archer + unitCounter.cavalry_Archer) >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "archer_armor2" and (unitCounter.archer + unitCounter.cavalry_Archer) >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "archer_armor3" and (unitCounter.archer + unitCounter.cavalry_Archer) >= upgrade.unitsRequired:
        return True


    # == ARCHERY RANGE AND STABLE UPGRADES ==
    elif upgrade.name == "thumb_ring" and (unitCounter.archer + unitCounter.cavalry_Archer) >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "parthian_tactics" and (unitCounter.cavalry_Archer) >= upgrade.unitsRequired:
        return True
    
    elif upgrade.name == "ballistics" and (unitCounter.archer + unitCounter.cavalry_Archer) >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "chemistry" and (unitCounter.archer + unitCounter.cavalry_Archer) >= upgrade.unitsRequired:
        return True

    elif upgrade.name == "bloodlines" and (unitCounter.cavalry_Archer + unitCounter.cavalry) >= upgrade.unitsRequired:
        return True
    elif upgrade.name == "husbandry" and (unitCounter.cavalry_Archer + unitCounter.cavalry) >= upgrade.unitsRequired:
        return True

    # 🔯🔯🔯 MODELLEN FÖR UPPGRADERINGEN SKRIVS NEDAN 🔯🔯🔯
    elif upgrade.name == "INSERT_UPGRADE_HERE" and _______INSERT_VARIABLE_____ >= upgrade.unitsRequired:
        return True

    elif upgrade.name == "imperial_age" and SCREENSHOT_DATA.totalVillagers >= upgrade.unitsRequired:
        return True

    # === UPGRADES FROM CASTLE (Not to be confused with Castle Age) ===
    elif upgrade.name == "conscription":  # Conscription has no unit requirements  
        return True 

    else:
        return False
         
    



def UNIT_AND_UPGRADE_RESOURCE_Requirement(target, quantity=1): # Checks if the user has sufficient upgrades, if he has, the resources are drained and the function RETURNS TRUE The function does NOT trigger the function that actually trains the upgrade. 


    # Quantity = 1 by default, since all upgrades will run the function without a quantity (only units specify quantity). 

    # Booleans checking that the user has enough resources. 
    remainingFood = SCREENSHOT_DATA.food - target.food * quantity 
    remainingWood = SCREENSHOT_DATA.wood - target.wood * quantity  
    remainingGold = SCREENSHOT_DATA.gold - target.gold * quantity
    remainingStone = SCREENSHOT_DATA.stone - target.stone * quantity


    if remainingFood < 0: 
        #cprint("There was not enough FOOD to train " + str(quantity) + " " + str(target.name), "yellow")  
        logger.info("There was not enough FOOD to train " + str(quantity) + " " + str(target.name))
        return False
    if remainingWood < 0: 
        logger.info(f"There was not enough WOOD to train {quantity} {target.name}. Have: {SCREENSHOT_DATA.wood}, Need: {target.food*quantity}")
        return False
    if remainingGold < 0: 
        #cprint("There was not enough GOLD to train " + str(quantity) + " " + str(target.name), "yellow")
        logger.info("There was not enough GOLD to train " + str(quantity) + " " + str(target.name))
        return False
    if remainingStone < 0: 
        #cprint("There was not enough STONE to train " + str(quantity) + " " + str(target.name), "yellow")
        return False


    # === If not returned false: Drain the resources from the player here === 
    SCREENSHOT_DATA.food = remainingFood
    SCREENSHOT_DATA.wood = remainingWood
    SCREENSHOT_DATA.gold = remainingGold
    SCREENSHOT_DATA.stone = remainingStone

    return True
    '''
    RESONEMANG: Ska man räkna på total kostnad för alla UNITS, eller bara kostnaden för EN unit? 
    SVAR: ALLA UNITS:  
        * Det är viktigt att programmet BARA köper uniten om man HAR RÅD MED ALLA UNITS som ska köpas. 
    * Argument för att räkna med alla units: 
        * Funktionen som räknar antalet units man köpt fungerar inte om programmet tillåter att man köper units som man inte har råd med. 
        * Det är ett stort problem att programmet inte kan prioritera mellan vilka units man ska ha.  
        * Det är inte ett stort problem att botten tror att den inte har råd med units, eftersom man oftast bara kommer ha ca 4-5 stall (inte 10). 
    
    '''



def UpdateUnitData(inputReason = ""):  # Updates unit and upgrade data based on specific situations (e.g persian archers costing wood, or Huskarls trained from barracks instead of castles.)


    # === UPGRADES: IF THE FUNCTION IS RUN WITH SPECIFIC PARAMETERS ===
    if inputReason == "conscription" : # If conscription is researched: Count that the Unique unit can be trained more often. 
        uniqueUnit.trainingTime = uniqueUnit.trainingTime / 1.33

    '''
    Saker att lägga in: 
    * Elite Genoese Crossbowman: Training time 18s -> 14s. 


    '''
    
    


    # === FOR WHEN THE FUNCTION IS RUN AT THE START === 
    if uniqueUnit.name == "janissary":

        # archer = cavalry_archer # <<<<< ANVÄND COPY HÄR ISTÄLLET:  https://docs.python.org/3/library/copy.html 
        pass

    if uniqueUnit.name == "war_elephant":  # SUGGESTION: Detect specific civilizations by assigning which unique unit is used. 
        archer.wood = 60 # <<<< NOTE: 
        archer.gold = 0


def TrainUnits(): # 

    UNIT_Train_If_Applicable(uniqueUnit, listener.castles)   

    UNIT_Train_If_Applicable(militia, listener.barracks)

    UNIT_Train_If_Applicable(knight, listener.stables)
    if SCREENSHOT_DATA.age < 3 or (SCREENSHOT_DATA.food > 1000): # If the castle age is not reached, or if we are floating lots of food, we will try to make scouts. 
        UNIT_Train_If_Applicable(scout_cavalry, listener.stables) 
    else:
        #cprint("Scout cavalry was not trained since we could afford Knights instead - Not entirely sure if this is true", "yellow")
        pass 

    UNIT_Train_If_Applicable(archer, listener.archery_ranges)

    UNIT_Train_If_Applicable(mangonel, listener.siege_workshops)


def ResearchUpgrades():  # Runs all functions for researching upgrades

    # ECONOMIC UPGRADES: 
    UPGRADE_Research_If_Applicable(imperial_age) # It is good to check for Imperial Age early, in order to start the red-research-line as early as possible (see the function CheckAgeResearch in Screenshot_Data)

    UPGRADE_Research_If_Applicable(wood1)   
    UPGRADE_Research_If_Applicable(wood2)
    UPGRADE_Research_If_Applicable(wood3)
    UPGRADE_Research_If_Applicable(food1)
    UPGRADE_Research_If_Applicable(food2)
    UPGRADE_Research_If_Applicable(food3)

    UPGRADE_Research_If_Applicable(gold1)
    UPGRADE_Research_If_Applicable(gold2)
    UPGRADE_Research_If_Applicable(stone1)
    UPGRADE_Research_If_Applicable(stone2)

    UPGRADE_Research_If_Applicable(tc_chart1)
    UPGRADE_Research_If_Applicable(tc_chart2)
    UPGRADE_Research_If_Applicable(caravan)
    UPGRADE_Research_If_Applicable(loom)

    

    # MILITARY UPGRADES: 
    UPGRADE_Research_If_Applicable(melee_weapon1)
    UPGRADE_Research_If_Applicable(melee_weapon2)
    UPGRADE_Research_If_Applicable(melee_weapon3)

    UPGRADE_Research_If_Applicable(infantry_armor1)
    UPGRADE_Research_If_Applicable(infantry_armor2)
    UPGRADE_Research_If_Applicable(infantry_armor3)

    UPGRADE_Research_If_Applicable(cavalry_armor1)
    UPGRADE_Research_If_Applicable(cavalry_armor2)
    UPGRADE_Research_If_Applicable(cavalry_armor3)

    UPGRADE_Research_If_Applicable(archer_weapon1)
    UPGRADE_Research_If_Applicable(archer_weapon2)
    UPGRADE_Research_If_Applicable(archer_weapon3)

    UPGRADE_Research_If_Applicable(archer_armor1)
    UPGRADE_Research_If_Applicable(archer_armor2)
    UPGRADE_Research_If_Applicable(archer_armor3)

    UPGRADE_Research_If_Applicable(thumb_ring)
    UPGRADE_Research_If_Applicable(parthian_tactics)
    UPGRADE_Research_If_Applicable(ballistics)
    UPGRADE_Research_If_Applicable(chemistry)
    
    UPGRADE_Research_If_Applicable(bloodlines)
    UPGRADE_Research_If_Applicable(husbandry)

    UPGRADE_Research_If_Applicable(conscription)
    


def RemoveUpgrade(theUpgrade): # Removes the upgrade which was added in CheckRecentlyResearchedUpgrades. This has to be a separate function since it is run with a 60 second delay. 
    Upgrade.recentlyResearchedUpgrades.remove(theUpgrade) # 

def CheckRecentlyResearchedUpgrades(theUpgrade): 

    # STEP 1: Check if the upgrade-type that is being researched has already been researched recently. 
    for loop1_upgrade in Upgrade.recentlyResearchedUpgrades:
        if loop1_upgrade in theUpgrade.name: # If the upgrade contains a keyword: 
            #cprint("The following upgrade was not researched since its predecessor was recently researched: " + theUpgrade.name, "yellow", "on_cyan") 
            return False 


    # STEP 2: Check if the upgrade to research has a level, e.g "melee_weapon 1/2/3"
    for loop2_upgrade in Upgrade.upgradesToCheck:
        if loop2_upgrade in theUpgrade.name: # If the upgrade contains a keyword: 
            Upgrade.recentlyResearchedUpgrades.append(loop2_upgrade)

            # STEP 3: Remove the added upgrade after 60s.    
            thread_removeUpgrade = Timer(Upgrade.time_while_upgradePath_is_disabled, RemoveUpgrade, args=[loop2_upgrade]) # 🔯 Se NEDAN för länken att använda, samt kontrollera att steg 1-3 är på plats. 
            thread_removeUpgrade.start()  

    return True # If we reached this point, the upgrade was not found in the list of recent upgrade (but was added there), so the function approves the researching of this upgrade.  

def CalculateCurrentCost_PER_SECOND():  # Calculates the total cost PER SECOND of the units that are being trained, under the ASSUMPTION that the initially assigned units are being trained (e.g only scouts and knights in the stable)

    # Calculates cost per second by dividing the unit cost with its training time.  



    totalWoodCost = ((listener.markets * trade_chart.wood) / trade_chart.trainingTime + 
                    (listener.archery_ranges * archer.wood) / archer.trainingTime + 
                    (listener.siege_workshops * mangonel.wood) / mangonel.trainingTime + 
                    (listener.castles * uniqueUnit.wood) / uniqueUnit.trainingTime)

    totalFoodCost = ((listener.town_centers * villager.food) / villager.trainingTime  +  
                (listener.stables * knight.food) / knight.trainingTime + 
                (listener.barracks * militia.food) / militia.trainingTime + 
                (listener.castles * uniqueUnit.food) / uniqueUnit.trainingTime)

    totalGoldCost = ((listener.markets * trade_chart.gold) / trade_chart.trainingTime + 
                    (listener.barracks * militia.gold) / militia.trainingTime +
                    (listener.archery_ranges * archer.gold) / archer.trainingTime + 
                    (listener.stables * knight.gold) / knight.trainingTime +  
                    (listener.siege_workshops * mangonel.gold) / mangonel.trainingTime + 
                    (listener.castles * uniqueUnit.gold) / uniqueUnit.trainingTime)

    required_villagers_wood = totalWoodCost / 0.47   # EXAMPLE: Suppose a player spends 3 wood per second. He then needs 3/0.47 [i.e 6.38] lumberjacks. The GAME SPEED is 1.7, so it is divided here to reflect the running-speed of AoE. 
    required_villagers_food = totalFoodCost / 0.32  
    required_villagers_gold = totalGoldCost / 0.44 

    # Takes away the two variables GameSpeed (1.7) and "Unit.trainingTime_compensationFactor". These factors are NOT supposed to be included in this calculation, so they are "weighted back to normal" here. 
    '''
    # Examlpe: 
        1. A knight has a training time of 30 seconds. This value is divided by 1.7 to compensate for game-speed, and multiplied by "trainingTime_compensationFactor" (e.g 0.7)
        2. The totalGoldCost (per second) is calculated by DIVIDING with the knights training time. So at this point, we are DIVIDING TWICE with the compensation-factor. 

            CALCULATION: 6011
            totalGoldCost = 75 / (30*[0.7/1.7])

            To REMOVE the factor [0.7/1.7], we must MULTIPLY by this, so by taking totalGoldCost*[0.7/1.7], we get the new value: 
            actualGoldCost = 75 / 30
    '''
    required_villagers_wood = required_villagers_wood * (Unit.trainingTime_compensationFactor / 1.7) # See explaination above 
    required_villagers_food = required_villagers_food * (Unit.trainingTime_compensationFactor / 1.7)
    required_villagers_gold = required_villagers_gold * (Unit.trainingTime_compensationFactor / 1.7)

    required_villagers_food = round(required_villagers_food)
    required_villagers_wood = round(required_villagers_wood)
    required_villagers_gold = round(required_villagers_gold)

    '''
    COLLECTION RATES USED (villagers with Fedual upgrades, this gives a good rough estimate): 
    # Wood: 0.47 (0.39*1.2) 
    # Food: 0.32
    # Gold: 0.42 (0.38*1.15)
    # (Stone): 0.41 (0.36*1.15)
    '''

    totalFoodCost = round(totalFoodCost)
    totalWoodCost = round(totalWoodCost)
    totalGoldCost = round(totalGoldCost)

  

    return totalWoodCost, totalFoodCost, totalGoldCost, required_villagers_wood, required_villagers_food, required_villagers_gold

        

def MainProductionLoop():  # 013435355

    while True: 

        listener.DEBUG_total_running_time = time.time() - listener.DEBUG_timeStamp_Start # Calculates the time since the bot started running
        listener.DEBUG_total_running_time = round(listener.DEBUG_total_running_time, 0) 

        logger.info("##### NEW ITERATION STARTED. Current Running time: " + str(listener.DEBUG_total_running_time)  + " ##### ")

        cprint("==== NEW ITERATION STARTED. Current Running time: " + str(listener.DEBUG_total_running_time) + " ==== ", "grey", "on_white") #  

        # CALCULATES TIME TO NEXT ITERATION (Explaination below) - It is relevant that this function runs EVEN WHEN THE BOT IS INACTIVE: This will cause the bot to work INSTANTLY when put on (instead of waiting an entire iteration)! 
        listener.time_LEFT_UNTIL_NEXT_ITERATION = listener.timePerIteration + listener.TIMESTAMP_LastIteration - time.time() 
        listener.time_LEFT_UNTIL_NEXT_ITERATION = round(listener.time_LEFT_UNTIL_NEXT_ITERATION, 0)
        ''' 
            How is the time until next iteration calculated?  
            Example: 
                - Declared time per iteration:    25s 
                - Timestamp for last iteration:   50s 
                - Current time:                   60s  
                In this scenario: 
                    * The next iteration will happen at 50+25 seconds. This will of course be 15 seconds from now. 
                    * So, the time until the next iteration will be: 25 + 50 - 60 = 15, i.e:  
                    [Time Left until next iteration] = [Declared Time Per Iteration] + [Timestamp for last iteration] - [Timestamp now] 
        '''

        # CALCULATES TIME TO NEXT Screenshot-reading (Same as above): 
        SCREENSHOT_DATA.time_left_to_next_SCREENSHOT = SCREENSHOT_DATA.timePerIteration + SCREENSHOT_DATA.TIMESTAMP_LastIteration - time.time() 
        SCREENSHOT_DATA.time_left_to_next_SCREENSHOT = round(SCREENSHOT_DATA.time_left_to_next_SCREENSHOT, 0)

        if listener.botActive == False and SCREENSHOT_DATA.time_left_to_next_SCREENSHOT < 0: #0
            SCREENSHOT_DATA.TIMESTAMP_LastIteration = time.time() 
            SCREENSHOT_DATA.UpdateScreenshot()
            SCREENSHOT_DATA.UpdateVariables_THREAD() # Tar ett screenshot och uppdaterar alla screenshot-variabler  00000


        '''FÖRKLARING AV NEDANSTÅENDE: Programmet ska INTE fortsätta exekvera i loopen om NÅGOT påståendena är uppfyllda. 
        Sats 1: Botten är inte aktiv.
        Sats 2: Time-till force_run är inte uppnådd, eller så är force-control satt till false.     
        
        Exempel 1: Botten är inte aktiv. Vi har överskridit tid för force_run_time, men force_take_control är satt till false: 
            Outcome: Påstående 1 är true. Påstående 2 är True (eftersom satsen force_take_control är False)
        
          '''

        should_the_bot_run = True # Assume the bot should be run, then set it to False as soon as a critical condition isn't met.  

        if listener.time_LEFT_UNTIL_NEXT_ITERATION > 0:   # Om vi inte kommit till tid 0 för tid till nästa iteration, ska botten inte köra. 
            #cprint("1. Bot did not run - Time to the next iteration has not come. ", "yellow")
            should_the_bot_run = False

        elif listener.botActive == False: # If the bot is not currently running, it should only run if the conditions for force_control are met. bqzbjqbkqblwbqsbgc-
            cprint("The bot is not active. The variable 'botActive' is set to " + str(listener.botActive), "yellow")  #0bqzbjqbkqblqblw0bqs
            if (listener.time_LEFT_UNTIL_NEXT_ITERATION > -listener.force_run_time or listener.force_take_control == False):
                #cprint("2. Bot did not run. EITHER the [time until the time when the bot takes control] has not come, OR force_take_control is turned off", "yellow")
                should_the_bot_run = False
            else: 
                # The bot runs. botActive and blockActive are set to true. 
                listener.botActive = True # Toggles the value botActive. 
                 
            
        
        if should_the_bot_run == True: 
        
            cprint("===RUNNING LOOP===", "blue")

            listener.TIMESTAMP_LastIteration = time.time() 
            
            # MYCKET VIKTIGT: När klassen Input_Block initieras får PARANTESER INTE ANVÄNAS dvs "Input_Block()" -> Då initierar man en NY Input_Block och det blir kaos. 
            # OCKSÅ VIKTIGT: klassen MÅSTE initieras genom en TRÅD eftersom att den ska köras kontinuerligt (annas fungerar inte keyboard disable). 

            # ======== ECONOMIC UNITS ======== 
            if SCREENSHOT_DATA.popCapReached == False:  # Checks for population cap. 

                if (SCREENSHOT_DATA.totalVillagers < Caps.villagerMax):
                    UNIT_Train_If_Applicable(villager, listener.town_centers)
                else: # 
                    cprint("No villagers were trained since the user has " + str(SCREENSHOT_DATA.totalVillagers) + " villagers and the villager cap is " + str(Caps.villagerMax), "yellow") 

                if (SCREENSHOT_DATA.villagersGold < Caps.trade_chartMax):
                    UNIT_Train_If_Applicable(trade_chart, listener.markets)
                else: # 
                    cprint("No trade charts were trained since the user has " + str(SCREENSHOT_DATA.villagersGold) + " gold workers and the trade chart cap is " + str(Caps.trade_chartMax), "yellow") 


            # ======== UPGRADES ======== 
            
            if listener.researchUpgrades == True: 
                ResearchUpgrades() # Contains all upgrades to research 

            else: 
                cprint("NO UPGRADES WERE RESEARCHED - researchUpgrades was False", "yellow") 
                
            # ======== MILITARY UNITS ======== 
            if SCREENSHOT_DATA.popCapReached == False:  # Checks for population cap. 

                # IMPORTANT: List the units to train here IN ORDER OF PRIORITY (And remember they are ALSO prioritized based inputs to listener. )

                TrainUnits()

                

            else: 
                cprint("No units could be trained, User Pop-capped", "yellow")

        # RESETS VARIABLES USED DURING LOOP
        Input_Blocker.blockActive = False # Switches Input_blocker off.
        listener.botActive = False

        time.sleep(1) # Det är bra att ha ett kort delay här --> Detta minskar processkraft REJÄLT ifall alla if-satser ovan är checkade (för isåfall kommer funktionen att köra om sig själv extremt ofta)
    

# ==== DEFINE ALL UNITS ====  1353
villager = Unit("villager") 
trade_chart = Unit("trade_chart") 

militia = Unit("militia") 

archer = Unit("archer")
cavalry_archer = Unit("cavalry_archer")

knight = Unit("knight")
scout_cavalry = Unit("scout_cavalry")

mangonel = Unit("kipchak")


uniqueUnit = Unit(UNIQUE_UNIT_NAME) 


# ==== DEFINE ALL UPGRADES ====   
wood1 = Upgrade("wood1")
wood2 = Upgrade("wood2")
wood3 = Upgrade("wood3")
food1 = Upgrade("food1")
food2 = Upgrade("food2")
food3 = Upgrade("food3")

gold1 = Upgrade("gold1")
gold2 = Upgrade("gold2")
stone1 = Upgrade("stone1")
stone2 = Upgrade("stone2")

tc_chart1 = Upgrade("tc_chart1")
tc_chart2 = Upgrade("tc_chart2")
caravan = Upgrade("caravan")
loom = Upgrade("loom")

melee_weapon1 = Upgrade("melee_weapon1")
melee_weapon2 = Upgrade("melee_weapon2")
melee_weapon3 = Upgrade("melee_weapon3")

infantry_armor1 = Upgrade("infantry_armor1")
infantry_armor2 = Upgrade("infantry_armor2")
infantry_armor3 = Upgrade("infantry_armor3")

cavalry_armor1 = Upgrade("cavalry_armor1")
cavalry_armor2 = Upgrade("cavalry_armor2")
cavalry_armor3 = Upgrade("cavalry_armor3")

archer_weapon1 = Upgrade("archer_weapon1")
archer_weapon2 = Upgrade("archer_weapon2")
archer_weapon3 = Upgrade("archer_weapon3")

archer_armor1 = Upgrade("archer_armor1")
archer_armor2 = Upgrade("archer_armor2")
archer_armor3 = Upgrade("archer_armor3")

thumb_ring = Upgrade("thumb_ring")
parthian_tactics = Upgrade("parthian_tactics")
ballistics = Upgrade("ballistics")
chemistry = Upgrade("chemistry")

bloodlines = Upgrade("bloodlines")
husbandry = Upgrade("husbandry")
conscription = Upgrade("conscription")

imperial_age = Upgrade("imperial_age")


# ==== DEFINE ALL PROGRAM-SPECIFIC CLASS-OBJECTS ====  

UpdateUnitData() # Updates unit data, e.g makes persian archers cost wood. 

unitCounter = UnitCounter()

listener = ListenerClass() # <--  Skapar listener  #  
lyssnare_thread = Listener(on_press=listener.OnKeyDown, on_release=listener.OnKeyUp)
lyssnare_thread.start()

SCREENSHOT_DATA = Screenshot_Data()

mainLoop = Thread(target=MainProductionLoop)
mainLoop.start()



'''
# ==== ALTNERNATIVT SÄTT ATT KÖRA LISTENER PÅ ====
with Listener(on_press=listener.OnKeyDown, on_release=listener.OnKeyUp) as lyssnare:
    lyssnare.join() # gör att programmet kör tills listener är färdig
'''

# from DisplayText import SkapaTkinterFönster 
import tkinter as tk
class SkapaTkinterFönster():

    def __init__(self):
        
        self.root = tk.Tk()  # Defines the root tkinter (Vet ej exakt vad detta gär- )

        # === DEFINE THE WINDOWS ===
        self.text = tk.StringVar() # <<<<<<<< REMOVE 
        self.text_window1 = tk.StringVar() # Defines a text object. 
        self.text_window2 = tk.StringVar() # Defines a text object. 

        self.label_window1 = self.CreateWindow(1) # Creates a new window 
        self.label_window2 = self.CreateWindow(2) # Creates a new window 

        # === REMOVES MAIN-WINDOW (A main window is created automatically - this is not to be used, so it is removed here) ===
        self.label = tk.Label(self.root, textvariable="")  
        self.label.master.geometry("+3000+0") # Sets the position of the window OUTSIDE OF THE SCREEN. 


        # === INITIATE THE WINDOWS ===
        self.root.after(1000, self.changeText) # Kör funktionen som regelbundet uppdaterar texten.  
        self.label_window1.pack()
        self.label_window2.pack()

     # self.label.pack() # 00
        self.root.mainloop()

    
    def CreateWindow(self, window_number):
        new_window = tk.Toplevel(self.root)

        if window_number == 1: 
            #new_window.geometry("200x300") # Sets the SIZE of the window  
            label = tk.Label(new_window, textvariable = self.text_window1, justify="left") # IMPORTANT -> It MUST say "textvariable" [not "text"] for the variable to be changed! 
            label.master.geometry("+2260+360") # Sets the POSITION of the window.  

        elif window_number == 2: 
            # new_window.geometry("700x70") # Sets the SIZE of the window
            label = tk.Label(new_window, textvariable = self.text_window2, justify="left") # IMPORTANT -> It MUST say "textvariable" [not "text"] for the variable to be changed! 
            label.master.geometry("+32+220") # Sets the POSITION of the window.


        elif window_number == 3: 
            #new_window.geometry("200x300") # Sets the SIZE of the window
            label = tk.Label(new_window, textvariable = self.text_window3, justify="left") # IMPORTANT -> It MUST say "textvariable" [not "text"] for the variable to be changed! 
            label.master.geometry("+600+400") # Sets the POSITION of the window.  

        else:
            label = ""
            print("ERROR - WRONG NUMBER ENTERED")
        

        # === DEFINE GENERAL WINDOW PROPERTIES ===
        # TEXT
        label.config(font=("Courier", 14))

        # REMOVE ABILITY TO INTERACT
        label.master.overrideredirect(True) # Tar bort mojligheten att kryssa/minimera fonstret. 
        label.master.lift()  # Vet ej vad funktionen gor, men v�rt att l�gga in. 
        label.master.wm_attributes("-topmost", True) # Gor s� att bilden ligger l�ngst fram p� sk�rmen (dvs den syns alltid �ven om man har massa fonster oppna)
        label.master.wm_attributes("-disabled", True) # Gor s� att sk�rmen inte kan interageras med. 
        

        return label # RETURNS new window so that the program can STORE this window and update it


    def changeWindowColor(self): # Changes the color of the window depending on the bot's current state, making it easier to tell what the bot is doing. 

        if listener.botActive == False: # If the bot is not active 
            self.label_window1.config(bg= "gray", fg= "white")

            if (listener.time_LEFT_UNTIL_NEXT_ITERATION < -listener.warning1_time ):  # If too long time has passed since the last iteration. 
                self.label_window1.config(bg= "yellow", fg= "black")

            if (listener.time_LEFT_UNTIL_NEXT_ITERATION < -listener.warning2_time ):  # If too long time has passed since the last iteration. 
                self.label_window1.config(bg= "red", fg= "yellow")

        elif listener.botActive and listener.time_LEFT_UNTIL_NEXT_ITERATION < 0: # If the bot is running 
            self.label_window1.config(bg= "black", fg= "white")

        

        if False: # If the bot is active, but not running
            self.label_window1.config(bg= "green", fg= "yellow") 

 
    def changeText(self): # Continiously updates the text on the window    0

        self.changeWindowColor()

        
        newText_window1 = "" # "Declares" the textvariables in case they are for any reason not assigned in the if-statements below. 
        newText_window2 = ""

        # =====================================================================
        # === WINDOW 2: RECOMMENDED VILLAGER DISTRIBUTION (Separate Window) ===  
        # Calculates total cost: 
        currentCost_wood, currentCost_food, currentCost_gold, required_villagers_wood, required_villagers_food, required_villagers_gold = CalculateCurrentCost_PER_SECOND() # Shows the total cost. 
        total = currentCost_wood + currentCost_food + currentCost_gold
        if total != 0: 
            # round(listener.DEBUG_total_running_time, 0) 
            percent_wood = round((currentCost_wood / total)*100)
            percent_food = round((currentCost_food / total)*100)
            percent_gold = round((currentCost_gold / total)*100)

            # newText_window2 = newText_window2 + "\n"1363
            
            space1 = "         "
            space2 = "        "
            #space = ""

            newText_window2 =   (str(required_villagers_wood).zfill(2) + space1 + 
                                str(required_villagers_food).zfill(2) + space1 +
                                str(required_villagers_gold).zfill(2) + "\n")
            newText_window2 = newText_window2 + str(percent_wood).zfill(2) + "%" + space2 + str(percent_food).zfill(2) + "%" + space2 + str(percent_gold).zfill(2) + "%"

            '''
            newText_window2 = newText_window2 + "\nWood:\t" + str(percent_wood) + "%\t" + str(required_villagers_wood) + "     "
            newText_window2 = newText_window2 + "\nFood:\t" + str(percent_food) + "%\t" + str(required_villagers_food) + "     "
            newText_window2 = newText_window2 + "\nGold:\t" + str(percent_gold) + "%\t" + str(required_villagers_gold) + "     "
            listener.ReturnBaseData()

            '''

            newText_window2 = newText_window2 + "\nTot: " + str(required_villagers_wood+required_villagers_food+required_villagers_gold) + "\n"

            newText_window2 = newText_window2 + listener.ReturnBaseData()

        # =============================
        # === WINDOW 1: MAIN WINDOW ===  
        # =============================

        # === DISPLAYS BOOL-STATEMENTS ===  
        if (listener.researchUpgrades == False):
            researchUpgradeText = "\nUPGRADES: OFF"
        else:
            researchUpgradeText = "\nUPGRADES: ON"  
        if (listener.force_take_control == False):
            researchUpgradeText += "\nforce_take_control: OFF"
        else:
            researchUpgradeText += "\nforce_take_control: ON"  
        
        # BASE TEXT (included in multiple states)
        newText_window1 = ""
        newText_window1 = newText_window1 + "\n" + researchUpgradeText 
        newText_window1 = newText_window1 + "\n" + "Screenshots progress:\n" + SCREENSHOT_DATA.ReturnProgressBar(SCREENSHOT_DATA.screenshotsTaken_CurrentIteration)

        
        #newText_window1 = newText_window1 + "\nScreenshots left:\n" + str(SCREENSHOT_DATA.screenshotsTaken_CurrentIteration) + "/" + str(SCREENSHOT_DATA.screenshots_TO_TAKE_per_iteration)

        # === DISPLAY: STATE 1: BOT IS RUNNING === 
        if (listener.time_LEFT_UNTIL_NEXT_ITERATION < 0 and listener.botActive):  # if the bot is running.  
                newText_window1 = "\n\n\n\n\n" + "BOT IS WORKING!" + "\n" + newText_window1

                newText_window1 = newText_window1 + "\n" + "Training/Researching:\n" + str(Input_Blocker.objectThatIsBeingTrained)
                newText_window1 = newText_window1 + "\n" + "Recent Upgrades:\n"
                for loopUpgrade1 in Upgrade.recentlyResearchedUpgrades:
                    newText_window1 = newText_window1 + " " + loopUpgrade1 + "\n"
                newText_window1 = newText_window1 + "\n\n\n\n\n" # Adds a bunch of new lines to make the window large.     

        # === DISPLAY: STATE 0: BOT IS NOT RUNNING === 
        else:  

            if listener.windowToDisplay == 1: 
                
                # ADD ADVICE HERE 
                newText_window1 = newText_window1 + "\n\nADVICES:" 

                if (SCREENSHOT_DATA.wood + SCREENSHOT_DATA.food + SCREENSHOT_DATA.gold > 1500):
                    newText_window1 = newText_window1 + "\n" + "- Assign more\nproduction buildings!!!" 

                if (SCREENSHOT_DATA.stone > 650):
                    newText_window1 = newText_window1 + "\n" + "- Build Castle" 

                if (SCREENSHOT_DATA.villagersWood > SCREENSHOT_DATA.villagersFood):
                    newText_window1 = newText_window1 + "\n" + "- Make Farmers: " + str(SCREENSHOT_DATA.villagersWood) + "/" + str(SCREENSHOT_DATA.villagersFood) 


                # TIME TO NEXT ITERATION.  
                newText_window1 = newText_window1 + "\n\n" + "Next iteration:" + "\n" + str(listener.time_LEFT_UNTIL_NEXT_ITERATION)
    
            elif listener.windowToDisplay == 2:  # DEBUG:  Shows the screensot data, and if the bot is active.  
                newText_window1 = SCREENSHOT_DATA.ReturnScreenshotData() # Printar ut den data som läses av från screenshottet. 
                newText_window1 = newText_window1 + "\n" + "Screenshots:" + str(SCREENSHOT_DATA.DEBUG_ScreenshotsTaken) # Räknar antalet ti0d som tagits. 
                newText_window1 = newText_window1 + "\n" + "DEBUG (total time): " + str(listener.DEBUG_total_running_time) 
                newText_window1 = newText_window1 + "\nInput disabled? " + str(Input_Blocker.blockActive)
                newText_window1 = newText_window1 + "\n" + researchUpgradeText
                
                
            elif listener.windowToDisplay == 3:  # DEBUG: Shows the counted trained units.  0000
                newText_window1 =                 "infantry: " + str(unitCounter.infantry) + "\n" 
                newText_window1 = newText_window1 + "archers: " + str(unitCounter.archer) + "\n" 
                newText_window1 = newText_window1 + "cavalry: " + str(unitCounter.cavalry) + "\n" 
                newText_window1 = newText_window1 + "cavalry_Archers: " + str(unitCounter.cavalry_Archer) + "\n" 
                newText_window1 = newText_window1 + "siege weapons: " + str(unitCounter.siege_Weapon) + "\n" 

            else: 
                newText_window1 = "No mode selected. \n Mode = " + str(listener.windowToDisplay)

        # SETS TEXTS FOR WINDOWS  
        self.text_window1.set(newText_window1)  
        self.text_window2.set(newText_window2)  
        

        time_to_update_window_MS = 100 # Runs the function changeText with updades the text, every. The program does NOT appear to lag even if this function is run every 1 ms. 
        self.root.after(time_to_update_window_MS, self.changeText) 

''' 
==== SLUTSATS ANGÅENDE tkinter-FÖNSTER ====    

- Enligt koden jag skrev är programmet gjort så att raden "mainloop" SKA VARA I SLUTET av koden:
    = "Put in the simplest terms possible: ALWAYS CALL MAINLOOP AS THE LAST LOGICAL LINE OF CODE IN YOUR PROGRAM. 
        That's how Tkinter was designed to be used." 
    * ALLTSÅ  är det bara att acceptera det och göra koden som den är. 
    * Koden MÅSTE LIGGA I DETTA DOKUMENT eftersom att den måste kunna ta in text från resten av funktionerna. 
    Jag är mycket tveksam till ifall det är värt att köra dubbla importer, så det är läggare att bara lägga texten här.   
'''


fönster = SkapaTkinterFönster() # <<<< DENNA RAD MÅSTE KÖRAS I SLUTET AV PROGRAMMET   







