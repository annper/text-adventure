
class InventoryManager(object):
	def __init__(self, *inventoryItems):
		self._inventory = {}
		for item in inventoryItems:
			self._inventory[item.getName()]=item

	def getInventory(self):
		return self._inventory

	# returns an inventory item as dict or object
	# itemName string - name of item to return
	# asArray bool - if True the item will be returned as an array
	# return dict/object - the requested item
	def getItem(self, itemName, asArray=False):
		try:
			itemName.getName()
			thisItem = itemName
		except:
			thisItem = self._inventory[itemName]
		if asArray:
			outItem = {
				'name': thisItem.getName(),
				'type': thisItem.getType(),
				'desc': thisItem.getDesc(),
				'amount': thisItem.getAmount(),
				'equipped': thisItem.isEquipped(),
				'equippable': thisItem.isEquippable()
			}
			try:
				outItem['damage']=thisItem.getDamage()
				outItem['hitChance']=thisItem.hitChance()
			except:
				pass

			if thisItem.getType() is 'armor':
				outItem['defence'] = thisItem.getDefence()
			return outItem
		if not asArray:
			return thisItem

	def addItem(self, inventoryObject):
		try:
			self._inventory[inventoryObject.getName()]=inventoryObject
			return self._inventory
		except:
			return False

	def dropItem(self, inventoryObject):
		try:
			self._inventory.pop(inventoryObject.getName())
			return self._inventory
		except:
			try:
				self._inventory.pop(inventoryObject)
				return self._inventory
			except:
				return False


	# equipps an item / weapon
	# itemName string - name of item to equip
	# return object/bool - item if successful, False if fail
	def equipItem(self, itemName):
		if self._inventory[itemName].getType() is 'armor':
			return False
		
		for key in self._inventory:
			if ( self._inventory[key].getType() is not 'armor' ) and ( key is not itemName ):
				self._inventory[key]._unequip()
			if key is itemName:
				self._inventory[key]._equip()
		return self._inventory[itemName]

	# equipps a piece of armor
	# itemName string - name of armor to equip
	# return bool - True is success, False is fail
	def equipArmor(self, itemName):
		if self._inventory[itemName].getType() is not 'armor':
			return False

		for key in self._inventory:
			if self._inventory[key].getType() is 'armor' and key is not itemName:
				self._inventory[key]._unequip()
			if key is itemName:
				self._inventory[key]._equip()
		return self._inventory[itemName]

	# unequip item, weapon or armor
	# itemName string - name of item to unequip
	# return dict - inventory
	def unequip(self, itemName):
		self._inventory[itemName]._unequip()
		return self._inventory


# superclass for items that can be put in the players backpack, usually weapon or armour
class InventoryItem(object):
	def __init__(self, itemDict):
		self._name = itemDict['name'] if 'name' in itemDict else 'Mysterious item'
		self._type = itemDict['type'] if 'type' in itemDict else 'Unknown'
		self._desc = itemDict['desc'] if 'desc' in itemDict else 'Nondescript'
		self._amount = itemDict['amount'] if 'amount' in itemDict else 1
		self._equipped = False
		self._equippable = False

	# -- getters -- #
	def getAmount(self):
		return self._amount

	def getName(self):
		return self._name

	def getType(self):
		return self._type

	def getDesc(self):
		return self._desc

	def getAmount(self):
		return self._amount

	def isEquipped(self):
		return self._equipped

	def isEquippable(self):
		return self._equippable

	# -- setters -- #
	def setAmount(self, newAmount):
		self._amount = newAmount

	def setName(self, newName):
		self._name = newName

	def setType(self, newType):
		self._type = newType

	def setIsEquippable(self, equippable):
		self._equippable = equippable

	# -- private functions -- #
	def _equip(self):
		self._equipped = True

	def _unequip(self):
		self._equipped = False

	# -- public functions -- #
	def getInfo(self):
		return {
			'name': self._name,
			'type': self._type,
			'desc': self._desc,
			'amount': self._amount,
			'equipped': self._equipped 
		}

