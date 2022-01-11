from . import dastmonitor
from . import sastmonitor
from .monitorformatter import MonitorFormatter

class AppsecMonitor():
    def __init__(self):
        self.dastMonitor = dastmonitor.DastMonitor()
        self.sastMonitor = sastmonitor.SastMonitor()
        self.monitorFormatter = MonitorFormatter()