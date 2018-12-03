class Enemy(object):
	def __init__(self, name, weapon):
		self._name = name
		self._health = 100
		self._weapon = weapon
		self._readyUp = False
		self._attackAct = False
		self._attacksFirst = False
		self._givesUpAt = 0
		self._spareAt = 0
		self._hitChance = 50
		self._defeated = False

	# -- getters -- #
	def getName(self):
		return self._name

	def getHealth(self):
		return self._health

	def getWeapon(self):
		return self._weapon

	def attacksFirst(self):
		return self._attacksFirst

	def getAttackAct(self):
		return self._attackAct

	def getReadyUp(self):
		return self._readyUp

	def givesUpAt(self):
		return self._givesUpAt

	def spareAt(self):
		return self._spareAt

	def hitChance(self):
		return self._hitChance

	def getDefeated(self):
		return self._defeated

	# --  setters -- #
	def setName(self, name):
		self._name = name

	def setHealth(self, heath):
		self._health = heath

	def setWeapon(self, weapon):
		self._weapon = weapon

	def setAttackAct(self, text):
		self._attackAct = text

	def setAttacksFirst(self, attacksFirst):
		self._attacksFirst = attacksFirst

	def setReadyUp(self, ready):
		self._readyUp = ready

	def setGivesUpAt(self, health):
		self._givesUpAt = health

	def setSpareAt(self, spare):
		self._spareAt = spare

	def setHitChance(self, hitchance):
		self._hitChance = hitchance

	def setDefeated(self, defeated):
		self._defeated = defeated

	# -- public functions -- #
	def Attack(self):
		try:
			return '' + self._attackAct + ''
		except:
			return self._name + ' swings their ' + self._weapon.getName()

	def ReadyUp(self):
		try:
			return ''+self._readyUp+''
		except:
			return self._name + ' approaches'

	# for taking damage in battle
	# use this rather than setDamage to ensure that damage is never less than 0
	def takeDamage(self, damage):
		self._health -= damage
		if self._health < 0:
			self._health = 0
		return self._health