# inventoryItem subclass for weapons
class Weapon(InventoryItem):
	def __init__(self, itemDict):
		InventoryItem.__init__(self, itemDict)
		self._type = self._type if self._type is not 'Unknown' else 'weapon'
		self._damage = itemDict['damage'] if 'damage' in itemDict else 10
		self._hitChance = itemDict['hitChance'] if 'hitChance' in itemDict else 50
		self._attackPattern = 'You swing your'
		self._equippable = True

	# -- setters -- #
	def setDamage(self, newDamage):
		self._damage = newDamage

	def setHitChance(self, chance):
		self._hitChance = chance

	def setAttackPattern(self, pattern):
		self._attackPattern = pattern

	# -- getters -- #
	def getDamage(self):
		return self._damage

	def hitChance(self):
		return self._hitChance


	# -- public functions -- #
	def getInfo(self):
		return {
			'name': self._name,
			'type': self._type,
			'damage': self._damage,
			'desc': self._desc,
			'amount': self._amount,
			'equipped': self._equipped 
		}

	# return string to illustrate an attack with the weapon
	# if a weapon is called the and the description ends with the - get ridd of one 'the'
	def Attack(self):
		lastWordInAttackPattern = self._attackPattern.split(' ')[-1]
		firstWordInWeaponName = self._name.split(' ')[0]
		if lastWordInAttackPattern.lower() is 'the' and firstWordInWeaponName.lower() is 'the':
			return self._attackPattern.split(' ')[:-2].join(' ') + ' '+self._name
		return self._attackPattern + ' '+  self._name

# InventoryItem subclass for armours
class Armor(InventoryItem):
	def __init__(self, itemDict):
		InventoryItem.__init__(self, itemDict)
		self._type = 'armor'
		self._defence = itemDict['defence'] if 'defence' in itemDict else 0
		self._equippable = True

	def getDefence(self):
		return self._defence

	def setDefence(self, newDefence):
		self._defence = newDefence

	# -- public functions -- #
	def getInfo(self):
		return {
			'name': self._name,
			'type': self._type,
			'defence': self._damage,
			'desc': self._desc,
			'amount': self._amount,
			'equipped': self._equipped 
		}

