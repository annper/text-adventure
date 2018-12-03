
class InputHandler(object):
	def __init__(self):
		self._prompt = '> '
		self._positiveConfirmation = ['1', 'yes', 'yeah']
		self._negativeConfirmation = ['2', 'no', 'nope', 'nah']

	# -- setters && getters -- #
	def setPrompt(self, prompt):
		self._prompt = prompt

	def setPosConfirmation(self, posCofirmation):
		self._positiveConfirmation = posCofirmation

	def setNegConfirmation(self, negConfirmation):
		self._negativeConfirmation = negConfirmation

	def getPosConfirmation(self):
		return self._positiveConfirmation

	def getNegConfirmation(self):
		return self._negativeConfirmation


	# -- public functions -- #

	# takes a users input and validates it too if required
	# needValidation bool - Set to True to validate the user input before returning it
	# returns string - the users validated inpout
	def takeInput(self, needValidation=False):
		this_input = raw_input(self._prompt)
		try:
			isalist = needValidation[0] # makes sure this is a list
			waitingOnValidInput=True
			while waitingOnValidInput:
				if this_input.lower() in needValidation:
					needValidation=False
					return this_input.lower()
				else:
					print this_input + ' is not a valid input, please try again'
					this_input = raw_input(self._prompt)
		except:
			while needValidation:
				if self.confirmInput(this_input) is True:
					needValidation=False
					return this_input
				else:
					print '\nPlease re-enter your answer'
					this_input = raw_input(self._prompt)
			return this_input
		return this_input

	# confirms that a users input was valid
	# input string - the input to validate
	# return function / bool - Returns True if input was valid
	#						 - Returns False if the input vas invalid
	#						 - Returns the function if users confirmation was not recognised
	def confirmInput(self, input):
		print 'You entered ' + input + ', is this correct?'
		print '1. Yes'
		print '2. No, I wish to change it'
		confirmation = raw_input(self._prompt).lower()
		if confirmation in self._positiveConfirmation:
			return True
		elif confirmation in self._negativeConfirmation:
			return False
		else:
			print '------------------------------------'
			print '| Invalid reply, please try again  |'
			print '------------------------------------'
			return self.confirmInput(input)

	# waits for empty input
	#
	# bonusPrompt string - optional additional text
	def awaitInput(self, bonusPromtp=''):
		raw_input(self._prompt + str(bonusPromtp))



