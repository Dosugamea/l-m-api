import threading,hmac,hashlib,base64,json,io
from .EventTypes import *

class Tracer(object):
    channelSecret = None
    EventInterrupt = {}
    
    def getJson(self,request):
        return json.load(io.TextIOWrapper(request.body, encoding='utf-8'))

    def __init__(self,channelSecret=None):
        if channelSecret == None:
            print("[WARNING] Tracer can't verify Signature!!!")
        else:
            self.channelSecret = channelSecret
        self.EventInterrupt = {}
        
    def __execute(self, event, is_thread):
        if is_thread:
            _td = threading.Thread(target=self.EventInterrupt[EventTypes._NAMES_TO_VALUES[EventTypes.EventDict[event["type"]]]](event))
            _td.daemon = False
            _td.start()
        else:
            self.EventInterrupt[EventTypes._NAMES_TO_VALUES[EventTypes.EventDict[event["type"]]]](event)

    def trace(self,request,is_thread=True):
        if self.verify(request):
            events = self.getJson(request)["events"]
            for event in events:
                if EventTypes._NAMES_TO_VALUES[EventTypes.EventDict[event["type"]]] in self.EventInterrupt.keys():
                    self.__execute(event, is_thread)
        else:
            print("[ALERT] Signature was wrong.")
    
    def addEventInterruptWithDict(self, EventInterruptDict):
        self.EventInterrupt.update(EventInterruptDict)

    def addEventInterrupt(self, EventType, DisposeFunc):
        self.EventInterrupt[EventType] = DisposeFunc
    
    #Not yet Implemented.
    def verify(self,request):
        if self.channelSecret != None:
            digest = hmac.new(self.channelSecret, request.body.read(), hashlib.sha256).hexdigest()
            print(digest)
            sign = base64.b64encode(digest)
            print(sign)
            if sign == request.headers["X-Line-Signature"]:
                return True
            else:
                return False
        else:
            print("[WARNING] ChannelSecret doesn't specified.")
            return True