##########################################
# SAST Health
##########################################

from appsecmonitor.connector import Connector
from appsecmonitor.scanparser import ScanParser
from .checkmarx import Checkmarx
import concurrent.futures

class SastHealth(Connector):
    
    def __init__(self):
        super().__init__(__name__)
        self.scanParser = ScanParser(self.details['cxFailedScansFile'], self.details['cxTmpFailedScansFile'])
        self.cx = Checkmarx(self.details)
        self.failedScanData = []
        self.keyType = 'scanId'

    def getScanHealth(self, data):
        '''
        Gets failed count and filepath of failed scan data based on scan data provided
        - Returns dict: {failedCount, failedScans}
        '''
        if data['tmpScanData'] == None:
            scanHealth = {'failedCount': len(data['scanData'].keys()), 'failedScans': self.details['cxFailedScansFile']}
        elif data['scanData'] != data['tmpScanData']:
            self.scanParser.compareScans(data['scanData'], data['tmpScanData'], self.keyType)
            if len(self.scanParser.newScanData) > 0:
                self.scanParser.writeScanData(self.scanParser.newScanData, self.details['cxNewFailedScansFile'])
            scanHealth = {'failedCount': len(self.scanParser.newScanData), 'failedScans': self.details['cxNewFailedScansFile']}
        else:
            self.scanParser.deleteScanFile(self.details['cxNewFailedScansFile'])
            scanHealth = {'failedCount': 0, 'failedScans': None}
        return scanHealth

    def getFailedScans(self, scanHealthData):
        '''
        Formats failed scan data
        - Returns dict: {scanId, projectName, scanStatus, scanDetails, scanType, engineServer, scanDate}
        '''
        if scanHealthData == []:
            failedScan = None
        else:
            if scanHealthData[0]['engineServer'] == None:
                engineServer = 'None'
            formattedScanDate = self.scanParser.formatScanDate(scanHealthData[0]['dateAndTime']['startedOn'])
            dateDiff = self.scanParser.todaysData - formattedScanDate
            if dateDiff.days <= 7:
                failedScan = {
                    'scanId': scanHealthData[0]['id'],
                    'projectName': scanHealthData[0]['project']['name'],
                    'scanStatus': scanHealthData[0]['status']['name'], 
                    'scanDetails': scanHealthData[0]['status']['details']['stage'], 
                    'scanType': scanHealthData[0]['scanType']['value'],
                    'engineServer': engineServer, 
                    'scanDate': scanHealthData[0]['dateAndTime']['startedOn']
                }
            else:
                failedScan = None
        return failedScan

    def failedScanResults(self, projectId):
        '''
        Gets all failed scans and appends them to failedScanData list
        '''
        scanHealthData = self.cx.getScanHealthData(projectId)
        failedScan = self.getFailedScans(scanHealthData)
        if failedScan != None:
            formattedFailedScanData = self.scanParser.formatScanData(failedScan, self.keyType)
            self.failedScanData.append(formattedFailedScanData)

    def sastHealth(self):
        projectIds = self.cx.getProjects()
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(self.failedScanResults, projectIds)
        self.scanParser.writeScanData(self.failedScanData, self.scanParser.scanFile)
        data = self.scanParser.getScanData(self.details['cxFailedScansFile'], self.details['cxTmpFailedScansFile'])
        sastHealth = self.getScanHealth(data)
        return sastHealth