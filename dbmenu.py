from AwesomeText import *
from InputHandler import *
from Game_Tools import *
from Enemy import *
from TA_Game import *


TXT = AwesomeText()
INP = InputHandler()
GAME = TA_Game(INP, TXT)

TXT.setDelayTime(0.01)

# create defaults
player = Grumpling('Nameless')

enemyweapon = Weapon({'name':'spear'})
enemy = Enemy('The Enemy', enemyweapon)


# prints main menu options and returns the players choice
def main_menu():
	TXT.delayPrint('\n----- Main menu -----')

	choices = [
		{ 'P' : 'Create a player character' },
		{ 'E' : 'Create enemy character' },
		{ 'D' : 'Duel' },
		{ 'I' : 'Instructions' },
		{ 'Q': 'Quit' }
	]
	return GAME.PlayerChoice(choices)

# prints chracter creation menu options and returns the players choice
def create_character_menu(player):
	TXT.delayPrint('\n----- Create Character -----')
	choices = [
		{ 'N': 'Name your character' },
		{ 'H': 'Set your characters health' }, # choose class here
		{ 'W': 'Create a weapon for your character' },
		{ 'R': 'Return to the previous menu' }
	]
	return GAME.PlayerChoice(choices)

# prints enemy creation menu options and returns the players choice
def create_enemy_menu(enemy):
	TXT.delayPrint('\n----- Create Enemy -----')
	choices = [
		{ 'N': 'Name the enemy' },
		{ 'H': 'Set the enemy\'s health' },
		{ 'W': 'Create a weapon for the enemy' },
		{ 'G': 'Set when the enemy should give up' },
		{ 'S': 'Set when the enemy should spare your character' },
		{ 'I': 'Set enemy battle introduction' },
		{ 'A': 'Set if the enemy should attack first'},
		{ 'R': 'Return to the previous menu' }

	]
	return GAME.PlayerChoice(choices)

# prints weapons menu options and return the players choice
def create_weapon_menu():
	TXT.delayPrint('\n----- Create Weapon -----')
	choices = [
		{ 'N': 'Name the weapon' },
		{ 'D': 'Set how much damage the weapon will inflict' },
		{ 'C': 'Set the weapons hit chance'},
		{ 'A': 'Set the weapons attack description' },
		{ 'R': 'Return to the previous menu' }
	]
	return GAME.PlayerChoice(choices)


def set_character_name(character):
	TXT.delayPrint('Current name is: ' + character.getName())
	TXT.delayPrint('Please enter a new name for the character:\n')

	INP.setPrompt('Enter name: ')
	name = INP.takeInput(True)
	INP.setPrompt('> ')
	if len(name) > 0:
		character.setName(name)
	TXT.delayPrint('The name has been set to: ' + character.getName())
	return True

def set_weapon_name(character):
	try:		
		TXT.delayPrint('The weapons current name is: ' + character.getEquippedItem().getName())
	except:
		TXT.delayPrint('The weapons current name is: ' + character.getWeapon().getName())
	TXT.delayPrint('Give the weapon a name:\n')

	name = INP.takeInput(True)
	print name
	if len(name) > 0:
		try:
			character.getEquippedItem().setName(name)
			TXT.delayPrint('The weapon is now named: ' + character.getEquippedItem().getName())
		except:
			character.getWeapon().setName(name)
			TXT.delayPrint('The weapon is now named ' + character.getWeapon().getName())
	return True

def set_weapon_damage(character):
	try:
		TXT.delayPrint('Current damage is: ' + str(character.getEquippedItem().getDamage()))
	except:
		TXT.delayPrint('Current damage is: ' + str(character.getWeapon().getDamage()))
	TXT.delayPrint('Set the amount of damage the weapon will do:\n')

	INP.setPrompt('Enter damage: ')
	damage = INP.takeInput([str(x) for x in range(1, 1001)])
	INP.setPrompt('> ')
	try:
		character.getEquippedItem().setDamage(int(damage))
	 	TXT.delayPrint('The weapon damage is now: ' + str(character.getEquippedItem().getDamage()))
	except:
	 	character.getWeapon().setDamage(int(damage))
	 	TXT.delayPrint('The weapon damage is now: ' + str(character.getWeapon().getDamage()))
	return True
	

def set_weapon_hitchance(character):
	try:
		TXT.delayPrint('Current hit chance is: ' + str(character.hitChance()))
	except:
		TXT.delayPrint('Current hit chance is: ' + str(character.getEquippedItem().hitChance()))
	TXT.delayPrint('Enter the likelihood of the weapon hitting:\n')

	INP.setPrompt('Enter hit chance: ')
	hitchance = INP.takeInput([str(x) for x in range(1, 101)])
	INP.setPrompt('> ')
	try:
		character.setHitChance(int(hitchance))
		TXT.delayPrint('The hit chance is now set to: ' + str(character.hitChance()))
	except:
		character.getEquippedItem().setHitChance(int(hitchance))
		TXT.delayPrint('The hit chance is now set to: ' + str(character.getEquippedItem().hitChance()))
	return True

def set_enemy_giveup(enemy):
	TXT.delayPrint('The enemy will currently give up when their health is: ' + str(enemy.givesUpAt()))
	TXT.delayPrint('Enter the health level when the enemy will give up:\n')

	INP.setPrompt('Enter health level: ')
	healthLevel = INP.takeInput([str(x) for x in range(1, enemy.getHealth())])
	INP.setPrompt('> ')
	enemy.setGivesUpAt(healthLevel)
	print enemy.givesUpAt()
	TXT.delayPrint('The enemy will give up when they have: ' + str(enemy.givesUpAt()) + ' health points')
	return True

