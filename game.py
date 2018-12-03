from AwesomeText import *
from InputHandler import *
from Game_Tools import *
from TA_Game import *
from Enemy import *
from random import randint
import sys

# SETUP
INP = InputHandler()
TXT = AwesomeText()
GAME = TA_Game(INP, TXT)

# check if debug mode activated:
if len(sys.argv) > 1 and sys.argv[1] == 'd':
	DEBUGMODE = True
else:
	DEBUGMODE = False

DEFAULTTIME =  0.005 if DEBUGMODE else 0.02
RERUNTIME = 0.005
TXT.setDelayTime(DEFAULTTIME)
BACKPACK_CHOICE = { 'I': 'Check inventory' }

# MENU OPTIONS
# start menu options
STARTMENU_HEADER = '\n----- Start Menu -----'
STARTMENU_CHOICES = [
	{ 'S': 'Start' },
	{ 'I': 'Instructions' },
	{ 'Q': 'Quit' }
]

#instructions menu options
INSTRUCTION_HEADER = '\n----- Instructions -----'
INSTRUCTION_CHOICES = [
	{ 'H': 'How to play' },
	{ 'A': 'About' },
	{ 'R': 'Return to previous menu' }
]

# start room options
START_ROOM_HEADER = '\n----- Actions -----'
START_ROOM_CHOICES = [
	{ 'L': 'Go through the LEFT door' },
	{ 'R': 'Go through the RIGHT door' },
	BACKPACK_CHOICE
]

# kitchen options
KITCHEN_HEADER = '\n----- Actions -----'
KITCHEN_CHOICES = [
	{ 'A': 'Attempt to take the bone' },
	{ 'F': 'Go through the door at the other end of the room' },
	BACKPACK_CHOICE
]

# armory options
ARMORY_HEADER = '\n----- Actions -----'
ARMORY_CHOICES = [
	{ 'R': 'Open the right door' },
	{ 'F': 'Open the door in front of you' },
	BACKPACK_CHOICE
]

# DIALOGUES
# how to play
HOWTOPLAY = [
	'\n1. Read the text.',
	'2. If the text holds instructions, follow them\n',
	'3. When you see the \'>\' symbol the program is waiting for your input.',
	'4. The program will tell you off when you enter the wrong thing.',
	'5. DON\'T press keys unless you are prompted to do so.\n',
	'6. Have fun! :)'
]

# about
ABOUT = [
	'\nThis is a text adventure game.',
	'It is 50% text and 50% adventure.\n',
	'The aim of the game is to defeat the final boss and escape the mountain.',
	'You do that by making the right decisions for your class,',
	'picking up useful items, and successfully escaping danger.\n',
	'Developed in 2016 by me.'
]

# intro
INTROTIME = 0.05
INTRO_PART_ONE = [
	['\nIn a faraway land, the usually careful trolls have grown bolder and bolder.', INTROTIME],
	['Following their fearsome Troll King they have taken residence in a great mountain.', INTROTIME],
	['Their numbers have grown larger and their magic is seeping out from every crack,', INTROTIME],
	['slowly spreading a sickness across the land.', INTROTIME],
	['...', INTROTIME + 0.1]
]
INTRO_PART_TWO = [
	['You have journeyed to the top of this very mountain.', INTROTIME],
	['There you found a way in.', INTROTIME],
	['Crawling through narrow passages, you wasn\'t able to carry more than the essentials.', INTROTIME],
	['Now it\'s up to you how long you survive among the trolls and goblins.', INTROTIME],
	['Be carfeul! Trolls are tricksy and if you\'re not careful,', INTROTIME],
	['who knows what could happen...', INTROTIME + 0.03]
]

# room 1
STARTROOMTIME = DEFAULTTIME
START_ROOM = [
	[ '\nYou are in a small dark room with a dirt floor.', STARTROOMTIME],
	[ 'In front of you there are two doors with signs on them', STARTROOMTIME ],
	[ 'The left one says \'Kitchen\'.', STARTROOMTIME + 0.02],
	[ 'The right one says \'Armory\',', STARTROOMTIME + 0.02]
]

