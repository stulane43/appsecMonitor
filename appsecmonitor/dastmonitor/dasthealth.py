##########################################
# DAST Health
##########################################

from appsecmonitor.connector import Connector
from appsecmonitor.scanparser import ScanParser
from .webinspect import WebInspect
import concurrent.futures

class DastHealth(Connector):
    
    def __init__(self):
        super().__init__(__name__)
        self.scanParser = ScanParser(self.details['wiAllScansFile'], self.details['wiCompletedScansFile'])
        self.wi = WebInspect(self.details)
        self.completedScanData = []
        self.keyType = 'projectName'

    def getFailedScans(self, data):
        '''
        Gets failed count and filepath of failed scan data based on scan data provided
        - Returns dict: {failedCount, failedScans}
        - deletes wiFaileScansFile
        '''
        self.scanParser.compareScans(data['tmpScanData'], data['scanData'], self.keyType)
        if len(self.scanParser.newScanData) > 0:
            self.scanParser.writeScanData(self.scanParser.newScanData, self.details['wiFailedScansFile'])
            return {'failedCount': len(self.scanParser.newScanData), 'failedScans': self.details['wiFailedScansFile']}
        else:
            self.scanParser.deleteScanFile(self.details['wiFailedScansFile'])
            return {'failedCount': 0, 'failedScans': None}

    def getScanHealth(self, data):
        '''
        Gets failed count and filepath of failed scan data based on scan data provided
        - If scanData is different than tmpScanData, updates the scan data file with tmp data key values
        - Returns dict: {failedCount, failedScans}
        '''
        if data['tmpScanData'] == None:
            self.scanParser.writeScanData(self.completedScanData, self.details['wiFailedScansFile'])
            scanHealth = {'failedCount': len(data['scanData'].keys()), 'failedScans': self.details['wiFailedScansFile']}
        elif data['scanData'] != data['tmpScanData']:
            self.updateScanData(data)
            scanHealth = self.getFailedScans(data)
        else:
            self.scanParser.deleteScanFile(self.details['wiFailedScansFile'])
            scanHealth = {'failedCount': 0, 'failedScans': None}
        return scanHealth

    def updateScanData(self, data):
        '''
        Updates any new projects identified in tmp data keys and adds them to the wiAllScansFile
        '''
        self.scanParser.compareScans(data['scanData'], data['tmpScanData'], self.keyType)
        self.scanParser.updateScanData({'scanFile': self.details['wiAllScansFile'], 'scanData': data['scanData']}, data['tmpScanData'])
        if len(self.scanParser.newScanData) > 0:
            self.scanParser.writeScanData(self.scanParser.newScanData, self.details['wiAllScansFile'], False)
        self.scanParser.newScanData = []

    def completedScanResults(self, completedScan):
        '''
        Formats completed scan data
        - Appends dict to completedScanData list: {scanId, projectName, scanStatus, scanDate}
        '''
        if completedScan != []:
            if completedScan['Name'] not in self.completedScanData:
                completedScanResults = {
                    'scanId': completedScan['ID'],
                    'projectName': completedScan['Name'],
                    'scanStatus': completedScan['Status'],
                    'scanDate': completedScan['StartTime']
                }
                formattedCompletedScanData = self.scanParser.formatScanData(completedScanResults, self.keyType)
                self.completedScanData.append(formattedCompletedScanData)

    def dastHealth(self):
        completedScans = self.wi.getCompletedScans()
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(self.completedScanResults, completedScans)
        self.scanParser.writeScanData(self.completedScanData, self.scanParser.scanFile)
        data = self.scanParser.getScanData(self.details['wiAllScansFile'], self.details['wiCompletedScansFile'])
        dastHealth = self.getScanHealth(data)
        return dastHealth