def set_enemy_battleintro(enemy):
	TXT.delayPrintDialogue([
		'Enter an introduction text for your character', 
		'that will run at the start of the battle\n', 
		'The current intro is: '+enemy.ReadyUp()
	])

	INP.setPrompt('Enter text: ')
	battleintro = INP.takeInput(True)
	INP.setPrompt('> ')
	if len(battleintro) > 0:
		enemy.setReadyUp(battleintro)
	TXT.delayPrint('The enemy will be introduced with: ' + enemy.ReadyUp())
	return True

def set_attackdesc(character):
	TXT.delayPrint('Enter the text that describes an attack with this weapon')
	try:
		TXT.delayPrint('The current attack description: ' + character.Attack() + '\n')
	except:
		TXT.delayPrint('Keep in mind that THE WEAPON NAME WILL BE ADDED TO THE END of the string that is entered here')
		TXT.delayPrint('The current attack description: ' + character.getEquippedItem().Attack() + '\n')

	INP.setPrompt('Your text: ')
	desc = INP.takeInput(True)
	INP.setPrompt('> ')
	if len(desc) > 0:
		try:
			character.getEquippedItem().setAttackPattern(desc)
			TXT.delayPrint('Your character will now attack like this: ' + character.getEquippedItem().Attack())
		except:
			character.setAttackAct(desc)
			TXT.delayPrint('The enemy will now attack like this: ' + character.Attack())
	return True


def set_enemy_attackfirst(enemy):
	TXT.delayPrint('Set if the enemy should attack first:\n')

	choices = [
		{ 'Y': 'Yes, the enemy should attack first' },
		{ 'N': 'No, the enemy should not attack first' }
	]
	resp = GAME.PlayerChoice()
	if resp == 'y':
		enemy.setAttacksFirst(True)
		TXT.delayPrint('This enemy will now attack first')
	if resp == 'n':
		enemy.setAttacksFirst(False)
		TXT.delayPrint('This enemy will wait for you to attack it first')
	return True

def set_enemy_spare(enemy, player):
	TXT.delayPrint('Enter the player\'s health level at which point the enemy will spare them:\n')

	INP.setPrompt('Enter health level: ')
	healthLevel = INP.takeInput([str(x) for x in range(1, player.getHealth())])
	INP.setPrompt('> ')
	enemy.setSpareAt(int(healthLevel))
	TXT.delayPrint('This enemy will spare you when your health is at least: ' + str(enemy.spareAt()) + ' points')
	return True

def set_player_health(player):
	TXT.delayPrint('Your currents health is: ' + str(player.getHealth()) + '\n')

	INP.setPrompt('Enter new health: ')
	newHealth = INP.takeInput([str(x) for x in range(1, 1001)])
	INP.setPrompt('> ')
	player.setHealth(int(newHealth))
	TXT.delayPrint('You health is now: ' + str(player.getHealth()))
	return True

def set_enemy_health(enemy):
	TXT.delayPrint('The enemy\'s current health is: ' + str(enemy.getHealth()) + '\n')

	INP.setPrompt('Enter new health: ')
	newHealth = INP.takeInput([str(x) for x in range(1, 1001)])
	INP.setPrompt('> ')
	enemy.setHealth(int(newHealth))
	TXT.delayPrint('Enemy health is now: ' + str(enemy.getHealth()) + ' points')
	return True

def run_player_options(player, enemy):
	option = create_character_menu(player)
	if option == 'n':
		set_character_name(player)
	if option == 'h':
		set_player_health(player)
	if option == 'w':
		return run_weapon_options(player, enemy, 'player')
	if option == 'r':
		return run(player, enemy)

	return run_player_options(player, enemy)

def run_enemy_options(player, enemy):
	option = create_enemy_menu(enemy)
	if option == 'n':
		set_character_name(enemy)
	if option == 'h':
		set_enemy_health(enemy)
	if option == 'w':
		return run_weapon_options(player, enemy, 'enemy')
	if option == 'g':
		set_enemy_giveup(enemy)
	if option == 's':
		set_enemy_spare(enemy)
	if option == 'i':
		set_enemy_battleintro(enemy)
	if option == 'a':
		set_enemy_attackfirst(enemy)
	if option == 'r':
		return run(player, enemy)

	return run_enemy_options(player, enemy)

def run_weapon_options(player, enemy, characterType):
	character = player if characterType == 'player' else enemy
	option = create_weapon_menu()
	if option == 'n':
		set_weapon_name(character)
	if option == 'd':
		set_weapon_damage(character)
	if option == 'c':
		set_weapon_hitchance(character)
	if option == 'a':
		set_attackdesc(character)
	if option == 'r':
		if characterType == 'player':
			return run_player_options(player, enemy)
		if  characterType == 'enemy':
			return run_enemy_options(player, enemy)

	return run_weapon_options(player, enemy, characterType)


def run(player, enemy):
	choice = main_menu()
	if choice == 'p':
		return run_player_options(player, enemy)
	if choice == 'e':
		return run_enemy_options(player, enemy)
	if choice == 'd':
		GAME.Duel(player, enemy)
	if choice == 'i':
		TXT.delayPrint('To come soon')
	if choice == 'q':
		return exit()

	return run(player, enemy)

def exit():
	TXT.delayPrint('Thanks for playing!')

run(player, enemy)

# TODO: Automatic reset after completed duel:
#       - reset enemy/player health
#		Preview stats in brackets from the menu


