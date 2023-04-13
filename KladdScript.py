

import random




def RandomizeDelay(inputDelay): # Takes an input-delay and makes it anywhere between 30% longer or 30% shorter.  

    randomFactor = random.uniform(0.7, 1.3)
    randomFactor = round(randomFactor, 1) 
    newDelay = inputDelay*randomFactor
    print("new increase/decrease : " + str(randomFactor))

    return newDelay

    x= 5



print(RandomizeDelay(0.1))
print(RandomizeDelay(0.5))
print(RandomizeDelay(1))





