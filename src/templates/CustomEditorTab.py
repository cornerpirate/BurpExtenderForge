from burp import IBurpExtender
from burp import IMessageEditorTabFactory
from burp import IMessageEditorTab
from burp import IParameter

# Originally from:
# https://github.com/PortSwigger/example-custom-editor-tab/tree/master/python
# Modified to suit
class BurpExtender(IBurpExtender, IMessageEditorTabFactory):
    
    extendername = "New Custom Editor" # Alter this as it becomes the name of your extension
    #
    # implement IBurpExtender
    #
    
    def	registerExtenderCallbacks(self, callbacks):
        # keep a reference to our callbacks object
        self._callbacks = callbacks
        
        # obtain an extension helpers object
        self._helpers = callbacks.getHelpers()
        
        # set our extension name
        callbacks.setExtensionName(self.extendername)
        
        # register ourselves as a message editor tab factory
        callbacks.registerMessageEditorTabFactory(self)
        
    # 
    # implement IMessageEditorTabFactory
    #
    
    def createNewInstance(self, controller, editable):
        # create a new instance of our custom editor tab
        return Base64InputTab(self, controller, editable)
        
# 
# class implementing IMessageEditorTab
#

'''
This entire class is part of PortSwigger's tutorial.
You would need to learn what this does and alter it 
to server your needs.
'''
class Base64InputTab(IMessageEditorTab):

    # Whatever you set this to it will be the name of your tab.
    extendername = "Base64InputTab"

    def __init__(self, extender, controller, editable):
        self._extender = extender
        self._editable = editable
        
        # create an instance of Burp's text editor, to display our deserialized data
        self._txtInput = extender._callbacks.createTextEditor()
        self._txtInput.setEditable(editable)
        
    #
    # implement IMessageEditorTab
    #

    '''
    When you change this class make sure getTabCaption remains like this.
    This way extenderforge's plugin names are maintained.
    '''
    def getTabCaption(self):
        return self.extendername
        
    def getUiComponent(self):
        return self._txtInput.getComponent()
    
    '''
    Burp Decides when to display a custom editor based on this.
    Returning true means your custom tab is displayed in proxy history
    and when trapping requests.
    In this case if the request has a parameter called "data" it will display
    the tab.
    '''    
    def isEnabled(self, content, isRequest):
        # enable this tab for requests containing a data parameter
        return isRequest and not self._extender._helpers.getRequestParameter(content, "data") is None
        
    def setMessage(self, content, isRequest):
        if content is None:
            # clear our display
            self._txtInput.setText(None)
            self._txtInput.setEditable(False)
        
        else:
            # retrieve the data parameter
            parameter = self._extender._helpers.getRequestParameter(content, "data")
            
            # deserialize the parameter value
            self._txtInput.setText(self._extender._helpers.base64Decode(self._extender._helpers.urlDecode(parameter.getValue())))
            self._txtInput.setEditable(self._editable)
        
        # remember the displayed content
        self._currentMessage = content
    
    def getMessage(self):
        # determine whether the user modified the deserialized data
        if self._txtInput.isTextModified():
            # reserialize the data
            text = self._txtInput.getText()
            input = self._extender._helpers.urlEncode(self._extender._helpers.base64Encode(text))
            
            # update the request with the new parameter value
            return self._extender._helpers.updateParameter(self._currentMessage, self._extender._helpers.buildParameter("data", input, IParameter.PARAM_BODY))
            
        else:
            return self._currentMessage
    
    def isModified(self):
        return self._txtInput.isTextModified()
    
    def getSelectedData(self):
        return self._txtInput.getSelectedText()
