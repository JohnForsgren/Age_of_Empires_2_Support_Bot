# Age-of-Empires-Support-Bot
A helper bot that automates tasks in the computer game Age of Empires II.

A video Demo of the bot can be found here:
https://www.youtube.com/watch?v=LbjOrQzaB8o

The purpose of the bot is to spend the player's resources automatically when playing the game. Features: 
* Uses the PIL and pytesseract libraries to read data from the screen, providing the bot with user data (e.g amount of in-game resources). 
* Uses the "mouse" & "keyboard" libraries to temporarily disable the user's mouse and keyboard, as well as executing keyboard commands. 
* Intelligently executes keyboard commands to spend the player's resources according to a list of rules. 
* Runs asynchronously with multiple threads. This lets the bot cycle between executing commands & being idle, while simultaniously reading the screen to stay updated on what happens. 

Read the "How to Use the bot"-file for more details of how to use the bot. 


