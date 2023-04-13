

# SOURCE: https://pypi.org/project/pytesseract/
# path: C:\Program Files\Tesseract-OCR

from PIL import Image
from PIL import ImageEnhance
import PIL.ImageGrab
import PIL.ImageOps


from threading import Thread

import numpy as np
from pynput.keyboard import Key, Controller, Listener
from termcolor import cprint
import time



import pyautogui

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

class Screenshot_Data():

    def __init__(self):
        self.currentScreenshot = pyautogui.screenshot() 

        # Inherits Listener class 
     
        
        # RESOURCES AND VILLAGERS: 
        self.wood = 0
        self.food = 0
        self.gold = 0
        self.stone = 0

        self.villagersWood = 0
        self.villagersFood = 0
        self.villagersGold = 0
        self.villagersStone = 0

        self.popCapReached = False 
        self.totalVillagers = 0 
        self.age = 1 # Age is an integer between 1-4, where 1 is Dark Age. 
        self.screenshotsTaken_CurrentIteration = 0 # Counts the amount of screenshots that have been taken at this point. 
        self.screenshots_TO_TAKE_per_iteration = 11 # A CONSTANT representing the amount of screenshot cutouts to be taken every ireration. At the time of wiring this, the variable above is 11: They are all variables listed above. 

        # Manages time per iteration [The screenshot data-function will read the player resources once every few seconds]
        self.TIMESTAMP_LastIteration = 0
        self.timePerIteration = 5 # The time between each iteration that takes screenshots. 
        self.time_left_to_next_SCREENSHOT = 0

        self.DEBUG_PicturesShown = 0 # DEBUG: ANvänds för att förhindra att fler än 10 bilder visas; Varje gång "Show" används: Kör den bara så länge DEBUG_PicturesShown < 10
        self.DEBUG_ScreenshotsTaken = 0

    def ReturnProgressBar(self, currentProgress): # Returns a progress bar, allowing the program to visualise the progress of the screenshots. 

        progressString = ""
        fullProgress = "###########" # Eleven (11), since 11 screenshots are taken. 
        for x in range(currentProgress):
            progressString = progressString + "#"
        progressString = progressString + "\n" + fullProgress
        return progressString

    def ReturnScreenshotData(self): # Returns all stored data in the script.  
         
        sträng = (
                "wood: "           + str(self.wood) + "\n"
                "food: "           + str(self.food) + "\n"
                "gold: "           + str(self.gold) + "\n"
                "stone: "          + str(self.stone) + "\n"
                "villagersWood: "  + str(self.villagersWood) + "\n"
                "villagersFood: "  + str(self.villagersFood) + "\n"
                "villagersGold: "  + str(self.villagersGold) + "\n"
                "villagersStone: " + str(self.villagersStone) + "\n"
                "totalVillagers: " + str(self.totalVillagers) + "\n"
                "popCapReached: "  + str(self.popCapReached) + "\n"
                "AGE: "            + str(self.age) + ""
                )
        return sträng

    def PrintCurrentData(self):
        cprint(self.ReturnScreenshotData(), "yellow") 

    def UpdateScreenshot(self): # 0. SYFTE: Tar ett nytt screenshot. 
        self.currentScreenshot = pyautogui.screenshot()
        self.DEBUG_ScreenshotsTaken += 1

    
    def DEBUG_ShowImage(self, picture): # DEBUG-FUCTION: Shows the image, provided that no more than [self.DEBUG_PicturesShown] has already been shown. 


        if self.DEBUG_PicturesShown < 5:
            picture.show()
            self.DEBUG_PicturesShown += 1
        

    def UpdateVariables_THREAD(self): # SYFTE: Eftersom UpdateVariables (Som läser av all data) tar ca 2 sekunder att köra, körs det i bakgrunden av programmet i en separat tråd. Här skapas tråden. 

        updateVariablesThread = Thread(target=self.UpdateVariables, args=([])) # Notera att en tråd INTE startar om man har paranteser "Brekfast()"; skriv BARA funktionen "Brekfast"
        updateVariablesThread.start()
        # Note that no ".join" is used here since we don't want to wait for the thread to finish before moving on with the program. 
    

    def UpdateVariables(self): # 0. SYFTE: Uppdaterar alla variabler genom att köra funktionen en gång i taget. 
        
        self.screenshotsTaken_CurrentIteration = 0 # Resets the screenshots taken, so that the bot doesn't keep counting screenshots taken during previous iterations.  

        # CHECKS POP-CAP: Note that it is good to check this variable FIRST since it takes the longest time (This makes it easier to alert the user when the bot is complete with all checks below). 
        popCapThread = Thread(target=self.CheckPoPCap, args=([])) # Notera att en tråd INTE startar om man har paranteser "Brekfast()"; skriv BARA funktionen "Brekfast"
        popCapThread.start() # Startar tråden
        #popCapThread.join() # Väntar tills tråden är klar. 
        self.screenshotsTaken_CurrentIteration += 1 # Adds a screenshot indicating that the pop-cap-thread is finished. 

        self.wood = self.Return_Screenshot_Data("wood")
        self.food = self.Return_Screenshot_Data("food")
        self.gold = self.Return_Screenshot_Data("gold")
        self.stone = self.Return_Screenshot_Data("stone")

        

        self.villagersWood = self.Return_Screenshot_Data("villagersWood")
        self.villagersFood = self.Return_Screenshot_Data("villagersFood")
        self.villagersGold = self.Return_Screenshot_Data("villagersGold")
        self.villagersStone = self.Return_Screenshot_Data("villagersStone")

        self.totalVillagers = self.Return_Screenshot_Data("totalVillagers")  

        if (self.age < 4): # if the age is 4, we have reached the imperial age, and there is no need to check for this variable any more.
            self.age = self.Return_Screenshot_Data("Age", "string") # Since age is a string, we add that as one of the parameters in the Screenshot-data function.  

        
    

    def CheckPoPCap(self, iteration=1): # Checks if user is population-capped (See comment below for more info)

        if iteration < 4: # Programmet ska köras 3 gånger, dvs då iteration är 1, 2 respektive 3.   
            newScreenshot = pyautogui.screenshot() # Ta ett screenshot  
            cutout = self.CropImage(newScreenshot, "popCapReached") # Cuts out the area for population 

            r, g, b = cutout.getpixel((2, 2)) # Tar fram färg på pixlarna. 
            # print(str(r) + " " + str(g)+ " " +str(b)) # KORREKT FÄRG för pop-cap är enl PAINT: 178 / 178 / 0

            if r > 100 and g > 100: 
                #cprint("POPULATION CAPPED", "yellow")
                self.popCapReached = True
                
                return # RETURNERAR funktionen 
            else:
                #print("POPULATION CAPPED", "blue")
                if iteration == 3: # 
                    self.popCapReached = False

            '''
            IDÉ FÖR FUNKTIONEN : 
            1. Funktionen kör 3 ggr, dvs då "iteratiion" har värdena 1, 2 och 3. 
            2. Varje iteration kollar om den hittar en gul pixel. 
                2a. OM vi hittar en gul pixel betyder det att vi är housad -> Då kör funktionen "return" direkt vilket ska göra att funktionen SLUTAR köra. 
                2b. Om vi är i tredje iterationen och årogrammet inte hittar några gula pixlar betyder det att ingen av de tidigare iterationerna gjorde det heller
                (eftersom loopen isåfall hade brutits genom return- )
            
            '''
            iteration += 1 
            time.sleep(0.4)
            self.CheckPoPCap(iteration)

    def CheckAgeResearch(self, cutout): 
        '''
        EXPLAINATION: If the parameter is age, we must check for any red lines along the age-icon. This is because if the Imperial age is being research, 
        the text "Imperial Age" while the red "research-line" grows. So if we detect any red line, we cant 
        we  (This must be done BEFORE the color is removed)

        NOTE: This function is NOT foolproof -> If imperial age is researched RIGHT BEFORE the bot-loop starts, the bot won't see the red line because
        it doesn't appear the first few seconds. However, this scenario is VERY UNLIKELY. 

        '''
        r, g, b = cutout.getpixel((1, 10)) # Checks the color at the given coordinate.  

         
        cprint("The red color in the window was calculated to: " + str(r), "red", "on_green")

        if r > 50: # if more than 50 red was detected, it means we have found the "research-line" and that the current text on the screen for the age shows the age we are RESEARCHING, not the one we have 
            return True

        return False 


    def Return_Screenshot_Data(self, parameter, inputType = "int"): # 1. SYFTE: Tar in en parameter, t.ex "food", och returnerar den parametern genom att läsa av screenshottet. 
        
        bild = self.CropImage(self.currentScreenshot, parameter) # Skickar in parametern i funtionen CropImage som returnerar bilden. 

        if parameter == "Age": 

            if self.CheckAgeResearch(bild): 
                cprint("A RED COLOR IN THE AGE-WINDOW WAS DETECTED! (indicating that a new age is being researched but is not yet finished, so the current age should not be updated yet). The returned age is: " + str(self.age), "red", "on_green")

                return self.age # If we detected a red line, the function should simply return the current age. If no line was detected, the program will proceed with reading the text on the screen. 

        bild = self.AddBorder(bild) # Lägger in en border i bilden för att öka läsbarhet. Denna funktion är potentiellt sett inte alltid nödvändig. 
        
        self.screenshotsTaken_CurrentIteration += 1 # Registrers that a screenshot-cutout has been taken. 
        
        if inputType == "int":
            text_configuration ="-c tessedit_char_whitelist=0123456789"

        else:
            text_configuration = "-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzADFCI" # The capital characters "A, D, F, C, I" are included in the 4 different ages. 



        resultat = pytesseract.image_to_string(bild, config= text_configuration) # Det som står i whitelist är de ENDA tecknena som tillåts! Exempelvis för bokstäver: whitelist=abcdefghijklmnopqrstuvwxyz   #  --psm 7
        resultat = resultat.replace("\n", "") # Removes new lines
        resultat = resultat.replace(" ", "") # Removes spaces 

        if resultat.replace(" ", "") == "": 
            #cprint("RESULT DOES NOT EXIST", "red") 
            #self.DEBUG_ShowImage(bild)

            if (parameter == "food" or parameter == "wood" or parameter == "gold"):
                cprint(f"Value {parameter} read as 0 - It is fairly likely that this value is not read correctly", "red", "on_white")
             
            
            return 0

        if inputType == "string":  # If the parameter was AGE, it is meant to return a NUMBER and not a text. 

            if parameter == "Age": 
                if "Feudal" in resultat:
                    return 2

                elif "Castle" in resultat:
                    return 3
                
                elif "Imperial" in resultat:
                    return 4

                return self.age # If neither age 2, 3 och 4 was detected, the age should return itself (i.e be unchanged) 


        #print("The discovered value was " + str(resultat))

        if inputType == "int": 
            resultat = int(resultat)
  
        return resultat


    def CropImage(self, imageF, target): # 2. Plockar ut den bit av bilden som söks (T.ex resource count eller villager count)
        
        '''STORLEKER OCH POSITIONER FÖR URKLIPPNING (Gäller för mod: "Better readable Ressource Panel"). 
        Med Paint är det mycket smidigt att ta fram dessa värden. 
        Storleker på respektive bars: 
            * Resources: 72*32        NOTE The y-values here must be lowered by 5 pixles (for y), since the bars are smaller for some civs such as byzantines! 
            * Villagers: 53*26
            * Age: 797,21  -> Storkek på fönster: 215*30

        === KOORDINATER === 
                        Wood        Food        Gold        Stone       Pop / MaxPop
        RESOURCES:      (9,36)      (134,36)    (259,36)    (384,36)    (509,36)    [X ökar konsistent med 125 pixlar]
        VILLAGERS:      (62,21)     (187,21)    (312,21)    (437,21)    (562,21)    [X ökar konsistent med 125 pixlar]
        '''

        # VARIABLES: X och Y är positionen vi börjar titta. (1) Storleken av rutan bestäms av om det är en Resource eller VillagerCount. (2) x-förskjutningen ökar konsistent med 125  (3) y-förskjutningen är konstant. 
        x = 0
        y = 0 
        x_end = 0
        y_end = 0
        

        if (target == ("wood") or target == ("food") or target == ("gold") or target == ("stone") or target == ("popCapReached")):
            x = 62 # Första rutan för Resources (i.e food count) är på koordinaterna (62,20)
            y = 21
            x_displacement = 125 
            if(target == ("food")):
                x += x_displacement
            if(target == ("gold")):
                x += x_displacement*2
            if(target == ("stone")):
                x += x_displacement*3
            if(target == ("popCapReached")): 
                x += x_displacement*4
            x_end = x+72 
            y_end = y+31 -5 # The -5 is to cover for byzantines, who has a smaller interface. 
            
        elif (target == ("villagersWood") or target == ("villagersFood") or target == ("villagersGold") or target == ("villagersStone") or target == ("totalVillagers")):
            x = 9 # Första rutan för villagers (i.e food count) är på koordinaterna (62,20)
            y = 36
            x_displacement = 125 # (2) x-förskjutningen ökar konsistent med 125 när man går från vänster till höger
            if(target == ("villagersFood")):
                x += x_displacement
            if(target == ("villagersGold")):
                x += x_displacement*2
            if(target == ("villagersStone")):
                x += x_displacement*3
            if(target == ("totalVillagers")):
                x += x_displacement*4

            x_end = x+53 # Rutorna för villager counts har storleken 52*26. 
            y_end = y+26-5 # The -5 is to cover for byzantines, who has a smaller interface. 
            
        elif (target == "Age"):
            x = 797
            y = 21
            x_end = x+215
            y_end = y+30
            

        else: 
            cprint("MILITARY DATA REQUESTED - DOESNT EXIST AT THIS TIME", "red") 

        
        cropped_im = imageF.crop((x, y, x_end, y_end)) # Inom parantesen "Crop" inkluderas 2 koordinater (x1,y1, x2,y2) som anger start/slut för den yta som ska croppas. 

        #if target == "Age": 
            #self.DEBUG_ShowImage(cropped_im) 
        
        return cropped_im

    def AddBorder(self, inputImage): # 3. SYFTE: Skapar en ram runt bilden i input och returnerar den nya bilden med en svart ram. 
    
        # Lägger in en frame 
        old_size = inputImage.size   # <<< ATT GÖRA: 
        frame_size = (40,40) # Anger tjockleken på ramen. 

        new_size = tuple(map(sum,zip(old_size,frame_size))) # Lägger ihop 2 tuples: Bildens storlek samt ramens tjocklek. 
        new_image = Image.new("RGB", new_size)  # Följande 2 rader skapar den svarta ramen. 
        new_image.paste(inputImage, ((new_size[0]-old_size[0])//2,
                            (new_size[1]-old_size[1])//2))

        # KOLLA EFTER POP-färg 
        
        # Övriga funktioner för att öka läsbarhet.  
        new_image = PIL.ImageOps.invert(new_image) # Inverterar bilden så den blir svart med vit bakgrund. 
        enhancer = ImageEnhance.Sharpness(new_image)
        factor = 20
        new_image = enhancer.enhance(factor) # 
        gray = new_image.convert('L')
        new_image = gray.point(lambda x: 0 if x<2 else 255, '1')

        #new_image.show()

        return new_image


#screenshotData = Screenshot_Data()
#screenshotData.UpdateVariables()









