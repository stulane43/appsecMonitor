##########################################
# Sast Findings
##########################################

from appsecmonitor.connector import Connector
from appsecmonitor.scanparser import ScanParser
from .checkmarx import Checkmarx
import xml.etree.ElementTree as ET
import concurrent.futures

class SastFindings(Connector):

    def __init__(self):
        super().__init__(__name__)
        ScanParser.deleteScanFile(self.details['cxtoVerifyFile']) 
        self.scanParser = ScanParser(self.details['cxtoVerifyFile'], self.details['cxTmptoVerifyFile'])
        self.cx = Checkmarx(self.details)
        self.keyType = 'projectName'
        self.scanReportData = []
        self.toVerifyFindings = []
        self.totalToVerify = 0

    def getScanDetails(self, formattedReport):
        '''
        Parses through scan report to identify any 'To Verify' findings
        - Returns dict: {projectName, scanLink, description, scanId, highsToVerify, medsToVerify, totalToVerify}
        '''
        highsToVerify = 0
        medsToVerify = 0
        lowsToVerify = 0
        confirmed = 0
        notExploitable = 0
        toVerify = 0
        infoToVerify = 0
        with open(formattedReport, encoding='utf-8') as scanReport:
            tree = ET.parse(scanReport)
            root = tree.getroot()
            rootAttrib = root.attrib
            projectName = rootAttrib['ProjectName']
            print(f'Exporting scan report for: {projectName}')
            scanLink = rootAttrib['DeepLink']
            description = "`<" + scanLink + "|" + projectName + ">`"
            scanId = rootAttrib['ScanId']
            for node in root.iter():
                for result in node.attrib:
                    if result == 'state':
                        state = node.attrib[result]
                        if state == '0':
                            toVerify += 1
                        elif state == '1':
                            notExploitable += 1
                        elif state == '2':
                            confirmed += 1
                        severity = node.attrib['Severity']
                        if severity == 'High':
                            if state == '0':
                                highsToVerify += 1
                        elif severity == 'Medium':
                            if state == '0':
                                medsToVerify += 1
                        elif severity == 'Low':
                            if state == '0':
                                lowsToVerify += 1
                        elif severity == 'Information':
                            if state == '0':
                                infoToVerify += 1
            if highsToVerify > 0:
                description = description + "\n>*High*: " + str(highsToVerify)
            if medsToVerify > 0:
                description = description + "\n>*Medium*: " + str(medsToVerify)
            totalToVerify = highsToVerify + medsToVerify       
        return {'projectName': projectName, 'scanLink': scanLink, 'description': description, 'scanId': scanId, 'highsToVerify': highsToVerify, 'medsToVerify': medsToVerify, 'totalToVerify': totalToVerify}

    def formatScanReportData(self, scanReportData):
        '''
        Returns xml report in utf-8 format
        '''
        formattedReport = f"{scanReportData['reportPath']}/{scanReportData['projectName']}.xml"
        with open(formattedReport, 'w', encoding='utf-8') as reportTemplate:
            reportTemplate.write(scanReportData['scanReport'].text)
        with open(formattedReport, encoding='utf-8') as report:
            tree = ET.parse(report)
            root = tree.getroot()
            rootAttrib = root.attrib
            for elem in rootAttrib:
                if elem == 'DeepLink':
                    try:
                        rootAttrib[elem] = rootAttrib[elem].replace('http','https')
                        break
                    except Exception as e:
                        print(Exception(e))
        tree.write(formattedReport, xml_declaration=True, method='xml', encoding='utf-8')
        return formattedReport

    def scanResults(self, projectId):
        '''
        Gets SAST scan report based on project ID given and appends them to the scanReportData list
        '''
        completedScan = self.cx.getCompletedScans(projectId)
        if completedScan != None:
            scanReportId = self.cx.postScanReport(completedScan['scanId'])
            self.cx.getReportStatus(scanReportId)
            scanReport = self.cx.getScanReport(scanReportId)
            self.scanReportData.append({'scanReport': scanReport, 'scanReportId': scanReportId, 'projectName': completedScan['projectName'], 'reportPath': self.details['cxReportsPath']})

    def getToVerifyFindings(self, scanReportData):
        '''
        Gets all To Verify findings if they exist based on report data given
        - Appends findings to toVerifyFindings list
        - Adds findings count to totalToVerify int
        '''
        formattedScanReportData = self.formatScanReportData(scanReportData)
        scanDetails = self.getScanDetails(formattedScanReportData)
        if scanDetails['totalToVerify'] > 0:
            findings = {
                'scanId': scanDetails['scanId'],
                'projectName': scanDetails['projectName'],
                'scanLink': scanDetails['scanLink'],
                'description': scanDetails['description'],
                'highsToVerify': scanDetails['highsToVerify'],
                'medsToVerify': scanDetails['medsToVerify']
            }
            formattedFindings = self.scanParser.formatScanData(findings, self.keyType)
            self.toVerifyFindings.append(formattedFindings)
            self.totalToVerify += scanDetails['totalToVerify']

    def getNewFindings(self):
        '''
        Gets all SAST scan reports and appends them to the scanReportData list
        '''
        if self.totalToVerify == 0:
            newFindings = {'totalToVerify': 0, 'newFindings': None}
        else:
            newFindings = {'totalToVerify': self.totalToVerify, 'newFindings': self.details['cxtoVerifyFile']}
        return newFindings

    def newSastFindings(self):
        projectIds = self.cx.getProjects()
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            executor.map(self.scanResults, projectIds)
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(self.getToVerifyFindings, self.scanReportData)
        self.scanParser.writeScanData(self.toVerifyFindings, self.scanParser.scanFile)
        newSastFindings = self.getNewFindings()
        self.scanParser.deleteFolderContents(f"{self.details['cxReportsPath']}/*")
        return newSastFindings