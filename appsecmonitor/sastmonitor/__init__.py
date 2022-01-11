from .sastfindings import SastFindings
from .sasthealth import SastHealth

class SastMonitor():
    def __init__(self):
        self.health = SastHealth()
        self.findings = SastFindings()