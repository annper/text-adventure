import time
import sys
from colorama import init, Fore, Back, Style

# Does cool things with strings
class AwesomeText(object):

	def __init__(self, text=''):
		self._text = text
		self._delayTime = 0.1
		self._endLine = '\n'
		self._textColor = Fore.WHITE
		self._coloredTextSetting = False
		self._constructPrintText()
		init()
		
		
	# -- getters & setters -- #
	def getDelayTime(self):
		return self._delayTime

	def getText(self):
		return self._text

	def getEndLine(self):
		return repr(self._endLine)

	def getTextColor(self):
		return self._textColor

	def getColoredTextSetting(self):
		return self._coloredTextSetting

	def setDelayTime(self, delayTime):
		self._delayTime = delayTime

	def setText(self, newText):
		self._text = newText
		self._constructPrintText()

	def setEndLine(self, endLineChar):
		self._endLine = endLineChar
		self._constructPrintText()

	def setTextColor(self, color):
		self._textColor = color

	def setColoredTextSetting(self, setting):
		self._constructPrintText()
		self._coloredTextSetting = setting

	# -- private functions -- #
	def _constructPrintText(self):
		if self._coloredTextSetting == True:
		 	self._printText = self._textColor + self._text + self._endLine
		else:
			self._printText = self._text + self._endLine

	#  -- public functions -- #
	
	# print text one char at a time
	# 
	# float/int/str tempDelayTimeOrText - Optional delay time or text only to be used for one instance
	# float/int tempDelayTime - Optional delay time for one instance
	def delayPrint(self, tempDelayTimeOrText=None, tempDelayTime=None, color=False):
		delayTime = self._delayTime
		textToPrint = self._printText

		# assign correct variable values
		if tempDelayTimeOrText is not None and tempDelayTime is None:
			if isinstance(tempDelayTimeOrText, float) or isinstance(tempDelayTimeOrText, int):
				delayTime = tempDelayTimeOrText
			elif isinstance(tempDelayTimeOrText, str):
				textToPrint = tempDelayTimeOrText + self._endLine
		elif tempDelayTimeOrText is not None and tempDelayTime is not None:
			textToPrint = tempDelayTimeOrText + self._endLine
			delayTime = tempDelayTime

		if color is not False:
			textToPrint = color + textToPrint
		else:
			textToPrint = ( self._textColor if self._coloredTextSetting else Fore.RESET ) + textToPrint
		

		# do the printing
		if len(textToPrint) > 0:
			for c in textToPrint:
				sys.stdout.write( '%s' % c )
				sys.stdout.flush()
				time.sleep(delayTime)
		else:
			pass

	# print out several lines of text, one char at a time
	#
	# dialogueList list[string] / list[list[string, num]] 
	#				-  one string for each dialogue line
	#				- string dialogue line, optional num for print delay speed
	def delayPrintDialogue(self, dialogueList):
		for dialogue in dialogueList:
			if isinstance(dialogue, list):
				color = dialogue[2] if len(dialogue) >= 3 else self._textColor if self._coloredTextSetting else Fore.RESET 
				self.delayPrint(dialogue[0], dialogue[1] if len(dialogue) > 1 else self._delayTime, color)
			else:
				self.delayPrint(dialogue)
        	
	


