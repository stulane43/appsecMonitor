##########################################
# Scan Parser for appsecMonitor
##########################################

from appsecmonitor.connector import Connector
from datetime import datetime
import concurrent.futures
import json
import os
import glob

class ScanParser(Connector):

    def __init__(self, scansFile, tmpScansFile):
        super().__init__(__name__)
        self.scanFile = self.getScanFile(scansFile, tmpScansFile)
        self.todaysData = self.getTodaysDate()
        self.newScanData = []
    
    def getScanFile(self, scanFile, tmpScanFile):
        '''
        Returns tmp file path if it exists
        - Otherwise, returns base file path
        '''
        if os.path.exists(scanFile):
            return tmpScanFile
        else:
            return scanFile

    @classmethod
    def getTodaysDate(self):
        '''
        Returns current formatted datetime object
        - Can be used as a classmethod
        '''
        todaysdate = datetime.today().strftime('%Y-%m-%d')
        todaysdate = datetime.strptime(todaysdate, '%Y-%m-%d')
        todaysdate = todaysdate.date()
        return todaysdate

    def getScanData(self, scansFile, tmpScansFile):
        '''
        Returns json data from base file path and tmp file path if either or both exist
        - Returns dict: {scanData, tmpScanData}
        '''
        if os.path.exists(scansFile):
            with open(scansFile, 'r') as file:
                scanData = json.load(file)
            if os.path.exists(tmpScansFile):
                with open(tmpScansFile, 'r') as tmpFile:
                    tmpScanData = json.load(tmpFile)
                self.overwriteScanData(tmpScansFile, scansFile)
                os.remove(tmpScansFile)
                return {'scanData': scanData, 'tmpScanData': tmpScanData}
            else:
                return {'scanData': scanData, 'tmpScanData': None}
        else:
            return {'scanData': None, 'tmpScanData': None}

    def formatScanDate(self, scanDate):
        '''
        Returns formatted scan datetime object to match current datetime object
        '''
        splitScanDate = scanDate.split("T", 1)
        scanDate = splitScanDate[0]
        dateTimeObj = datetime.strptime(scanDate, '%Y-%m-%d')
        formattedScanDate = dateTimeObj.date()
        return formattedScanDate

    def formatScanData(self, ScanData, keyType=None):
        '''
        Sets each scan data dictionary with the key name specified (optional)
        - Returns dict: {keyType: scanData}
        '''
        if keyType == None:
            formattedScanData = {f"{ScanData[self.keyType]}": [ScanData]}
        else:
            formattedScanData = {f"{ScanData[keyType]}": [ScanData]}
        return formattedScanData
    
    def writeScanData(self, scanData, scanFile, writeFile=None):
        '''
        Writes scanData to file specified (Appends to file once created)
        - Optional Boolean - writeFile: False - Will append to file specified (File must exist)
        '''
        if writeFile == None:
            writeFile = True
        for data in scanData:              
            if writeFile:
                with open(scanFile, 'w') as newFile:
                    json.dump(data, newFile, indent=4)
                writeFile = False
            else:      
                with open(scanFile, 'r+') as newFile:
                    tmpData = json.load(newFile)
                    tmpData.update(data)
                    newFile.seek(0)
                    json.dump(tmpData, newFile, indent=4)
                    newFile.close()
    
    def overwriteScanData(self, tmpScansFile, scansFile):
        '''
        Copies data from tmp file and overwrites base scan file
        '''
        with open(tmpScansFile, 'r') as newScanData:
            newScanData = json.load(newScanData)
        with open(scansFile, 'w') as file:
            json.dump(newScanData, file, indent=4)

    def getNewScanData(self, tmpScanKey):
        '''
        Checks all keys in tmp data and appends to newScanData list if key is not in base scan data
        '''
        if tmpScanKey not in self.scanDataKeys:
            formattedNewScanData = self.formatScanData(self.tmpScanData[tmpScanKey][0])
            self.newScanData.append(formattedNewScanData)

    def updateScanData(self, completedScans, tmpscanData):
        '''
        updates key values in base data file with key values from tmp data
        '''
        for tmpScanKey in tmpscanData.keys():
            if tmpScanKey in completedScans['scanData'].keys():
                completedScans['scanData'][tmpScanKey][0] = tmpscanData[tmpScanKey][0]
        with open(completedScans['scanFile'], 'w') as scanFile:
            json.dump(completedScans['scanData'], scanFile, indent=4)
    
    @classmethod
    def deleteScanFile(self, file):
        '''
        deletes specified file based on file path given
        - Can be used as a classmethod
        '''
        if os.path.exists(file):
            os.remove(file)

    @classmethod
    def deleteFolderContents(self, path):
        '''
        deletes all files within a given directory
        - Can be used as a classmethod
        '''
        files = glob.glob(path)
        for f in files:
            os.remove(f)

    def compareScans(self, scanData, tmpScanData, keyType):
        self.scanDataKeys = scanData.keys()
        self.tmpScanData = tmpScanData
        self.keyType = keyType
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(self.getNewScanData, tmpScanData.keys())