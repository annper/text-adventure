from Game_Tools import *
import copy
import time
import os
from colorama import init, Fore, Back
from random import randint

class TA_Game(object):
	def __init__(self, inputHandler, awesomeText):
		self._inputHandler = inputHandler
		self._awesomeText = awesomeText
		
		self._optionColor = Fore.CYAN
		self._headerColor = Fore.GREEN

		init()

		self._names = [
			'Hugo',
			'Finn',
			'Lisa',
			'Nolte',
			'Nark',
			'Gunnar',
			'Inge',
			'Berg',
			'Strom',
			'Lurv',
			'Lele',
			'Barock',
			'Hillie',
			'Tussle',
			'Bengt',
			'Gran',
			'Mars',
			'Yngve',
			'Sylve',
			'Alk',
			'Eva',
			'Lasse',
			'Lort',
			'Mort',
			'Kimmel',
			'Malte',
			'Locke',
			'Sigurd',
			'Mans',
			'Tove',
			'Blimp',
			'Karsk',
			'Bella',
			'Kotte',
			'Nalle',
			'Bork',
			'Ture',
			'Lisp',
			'Kork',
			'Nora',
			'Palle'

		]

	# -- getters -- #


	# -- setters -- #


	# -- private functions -- #
	# walls off the text to make it easier to read
	# character string - character wall off with
	# amount int - number of times to write out the character
	# breakspace bool - Indicates if the wall should finish with a breakspace or not
	def _wall(self, character, amount, breakspace=False):
		print character * amount
		if breakspace:
			print ''

	# same as wall but prints the wall dynamically using AwesomeText.delayPrint(string)
	def _wallDelay(self, character, amount, breakspace=False):
		wall = character * amount
		self._awesomeText.delayPrint(wall)
		if breakspace:
			print ''

	# capitalises the first letter in a string and returns it
	def _upperFirst(self, string):
		if len(string) > 0:
			return string[0].upper() + string[1:]
		else: 
			return string

	# takes a dict with one key, value pair and returns them as a tuple
	# return tuple - (key, value)
	# used in self.PlayerChoice()
	def _getDictItem(self, dictionary):
		for key, value in dictionary.items():
			return (key, value)

	# shows the current health status for a character ( enemy or player char )
	# used in self.Dueling()
	def _showHealthStatus(self, health, char):
		status = 'Your health is now ' + str(health) if char is 'player' else 'Their health is now ' + str(health)
		allText = [
			'',
			'*' * 15,
			status,
			'*' * 15
		]
		self._awesomeText.delayPrintDialogue(allText)

	# play out the enemy attack
	# Player Character() - the player's character
	# Enemy Enemy() - enemy thats attacking the player
	# return none - when ending the functions continues in _dueling()
	def _enemyAttack(self, Player, Enemy):
		self._wallDelay('-', 15, True)
		time.sleep(1)
		self._awesomeText.delayPrint(Enemy.Attack())
		print ''
		time.sleep(1.5)

		hit = randint(1, 100)
		if hit <= Enemy.hitChance():
			self._awesomeText.delayPrint( 'They hit!' )
			Player.takeDamage( Enemy.getWeapon().getDamage() )
			self._awesomeText.delayPrint( 'You took ' + str(Enemy.getWeapon().getDamage()) + ' points of damage' )
			self._showHealthStatus(Player.getHealth(), 'player')
		else:
			self._awesomeText.delayPrint( 'They miss!' )
			self._wall('', 1)

		# time.sleep(1.5)

	# play out player attack
	# Player Character() - the players character
	# Enemy Enemy() - enemy that the player is attacking
	# return none - when ending the function continues in _dueling()
	def _playerAttack(self, Player, Enemy):
		self._wall('-', 15, True)
		time.sleep(1)
		playerWeapon = Player.getEquippedItem() if Player.getEquippedItem().getType() is 'weapon' else Player.getDefaultWeapon()
		self._inputHandler.awaitInput('Attack!')
		self._awesomeText.delayPrint(playerWeapon.Attack())
		print ''
		time.sleep(1.5)

		hit = randint(0, 100)
		if hit <= playerWeapon.hitChance():
			self._awesomeText.delayPrint( 'It\'s a hit!' )
			Enemy.takeDamage( playerWeapon.getDamage() )
			self._awesomeText.delayPrint( Enemy.getName() + ' took ' + str(playerWeapon.getDamage()) + ' points of damage' )
			self._showHealthStatus(Enemy.getHealth(), 'enemy')
			
		else:
			self._awesomeText.delayPrint( 'You missed!' )
			self._wall('', 1)

		# time.sleep(1.5)


	# recursive function where player and enemy take turn to attack one another
	# recursion ends when enemy or player gives up or dies	
	def _dueling(self, Player, Enemy, EnemyAttack=False):
		if Enemy.getHealth() <= Enemy.givesUpAt():
			return self._enemyDefeat(Player, Enemy)

		if Player.getHealth() <= Enemy.spareAt():
			return self._playerDefeat(Player, Enemy)

		if EnemyAttack:
			self._enemyAttack(Player, Enemy)
			return self._dueling(Player, Enemy)
		else:
			self._playerAttack(Player, Enemy)
			return self._dueling(Player, Enemy, True)

	# executed when the player defeats the enemy or it gives up
	def _enemyDefeat(self, Player, Enemy):
		Enemy.setDefeated(True)
		if Enemy.getHealth() is 0:
			return ( 'You defeated ' + Enemy.getName() +'!', 'dead' )
		elif Enemy.getHealth() <= Enemy.givesUpAt():
			return ( Enemy.getName() + ' gives up...', 'yield' )

	# executed when the enemy defeats the player or spares them
	def _playerDefeat(self, Player, Enemy):
		if Player.getHealth() is 0:
			return ( 'You was killed by '+Enemy.getName(), 'killed' )
		elif Player.getHealth() <= Enemy.spareAt():
			return ( Enemy.getName() + ' has decided to spare you...', 'spare' )

	# prints the menu for choosing a class
	# returns the players choice
	def _chooseClassMenu(self):
		choices = [
			{ 'D': 'Dryxie' },
			{ 'G': 'Grumpling' },
			{ 'S': 'Stoneskin' },
			{ 'R': 'Randomise a class' }
		]
		playerChoice = self.MenuOptions(choices, '\n----- Pick a class ----')
		return self._setClass(playerChoice)

	# give the option to create a class / randomise a class / go back 
	# classType char - letter referencing the character class to create
	# returns Character() - Returns the created character object OR redirects back to pick a class menu
	def _setClass(self, classType):
		if classType == 'r': # randomise a class
			randomClass = randint(1, 3)
			classType = 'd' if randomClass == 1 else 'g' if randomClass == 2 else 's'

		if classType == 'd':
			playerCharacter = Dryxie('unnamed')
		if classType == 'g':
			playerCharacter = Grumpling('unnamed')
		if classType == 's':
			playerCharacter = Stoneskin('unnamed')
		
		self._awesomeText.delayPrint('\n----- ' + playerCharacter.getClassName() + ' -----', None, self._headerColor)
		self._awesomeText.delayPrint(playerCharacter.getAbout())
		self._wall('', 0)

		choices = [
			{ 'P': 'Pick class' },
			{ 'R': 'Return to class options'}
		]
		try:
			if randomClass in range(1, 4):
				choices.append( { 'G': 'Generate new!' } )
		except:
			pass

		playerChoice = self.PlayerChoice(choices)
		if playerChoice == 'r':
			return self._chooseClassMenu()
		if playerChoice == 'p':
			return playerCharacter
		if playerChoice == 'g':
			return self._setClass('r')

	# shows menu for how to set a name, pick between randomise or type in own
	# playerCharacter Character() - the players character object
	# returns the chosen name
	def _nameCharacterMenu(self, playerCharacter):
		choices = [
			{ 'T': 'Type a name' },
			{ 'R': 'Randomise a name' }
		]
		playerChoice = self.MenuOptions(choices, '\n----- Name your ' + playerCharacter.getClassName() + ' -----')
		if playerChoice == 't':
			return self._typeCharacterName(playerCharacter)
		if playerChoice == 'r':
			return self._randomiseCharacterName(playerCharacter)

	# choses a random character name, an shows menu for accepting or trying again
	# playerCharacter Character() - the players character object
	# returns function or name
	def _randomiseCharacterName(self, playerCharacter):
		self._awesomeText.delayPrint('\n----- Randomise character name -----', None, self._headerColor)
		randName = self._names[randint(0, len(self._names)-1)]
		choices = [
			{ 'A': 'Accept this as your character name' },
			{ 'R': 'Randomise a new name' },
			{ 'T': 'Type in a new name' }
		]
		playerChoice = self.MenuOptions(choices, '\n-- Your name is ' + randName + ' --')
		if playerChoice == 'r':
			return self._randomiseCharacterName(playerCharacter)
		if playerChoice == 't':
			return self._typeCharacterName(playerCharacter)
		if playerChoice == 'a':
			return randName

	# lets user type in a char name, and then accept or redo it
	# playerCharacter Character() - the players chosen character object
	# returns function or name
	def _typeCharacterName(self, playerCharacter):
		self._awesomeText.delayPrint('\n----- Type in a name -----', None, self._headerColor)
		playerName = self._inputHandler.takeInput()
		self.ClearTerminal()
		choices = [
			{ 'A': 'Accept this as your character name' },
			{ 'T': 'Type in a new name' },
			{ 'R': 'Randomise a new name'}
		]
		playerChoice = self.MenuOptions(choices, '\n-- Your name is ' + playerName + ' --')
		if playerChoice == 't':
			return self._typeCharacterName(playerCharacter)
		if playerChoice == 'r':
			return self._randomiseCharacterName(playerCharacter)
		if playerChoice == 'a':
			return playerName

	# shows the players inventory and options to inspect them
	# ITEM dict - item dictionary of the inventoryItem being dropped
	# PLAYER Character() - The players character object
	# return InventoryMenu() 
	def _inventoryItemMenu(self, ITEM, PLAYER, previousMenu):
		# show item info
		itemDesc = [
			'Item: ' + self._upperFirst(ITEM['name']) + ' (' + ITEM['type'] + ')',
			'About: ' + self._upperFirst(ITEM['desc'])
			#'Amount: ' + str(ITEM['amount']),
		]
		if 'damage' in ITEM:
			itemDesc.append( 'Damage: ' + str(ITEM['damage']) + ' points' )
		if 'hitChance' in ITEM:
			itemDesc.append( 'Chance to hit: ' + str(ITEM['hitChance']) + '%' )
		if 'defence' in ITEM:
			itemDesc.append( 'Defence: ' + str(ITEM['defence']) + ' points' )
		if ITEM['equipped']:
			itemDesc.append( '* EQUIPPED *' )
		itemDesc.append('')

		self._awesomeText.delayPrint('\n-- ' + self._upperFirst(ITEM['name']) + ' --', None, self._headerColor)
		self._awesomeText.delayPrintDialogue(itemDesc)

		# show item options
		# D: Drop item
		# E: Equip item
		# R: Return to inventory
		choices = [
			{ 'D': 'Drop item (This cannot be undone)' },
		]
		if (ITEM['equipped'] == False) and ITEM['equippable'] == True:
			choices.append( { 'E' : 'Equip ' + ITEM['name'] } )
		choices.append( { 'R': 'Return to inventory' } )

		playerChoice = self.MenuOptions(choices)
		if playerChoice == 'r': # return to InventoryMenu()
			return self.InventoryMenu(PLAYER, previousMenu) 
		
		if playerChoice == 'd': # drop item
			return self._dropItem(ITEM, PLAYER, previousMenu)
		
		if playerChoice == 'e': # equip item
			return self._equipItem(ITEM, PLAYER, previousMenu)

	# drop item from inventory, unless its a default
	# ITEM dict - item dictionary of the inventoryItem being dropped
	# PLAYER Character() - The players character object
	# return self.InventoryMenu(ITEM, PLAYER)
	def _dropItem(self, ITEM, PLAYER, previousMenu):
		options = [
			{ 'Y': 'Yes, I want to drop this item' }, 
			{ 'N': 'No I want to keep it' }
		]
		confirmDrop = self.MenuOptions(options, '\n----- Please confirm -----')
		if confirmDrop == 'y':
			INVENTORY = PLAYER.dropFromInventory(ITEM['name'])
			if INVENTORY != False: # can't drop default weapons
				self._awesomeText.delayPrint('\nYou dropped ' + self._upperFirst(ITEM['name']))
				self._inputHandler.awaitInput('OK')
				return self.InventoryMenu(PLAYER, previousMenu)
			else:
				self._awesomeText.delayPrint('\nYou are not allowed to drop ' + self._upperFirst(ITEM['name']))
				self._inputHandler.awaitInput('OK')
				self.ClearTerminal()
				return self._inventoryItemMenu(ITEM, PLAYER, previousMenu)
		if confirmDrop == 'n':
			return self._inventoryItemMenu(ITEM, PLAYER, previousMenu)

	# equip an item from the players inventory
	# ITEM dict - item dictionary of the inventoryItem being equipped
	# PLAYER Character() - The players character object
	# return self._inventoryItemMenu(ITEM, PLAYER)
	def _equipItem(self, ITEM, PLAYER, previousMenu):
		if ITEM['type'] == 'armor':
			equippedItem = PLAYER.setEquippedArmor(ITEM['name'])
		else:
			equippedItem = PLAYER.setEquippedItem(ITEM['name'])
		asArray=True
		ITEM = PLAYER.getInventoryManager().getItem(equippedItem, asArray)
		self._awesomeText.delayPrint('\nYou have equipped ' + self._upperFirst(ITEM['name']))
		return self._inventoryItemMenu(ITEM, PLAYER, previousMenu)
			

	# -- public functions -- #

	# write out dialogue and wait for player to hit enter before coninuing
	# dialogueList list - list of strings or lists of [str, num] //see AwesomeText
	# bonusPrompt string - extra bit of prompt for user guidance e.g OK 
	def Dialogue(self, dialogueList, bonusPrompt='', clearTerminal=True):
		self._awesomeText.delayPrintDialogue(dialogueList)
		self._inputHandler.awaitInput(bonusPrompt)
		if clearTerminal:
			self.ClearTerminal()
		return True

	# write out player choices and expected input
	# choices list of dicts [ {'char':'string'} ] - expected input, and explanation of what will happen
	def PlayerChoice(self, choices):
		# choices_copy = [ {'hi':'bye'}, {'hej':'da'} ]
		choices_copy = copy.deepcopy(choices)
		validInputs=[]
		for choice in choices:
			returnValue , textValue = self._getDictItem(choice)
			validInputs.append(returnValue.lower())
			self._awesomeText.delayPrint(self._optionColor + returnValue +  Fore.RESET + ': ' + textValue)
			returnValue = choice
		playerChoice = self._inputHandler.takeInput().lower()
		if playerChoice in validInputs:
			self.ClearTerminal()
			return playerChoice
		else:
			print '//'
			self._awesomeText.delayPrint('// Invalid input, please try again')
			self._awesomeText.delayPrint('// Valid input are: ' + (', '.join([ x.upper() for x in validInputs ])))
			print '//'
			return self.PlayerChoice(choices_copy)

	# duel an enemy
	# Character - a player character
	# Enemy - an enemy character
	def Duel(self, Player, Enemy):
		info = [
			'You are about to duel ' + Enemy.getName(),
			'Read the instructions or proceed to the fight'
		]
		instructions = [
			'1. Attack by clicking Enter on your turn',
			'2. Fight to the death',
			'3. Try not to die first'
		]
		self._awesomeText.delayPrintDialogue(info)
		choices = [ 
			{ 'I': 'Instructions' },
			{ 'S': 'Start the duel' }
		]
		playerChoice = self.PlayerChoice(choices)

		if playerChoice == 'i':
			self.Dialogue(instructions, 'Got it!')

		print '-' * 15
		self.Dialogue([Enemy.ReadyUp()])
		
		# returns tuple ( message, endOfBattleInfo )
		# endOfBattleInfo can have 1 of 4 values:
		#  dead - You WON and the Enemy died
		#  yield - You WON and the Enemy yielded
		#  killed - You LOST and the Enemy killed you
		#  spare - You LOST and the Enemy spared you
		battleEnd = self._dueling(Player, Enemy, Enemy.attacksFirst())
		endMessage, status = battleEnd
		
		# write out the end message and wait for confirmation
		# return the end battle status
		self._wall('', 1)
		self._awesomeText.delayPrintDialogue([endMessage])
		return status

	# prints out a menu with a header
	# choices list - A list of dicts, one dict for each menu options e.g [ { 'S': 'Start' } ]
	# header string - a header that will appear above the menu
	def MenuOptions(self, choices, header=''):
		if len(header) > 0:
			self._awesomeText.delayPrint(header, None, self._headerColor)
		return self.PlayerChoice(choices)

	# add optional end message before quitting the game
	def Quit(self, endMessage=''):
		if len(endMessage):
			self._awesomeText.delayPrint(endMessage)
		else: pass

	
	# Takes user through the stages of setting up a character
	# returns Character() - The players chosen character (class + name)
	def CreateCharacter(self):
		newDelayTime=0.02
		oldDelayTime=self._awesomeText.getDelayTime()
		# 1. type out intro
		intro=[
			'\nThe first step on your way to becoming a great adventurer is to',
			'create your character! Let\'s go!'
		]
		self.Dialogue(intro)

		# 2. Pick class
		self._awesomeText.setDelayTime( newDelayTime )
		playerCharacter =  self._chooseClassMenu()
		self._awesomeText.setDelayTime(oldDelayTime)
		self.Dialogue(['\nMagnificent! You are now a ' + playerCharacter.getClassName() + '!'])

		# 3. Name character
		self._awesomeText.setDelayTime( newDelayTime )
		playerName = self._nameCharacterMenu(playerCharacter)
		playerCharacter.setName(playerName)
		self._awesomeText.setDelayTime(oldDelayTime)
		self.Dialogue(['\nFantastic! Your ' + playerCharacter.getClassName() + '\'s name is now ' + playerName])

		# 4. return the created character
		return playerCharacter

	# show menu of all available inventory items
	# PLAYER Character() - The players character object
	# return bool / funtion - True if player is done with the menu
	#						- self._inventoryItemMenu if player wants to look at an item
	def InventoryMenu(self, PLAYER, previousMenu='previous menu'):
		oldDelayTime = self._awesomeText.getDelayTime()
		self._awesomeText.setDelayTime(0.02)
		INVENTORY = PLAYER.getInventory()
		INVENTORY_MANAGER = PLAYER.getInventoryManager()
		choices=[]
		choicesDict={}
		i=0
		for itemName in INVENTORY:
			i += 1
			equipped = INVENTORY[itemName].isEquipped()
			choices.append( { str(i) : self._upperFirst(itemName) + ( ' ( equipped )' if equipped else '' )} )
			choicesDict[ str(i) ] = itemName
		choices.append( { 'R': 'Return to ' + previousMenu } )
		playerChoice = self.MenuOptions(choices, '\n----- Inventory -----')
		if playerChoice == 'r':
			# return to prev menu
			self._awesomeText.setDelayTime(oldDelayTime)
			return True
		else:
			# return item specific menu
			asArray=True
			ITEM = INVENTORY_MANAGER.getItem( choicesDict[playerChoice], asArray )
			return self._inventoryItemMenu(ITEM, PLAYER, previousMenu)

	# Clears all the contents in the current scope of the open terminal
	def ClearTerminal(self):
		os.system('cls' if os.name == 'nt' else 'clear')

	# Created a player character for use in debug mode
	# characterChoice is the second argument from the command line when running the game (sys.argv[2])
	# return Character() -  a character to use when debugging to skip going through character creation each time
	def SetDebugPlayer(self, characterChoice):
		if characterChoice == ('g' or 'grumpling'):
			return Grumpling('Grumpling')
		if characterChoice == ('d' or 'dryxie'):
			return Dryxie('Dryxie')
		if characterChoice == ('s' or 'stonekin'):
			return Stoneskin('Stonekin')
		else:
			return Grumpling('Grumpling')

	# used to set the damage of a weapon based on player stat
	# PLAYER Character() - The players character object
	# baseDamage - the weapons default damage
	# return int - the weapons actual damage on once the characters strength has been taken into account
	def StengthBasedDamage(self, PLAYER, baseDamage):
		return int((PLAYER.getStrength() / 100.0) * baseDamage)

	# used to set the damage of a weapon based on player stat
	# PLAYER Character() - The players character object
	# baseDamage - the weapons default damage
	# return int - the weapons actual damage on once the characters magic has been taken into account
	def MagicBasedDamage(seld, PLAYER, baseDamage):
		return int((PLAYER.getMagic() / 100.0) * baseDamage)













	







		








		





	