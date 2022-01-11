import json
from .logger import Logger

class Connector(Logger):

    def __init__(self, name):
        super().__init__(name)
        self.details = json.load(open('/opt/appsecMonitor/appsecmonitor/configuration/config.json'))