# kitchen
KITCHENTIME = 0.05
KITCHEN = [
	[ '\nThe kitchen is an absolute mess!', KITCHENTIME ],
	[ 'Dishes are stacked on top of dishes in the most improbable tower formations.', KITCHENTIME ],
	[ 'You feel an overwhelming need to leave this room.', KITCHENTIME ],
	[ '', KITCHENTIME + 0.05 ], # line break
	[ 'To your left there is a dog sleeping loudly, next to a big bone.', KITCHENTIME ],
	[ 'In front of you, at the other side of the room, there is another door.', KITCHENTIME]
]

# armory
ARMORYTIME = 0.05
ARMORY = [
	[ '\nThe room is dark making it hard to see.', ARMORYTIME ],
	[ 'It seems to you as though it\'s completely empty...', ARMORYTIME ],
	[ '', ARMORYTIME + 0.05 ],
	[ 'As your eyes get more adjusted to the light you notice that there are two doors.', ARMORYTIME + 0.03 ],
	[ 'One to your right which looks old and rusty.', ARMORYTIME ],
	[ 'And one in front of you, it has a similar look to the one you came in through', ARMORYTIME]
]


# -- HELPER FUNCTIONS -- #
# set the speed of the text in the rooms, depending on if the player has seent eh text before or not
# revisit bool - True if the reader is returning, false if its first time
# ROOM list - list of text to be printed out in the room
def set_runtime(revisit, ROOM):
	TXT.setDelayTime(RERUNTIME if revisit else DEFAULTTIME)
	if revisit:
		for line in ROOM:
			# diff = line[1] - DEFAULTTIME
			try:
				line[1] = RERUNTIME #+ diff
			except:
				line.append(RERUNTIME)
	return ROOM


# -- ROOMS -- #
# start menu > instructions
def instructions():
	playerChoice = GAME.MenuOptions(INSTRUCTION_CHOICES, INSTRUCTION_HEADER) # h, a, r
	if playerChoice == 'h':
		GAME.Dialogue(HOWTOPLAY)
		return instructions()
	if playerChoice == 'a':
		GAME.Dialogue(ABOUT)
		return instructions()
	if playerChoice == 'r':
		playerChoice = GAME.MenuOptions(STARTMENU_CHOICES, STARTMENU_HEADER) #s, q
		return run(playerChoice)


# first room after character creation and story setup
def first_room(PLAYER, revisit=False):
	global START_ROOM
	START_ROOM = set_runtime(revisit, START_ROOM)
	
	TXT.delayPrintDialogue(START_ROOM)
	playerChoice = GAME.MenuOptions(START_ROOM_CHOICES, START_ROOM_HEADER) # l, r, i
	if playerChoice == 'l': # kitchen
		return kitchen(PLAYER)
	if playerChoice == 'r': # armory
		return armory(PLAYER)
	if playerChoice == 'i': # inventory
		GAME.InventoryMenu(PLAYER, 'the room')
		return first_room(PLAYER, True)

# first_room > armory
# PLAYER Character() - THe players character object
# revisit bool - if player is revisiting or not
def kitchen(PLAYER, revisit=False):
	global KITCHEN
	KITCHEN = set_runtime(revisit, KITCHEN)
	
	TXT.delayPrintDialogue(KITCHEN)
	playerChoice = GAME.MenuOptions(KITCHEN_CHOICES, KITCHEN_HEADER) # a, f, i
	if playerChoice == 'a':
		# take bone
		return kitchen_take_bone(PLAYER)
	if playerChoice == 'f':
		# go to the door
		print 'goes to next room'
	if playerChoice == 'i': # inventory
		GAME.InventoryMenu(PLAYER, 'the kitchen')
		return kitchen(PLAYER, True)

