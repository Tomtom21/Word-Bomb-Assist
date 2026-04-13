<div align="center" style="text-align: center;">
<h1>Word Bomb Assist</h1>
<p>
A tool to "assist" in winning Word Bomb matches on Roblox
</p>
</div>

What is Word Bomb?
---
[Word Bomb](https://www.roblox.com/games/2653064683/Word-Bomb) is a Roblox game where the each player is given a sequence of 1-3 letters, and must come up with a word that contains the sequence of letters in a limited amount of time. If the player fails to come up with and type in an appropriate word, they lose a life. The last remaining player wins. A couple notes about this game:

 - The sequence of letters can be found anywhere in the word. It just has to be in the presented order.
 - If another player has already typed a word, it cannot be used again.
 - The sequence combinations presented to the players generally increase in difficulty as time goes on. 

What does this tool do?
---
Word Bomb Assist analyzes your screen using OCR models to determine the presented character sequence in the game and give the user word options that may work for the sequence. These suggested words can be used in the event the user doesn't know a word they could use.

How to use
---

 1. Install the required libraries
	 - `pip install -r requirements.txt`
 2. Run the script (no arguments needed)
	 - `python3 main.py`

The script will automatically start scanning your main monitor and presenting any suggestions it sees in the terminal. 

Please keep in mind
---
 - **This tool does not, and is not supposed to provide keyboard input or type any words in for you.**
	 - In my time working on this, I didn't find any popular or trustworthy methods of performing keyboard input on behalf of the user.
 - **The list of words presented to the user does not filter out already used words.**
	 - This script is not aware of whether a word was accepted by the game or not, so it does not keep track of which words have been truly used. This may be possible by voiding any typed word, but that was not a priority during implementation.
- **The OCR model can sometimes fail to detect characters properly.**
	- The OCR model will sometimes read a character incorrectly, so it is possible for the word suggestions to also  be incorrect. I've attempted to negate this by altering the input image, however the issue still somewhat remains. Take suggestions with a grain of salt.
