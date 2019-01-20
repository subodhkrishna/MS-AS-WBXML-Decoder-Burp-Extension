from burp import IBurpExtender
from burp import IHttpListener
from burp import IMessageEditorTabFactory
from burp import IMessageEditorTab
from java.io import PrintWriter
from PyWBXMLDecoder import ASCommandResponse


class BurpExtender(IBurpExtender, IHttpListener, IMessageEditorTabFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("WBXML Decoder")
        self._stdout = PrintWriter(callbacks.getStdout(), True)
        callbacks.registerHttpListener(self)
        callbacks.registerMessageEditorTabFactory(self)

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        pass
    # if messageIsRequest:
    # use for debugging
    # request = messageInfo.getRequest()
    # req = self._helpers.analyzeRequest(request)
    # req_headers = req.getHeaders()
    # for header in req_headers:
    #   if "wbxml" in header:
    #       #self._stdout.println(header)
    # self._stdout.println("Request offset = " + str(req.getBodyOffset()))
    # request_body = request[req.getBodyOffset():]
    # decoded_wbxml = ASCommandResponse.ASCommandResponse(request_body)
    # self._stdout.println(self._helpers.bytesToString(request_body))
    # self._stdout.println(decoded_wbxml.xmlString)
    # self._stdout.println("")

    def createNewInstance(self, controller, editable):
        # create a new instance of our custom editor tab
        return WBXMLTab(self, controller, editable)


#
# class implementing IMessageEditorTab
#

class WBXMLTab(IMessageEditorTab):
    def __init__(self, extender, controller, editable):
        self._extender = extender
        self._editable = editable
        self._controller = controller
        self._stdout = PrintWriter(extender._callbacks.getStdout(), True)

        # create an instance of Burp's text editor, to display our deserialized data
        self._txtInput = extender._callbacks.createTextEditor()
        self._txtInput.setEditable(editable)

    #
    # implement IMessageEditorTab
    #

    def getTabCaption(self):
        return "WBXML"

    def getUiComponent(self):
        return self._txtInput.getComponent()

    def isEnabled(self, content, isRequest):
        # enable this tab for requests containing a data parameter
        req = self._extender._helpers.analyzeRequest(content)
        req_headers = req.getHeaders()
        for header in req_headers:
            if "wbxml" in header:
                return True
        return False

    def setMessage(self, content, isRequest):
        if content is None:
            # clear our display
            self._txtInput.setText(None)
            self._txtInput.setEditable(False)
        else:
            # # retrieve the data parameter
            if isRequest:
                self._txtInput.setEditable(True)
            else:
                self._txtInput.setEditable(False)
            req = self._extender._helpers.analyzeRequest(content)
            request_body = content[req.getBodyOffset():]
            # self._stdout.println("REQUEST BODY FROM SET MESSAGE: " + self._extender._helpers.bytesToString(request_body))
            try:
                decoded_wbxml = ASCommandResponse.ASCommandResponse(request_body)
            except:
                self._stdout.println("Exception occoured while decoding")
            # deserialize the parameter value
            self._txtInput.setText(decoded_wbxml.xmlString)
            self._txtInput.setEditable(self._editable)
        self._currentMessage = content

    def getMessage(self):
        # determine whether the user modified the deserialized data
        if self._txtInput.isTextModified():
            #     # reserialize the data
            text = self._txtInput.getText()
        #     input = self._extender._helpers.urlEncode(self._extender._helpers.base64Encode(text))

        #     # update the request with the new parameter value
        #     return self._extender._helpers.updateParameter(self._currentMessage, self._extender._helpers.buildParameter("data", input, IParameter.PARAM_BODY))
        # else:
        return self._currentMessage

    def isModified(self):
        return self._txtInput.isTextModified()

    def getSelectedData(self):
        return self._txtInput.getSelectedText()
