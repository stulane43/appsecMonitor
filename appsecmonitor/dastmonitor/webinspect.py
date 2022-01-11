##########################################
# WebInspect API
##########################################

from appsecmonitor.scanparser import ScanParser
from datetime import timedelta
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebInspect():

    def __init__(self, details):
        self.details = details
        self.certVerify = False
        self.todaysDate = ScanParser.getTodaysDate()
        self.startsAfter = self.todaysDate - timedelta(days=4)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def getCompletedScans(self):
        '''
        Gets all completed project scans in WebInspect
        - Params: {startsAfter}
        - Returns completedScans
        '''
        url = f"https://{self.details['wiUsername']}:{self.details['wiPassword']}@{self.details['wiServer']}/webinspect/scanner/scans"
        params = {
            'startsAfter': self.startsAfter
        }
        response = requests.get(url, headers=self.headers, params=params, verify=self.certVerify)
        completedScans = response.json()
        return completedScans