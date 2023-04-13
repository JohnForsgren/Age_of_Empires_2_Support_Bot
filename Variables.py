


'''
STANDARDISERING för hur namn anges: 

- Units anges enligt: 
    - deras lägsta uppgradering; t.ex "champion" benämns med "militia"
    - Deras namn börjar med liten bokstav, dvs "villager" och inte "Villager"

- Upgrades anges enl nedan: 
    - Eco Upgrades: "farm1/2/3", etc. 
    - Blacksmith Upgrades: "meeleWeapon1/2/3" "infantryArmor1/2/3", etch 


- TANKE: Eventuellt borde units anges med en Unit-klass istället. Detta eftersom varje unit har flera parametrar: 
    - Enhetens namn, t.ex "villager"
    - lastCreation
    - creationTIme 
    - wood / food / gold cost. 


'''
from termcolor import cprint # Webpage for Cprint: https://pypi.org/project/termcolor/
import logging 



# === LOGGER === (Allows the program to print everything )
logging.basicConfig(filename="P:\\_PROGRAMMERING\\AoE2_Support_Bot\\log.txt",
            filemode='w',
            format='%(asctime)s,%(msecs)d,%(name)s,%(levelname)s,%(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG)




'''Kommentarer angående användning av loggern: 

    * Notera att följande rad måste vara i början av alla script som ska använda loggern: logger = logging.getLogger('[Scriptets namn skrivs här]')

    * Loggern kan loggas genom t.ex: logger.info("string")
    * Notera att textfilen "log.txt" i nuläget inte rensas i början på varje fil. 

'''

# 

class UnitCounter:


    def __init__(self):
        self.infantry = 0
        self.archer = 0
        self.cavalry = 0
        self.cavalry_Archer = 0
        self.siege_Weapon = 0
        self.trade_chart = 0 

    def CountUnitTrain(self, unitType, quantity):
        if unitType == "infantry":
            self.infantry += quantity
        elif unitType == "archer":
            self.archer += quantity
        elif unitType == "cavalry":
            self.cavalry += quantity
        elif unitType == "cavalry_archer":
            self.cavalry_Archer += quantity
        elif unitType == "siege_weapon":
            self.siege_Weapon += quantity
        elif unitType == "trade_chart":
            self.trade_chart += quantity
        

    
class Caps: 

    villagerMax = 120
    trade_chartMax = 40

    foodMax = 5000 # If max food or wood is reached, the bot can use the market to sell food. 
    woodMax = 5000 # 
    stoneMax = 650 # The program should signal to the user that a castle should be built. 









