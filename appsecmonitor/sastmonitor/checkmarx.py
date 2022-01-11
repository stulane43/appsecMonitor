##########################################
# Checkmarx API 
##########################################

import requests
import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Checkmarx():

    def __init__(self, details):
        self.details = details
        self.certVerify = False
        self.token = self.getAuthToken()
        self.payload = {}
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json;v=1.0'
        }
        
    def getAuthToken(self):
        '''
        Authenticate to Checkmarx REST API using basic authentication
        - Returns API Access Token
        '''
        url = f"https://{self.details['cxServer']}/cxrestapi/auth/identity/connect/token"
        payload = f"username={self.details['cxUsername']}&password={self.details['cxPassword']}&grant_type=password&scope=sast_rest_api&client_id=resource_owner_client&client_secret={self.details['cxClientSecret']}"
        headers = {
            'cxOrigin': '',
            'Accept': 'application/json;v=1.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, headers=headers, data=payload, verify=self.certVerify)
        jsonData = response.json()
        token = jsonData['access_token']
        return token

    def getProjects(self):
        '''
        Get details of all onboarded projects
        - Returns Project IDs
        '''
        projectIds = []
        response = requests.get(f"https://{self.details['cxServer']}/cxrestapi/projects", headers=self.headers, data=self.payload, verify=self.certVerify)
        jsonData = response.json()
        for project in jsonData:
            projectId = project['id']
            projectIds.append(projectId)
        return projectIds
    
    def getCompletedScans(self, projectId):
        '''
        Get details of a specific scan that has finished
        - Params: {projectid, last: 1, scanStatus: Finished}
        - Returns dict: {scan ID, Project Name}
        '''
        params = {
            'projectid': projectId,
            'last': 1,
            'scanStatus': 'Finished'
        }
        response = requests.get(f"https://{self.details['cxServer']}/cxrestapi/sast/scans", headers=self.headers, data=self.payload, verify=self.certVerify, params=params)
        jsonData = response.json()
        if jsonData == []:
            return None
        for p in range(len(jsonData)):
            scanId = jsonData[p]['id']
            projectName = jsonData[p]['project']['name']
        return {'scanId': scanId, 'projectName': projectName}

    def postScanReport(self, scanId):
        '''
        Registers a new SAST report
        - payload: {reportType: XML, ScanId}
        '''
        payload = {
            'reportType': 'XML',
            'ScanId': scanId
        }
        response = requests.post(f"https://{self.details['cxServer']}/cxrestapi/reports/sastScan", headers=self.headers, data=payload, verify=self.certVerify)
        jsonData = response.json()
        return jsonData['reportId']
                
    def getReportStatus(self, scanReportId):
        '''
        Get the status of a generated report
        - Query: scanReportId
        '''
        response = requests.get(f"https://{self.details['cxServer']}/cxrestapi/reports/sastScan/{scanReportId}/status", headers=self.headers, data=self.payload, verify=self.certVerify)
        if 'InProcess' in response.text:
            time.sleep(5)
            self.getReportStatus(scanReportId)
        else:
            print(f'{scanReportId}: Scan Report Created\n')

    def getScanReport(self, scanReportId):
        '''
        Get the specified report once generated
        - Query: scanReportId
        - Returns scanReport
        '''
        scanReport = requests.get(f"https://{self.details['cxServer']}/cxrestapi/reports/sastScan/{scanReportId}", headers=self.headers, data=self.payload, verify=self.certVerify)
        return scanReport
            
    def getScanHealthData(self, projectId):
        '''
        Get details of a specific scan that has failed
        - Params: {projectid, last: 1, scanStatus: Failed}
        - Returns scanHealthData
        '''
        url = f"https://{self.details['cxServer']}/cxrestapi/sast/scans"
        params = {
        'projectid': projectId,
        'last': 1,
        'scanStatus': 'Failed'
        }
        response = requests.get(url, headers=self.headers, data=self.payload, verify=self.certVerify, params=params)
        scanHealthData = response.json()
        return scanHealthData