def kitchen_take_bone(PLAYER):
	TXT.setDelayTime(KITCHENTIME)
	charClass = PLAYER.getClassName()

	# set steal success
	if charClass == 'Grumpling':
		success = True if randint(1, 2) == 1 else False
	if charClass == 'Dryxie':
		success = True
	if charClass == 'Stonekin':
		success = False

	if success:
		# take bone
		take_bone = [
			['\nYou inch closer to the dog, one step at a time, careful not to wake it.', KITCHENTIME],
			['You stretch out your arm, reaching for the bone...', KITCHENTIME + 0.05],
			['The dog growls, but doesn\'t wake up!', KITCHENTIME]
		]
		GAME.Dialogue(take_bone) # clears the terminal
		bone = Weapon( { 'name':'bone', 'damage': GAME.StengthBasedDamage(PLAYER, 15) } ) # create the weapon
		PLAYER.addToInventory(bone)
		PLAYER.setEquippedItem(bone)
		statusUpdate = [
			['\n*Status update: You equipped the bone!', KITCHENTIME, Fore.RED], 
			['The bone was added to your inventory', KITCHENTIME, Fore.RED]
		]
		story = [
			[ '' ]
		]
		TXT.delayPrintDialogue(statusUpdate)
		choices = [
			{ 'S': 'Sneak out of here while the dog\'s still sleeping' },
			{ 'I': 'Check inventory' }
		]

		playerChoice = GAME.MenuOptions(choices, '\n----- Well done! -----')
		while playerChoice != 's':
			GAME.InventoryMenu(PLAYER)
			playerChoice = GAME.MenuOptions(choices, '\n----- Well done! -----')
		return True # return prison room

	else:
		# chased out of room
		chased = [
			[ '\nYou get on your tiptoes, trying your best to be silence itself.', KITCHENTIME],
			[ 'You get as close as you dare, then stop and slowly, slowly reach for the bone...', KITCHENTIME + 0.05],
			[ 'Your fingers nudge the tip of the bone when suddenly the dog wakes up!', KITCHENTIME],
			[ '', KITCHENTIME],
			[ 'You turn and run as the dog chases you!', KITCHENTIME],
			[ 'You throw yourself through the door on the other side of the room, just in time!', KITCHENTIME],
			[ 'That\'ll teach you for trying to steal bones from sleeping dogs!', KITCHENTIME]
		]
		GAME.Dialogue(chased)
		return True # return prison room


# first_room > armory
# PLAYER Character() - THe players character object
# revisit bool - if player is revisiting or not
def armory(PLAYER, revisit=False):
	global ARMORY
	ARMORY = set_runtime(revisit, ARMORY)
	
	TXT.delayPrintDialogue(ARMORY)
	playerChoice = GAME.MenuOptions(ARMORY_CHOICES, ARMORY_HEADER) # r, f, i
	if playerChoice == 'r':
		# right door ( has sword )
		print 'open right door'
	if playerChoice == 'f':
		# go to next room
		print 'through to next room'
	if playerChoice == 'i':
		GAME.InventoryMenu(PLAYER, 'the armory')
		return armory(PLAYER, True)

# -- ROOMS SUMMARY -- #
ROOMS = [
	{ '1': 'First room' },
	{ '2': 'Kitchen' },
	{ '3': 'Armory' }
]
# -- SET DEBUG OPTIONS
if DEBUGMODE:
	print 'debugmode active!'
	STARTMENU_CHOICES.extend( ROOMS )
	try:
		DEBUG_PLAYER = GAME.SetDebugPlayer( sys.argv[2] )
	except:
		DEBUG_PLAYER = Grumpling('Grumpling')

	DEBUG_ROOMS = {
		'1': first_room,
		'2': kitchen,
		'3': armory
	}
	print DEBUG_PLAYER


# Runs the game
def run(playerChoice):
	
	# PLAY
	if playerChoice == 's':

		# CREATE CHARACTER
		PLAYER = GAME.CreateCharacter()

		GAME.Dialogue(['\nNow that you are all set up it\'s time to start the adventure'], 'Adventure forth!')

		# INTRO
		GAME.Dialogue(INTRO_PART_ONE, '', False)
		GAME.Dialogue(INTRO_PART_TWO, PLAYER.confirmation[randint(0, len(PLAYER.confirmation)-1)])

		# START ROOM
		PLAYER = first_room(PLAYER)

		# END
		playerChoice = GAME.MenuOptions(STARTMENU_CHOICES, STARTMENU_HEADER) #s, q
		return run(playerChoice)

	# INSTRUCTIONS
	if playerChoice == 'i':
		return instructions()

	# DEBUG ROOMS
	if playerChoice in [ str(n) for n in range(1, len(ROOMS)+1)]:
		DEBUG_ROOMS[playerChoice](DEBUG_PLAYER)

		# END
		playerChoice = GAME.MenuOptions(STARTMENU_CHOICES, STARTMENU_HEADER) #s, q
		return run(playerChoice)

	# QUIT
	else:
		GAME.Quit('\nThanks for playing!')


# START MENU
GAME.ClearTerminal() # clear terminal when starting the game
playerChoice = GAME.MenuOptions(STARTMENU_CHOICES, STARTMENU_HEADER) #s, q

# Run the game
run(playerChoice)








