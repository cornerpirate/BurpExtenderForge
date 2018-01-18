from burp import IBurpExtender
from burp import IIntruderPayloadProcessor
from array import array

class BurpExtender(IBurpExtender, IIntruderPayloadProcessor):

    extendername = "New Encoder" # Alter this as it becomes the name of your extension

    #
    # implement IBurpExtender
    #
    def registerExtenderCallbacks(self, callbacks):
      # obtain an extension helpers object
      self._helpers = callbacks.getHelpers()
      # set our extension name
      callbacks.setExtensionName(self.extendername)
      #register ourselves as an Intruder payload processor
      callbacks.registerIntruderPayloadProcessor(self)

    #
    # implement IIntruderPayloadProcessor
    #
    def getProcessorName(self):
        return self.extendername

    '''
    Parameters:
	currentPayload - The value of the payload to be processed.
	originalPayload - The value of the original payload prior to processing by any already-applied processing rules.
	baseValue - The base value of the payload position, which will be replaced with the current payload.
    Returns:
        The value of the processed payload. This may be null to indicate that the current payload should be skipped, and the attack will move directly to the next payload.
    '''
    def processPayload(self, currentPayload, originalPayload, baseValue):
        # Original arguments are byte arrays.
        # Convert to string as shown.
        currentPayloadString = currentPayload.tostring() 
        originalPayloadString = originalPayload.tostring()
        baseValueString = baseValue.tostring()

        # Simply convert payload to uppercase
        answer = currentPayloadString.upper() 

        # return needs a byte array again. If you have a string use "stringTobBytes"
        return self._helpers.stringToBytes(answer)