#superclass for player character
class Character(object):
	def __init__(self, name):
		self._name = name

		# stats
		self._HEALTH = 100
		self._STRENGTH = 100
		self._MAGIC = 100
		self._health = 100
		self._strength = 100
		self._magic = 100

		# items
		self._defaultWeapon = Weapon({ 'name':'fists' })
		self._equippedItem = self._defaultWeapon
		self._equippedItem._equip()

		self._equippedArmor = Armor({'name':'Prison garbs'})
		self._equippedArmor._equip()

		self._inventory = InventoryManager(self._equippedItem, self._equippedArmor)

		# other
		self._about = 'Unknown background'
		self._className = 'General Class'


	# -- getters -- #
	def getName(self):
		return self._name

	def getHealth(self):
		return self._health

	def getStrength(self):
		return self._strength

	def getMagic(self):
		return self._magic

	def getEquippedItem(self):
		return self._equippedItem

	def getEquippedArmor(self):
		return self._equippedArmor

	def getInventory(self):
		return self._inventory.getInventory()

	def getInventoryManager(self):
		return self._inventory

	def getDefaultWeapon(self):
		return self._defaultWeapon

	def getAbout(self):
		return self._about

	def getClassName(self):
		return self._className

	# -- setters -- #
	def setName(self, newName):
		self._name = newName

	def setHealth(self, health):
		self._health = health

	def setEquippedItem(self, itemName): # name of item or the actual item object
		try:
			itemName = itemName.getName()
		except:
			itemName = itemName

		equippedItem = self._inventory.equipItem(itemName)
		if equippedItem is not False:
			self._equippedItem = equippedItem
		return self._equippedItem

	# equip armor and assign it to the eqipeedarmor attribute
	# itemName Armor/string - 
	def setEquippedArmor(self, itemName):
		try:
			itemName = itemName.getName()
		except:
			itemName = itemName

		equippedArmor = self._inventory.equipArmor(itemName)
		if equippedArmor is not False:
			self._equippedArmor = equippedArmor
		return self._equippedArmor

	def setDefaultWeapon(self, weapon):
		self._defaultWeapon = weapon

	def setAbout(self, background):
		self._about = background

	def setClassName(self, className):
		self._className = className

	# -- private functions -- #

	# -- public functions -- #

	# heal character
	# healPoints int - amount to heal
	# return new health status
	def healDamage(self, healPoints):
		self._health += healPoints
		if self._health > self._HEALTH:
			self._health = self._HEALTH
		return self._health

	# add damage to charcters health
	# damage int - amount of damage to inflict
	# return new health status int
	def takeDamage(self, damage):
		self._health -= damage
		if self._health < 0:
			self._health = 0
		return self._health

	# interface between character and character bound inventory
	def addToInventory(self, inventoryObject):
		return self._inventory.addItem(inventoryObject)

	# interface beteen character and character bound inventory
	# inventoryObject string / object - name of item or acutal item object
	def dropFromInventory(self, inventoryObject):
		try:
			inventoryObject.getName() # check that its an item object
		except:
			inventoryObject = self._inventory.getItem(inventoryObject) # if item name was passed

		# also remove from equipped weapon
		if inventoryObject is self._defaultWeapon:
			return False # default weapon cannot be dropped
		if inventoryObject.isEquipped():
			inventoryObject._unequip()				
			if inventoryObject.getType() == 'armor':
				self._equippedArmor = False
			else:
				self.setEquippedItem(self._defaultWeapon)

		return self._inventory.dropItem(inventoryObject) # returns inventory or False if unsuccessful


	# returns string of 3 main stats
	def getStats(self, asArray=True):
		if asArray:
			return {
				'health': self._health,
				'strength': self._strength,
				'magic': self._magic
			}
		out = 'Health: {}'.format(self._health)
		out += '\nStrength: {}'.format(self._strength)
		out += '\nMagic {}'.format(self._magic)
		return out

# Character subclass
class Dryxie(Character):
	def __init__(self, name):
		Character.__init__(self, name)
		self._STRENGTH = 150
		self._MAGIC = 150
		self._strength = 50
		self._magic = 150

		# default weapon is the crappy wand
		self._defaultWeapon = Weapon({'name':'crappy wand', 'damage':10})
		self._equippedItem = self._defaultWeapon
		self.addToInventory(self._equippedItem)
		self.dropFromInventory('fists')

		self._about = 'Dryxies are a cross between dragon and pixie\nThey wear big wizard hats and carry tiny wands\n'
		self._className = 'Dryxie'

		# Game specific text / public
		self.confirmation = [
			'Let\'s do it!',
			'Hurrah!',
			'Alakazam',
			'I\'m in!',
		]

		

# character subclass
class Stoneskin(Character):
	def __init__(self, name):
		Character.__init__(self, name)
		self._HEALTH = 200
		self._STRENGTH = 150
		self._MAGIC = 50
		self._strength = 150
		self._health = 200
		self._magic = 50

		self._defaultWeapon = Weapon({'name':'fists', 'damage':15})
		self._equippedItem = self._defaultWeapon


		self._about = 'Stonekin are bumbling creatures with skin as hard as rock\nWhatever they may lack they always make up for in strength'
		self._className = 'Stonekin'

		# Game specific text, / public
		self.confirmation = [
			'Argh!',
			'Venture forth!',
			'Let\'s do it!',
			'Off we go!',
		]


# Character subclass
class Grumpling(Character):
	def __init__(self, name):
		Character.__init__(self, name)

		self._about = 'Grumplings are strange bloblike creatures\nThey are extremely grumpy\nThey can change shape into almost anything ... but only when they feel like it!'
		self._className = 'Grumpling'

		# Game specific text / public
		self.confirmation = [
			'Bah!',
			'Humpf',
			'Meh...',
			'(Grumple, grumble ...)'
		]




