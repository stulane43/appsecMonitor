##########################################
# appsecMonitor Alert Formatter
##########################################

import json

class MonitorFormatter():

    def __init__(self) -> None:
        self.color = "#37C526"
        self.string = "\n\n"
        self.monitorAlerts = []

    def formatMonitorAlertHeaders(self, totalCount, actionNeededTitle, actionNeededHeader):
        '''
        Sets Message title and header for each alert
        - Returns dict: {status, title, header}
        '''
        if totalCount > 0:
            status = True
            title = actionNeededTitle
            header = actionNeededHeader
            return {'status': status, 'title': title, 'header': header}

    def formatMonitorAlertText(self, monitorAlert, alertType, alertFile):
        '''
        Sets Message text for each alert
        - Returns alert text
        '''
        text = []
        with open(monitorAlert[alertFile], 'r') as file:
            fileData = json.load(file)
        if alertType == 'sastHealth':
            for key in fileData.keys():
                text.append(f">*Project:* `{fileData[key][0]['projectName']}`\n>*ScanDate:* {fileData[key][0]['scanDate']}")
        elif alertType == 'dastHealth':
            for key in fileData.keys():
                text.append(f">*Project:* `{fileData[key][0]['projectName']}`\n>*Last Successful Scan:* {fileData[key][0]['scanDate']}")
        elif alertType == 'newSastFindings':
            for key in fileData.keys():
                text.append(f">*Project:* {fileData[key][0]['description']}")
        alertText = self.string.join(text)
        return alertText

    def getMonitorAlerts(self, alerts):
        # Repetitive code - Needs to be updated.
        try:
            if alerts['newSastFindings']['totalToVerify'] > 0:
                self.color = "#c97a20"
        except:
            pass
        try:
            if alerts['sastHealth']['failedCount'] > 0:
                self.color = "#8C2C2C"
                alertType = 'sastHealth'
                alertFile = 'failedScans'
                actionNeededTitle = f">:red_siren:  *SAST Scans Failed*  *`Total Failures: {alerts['sastHealth']['failedCount']}`*"
                actionNeededHeader = "Failed SAST Scans"
                headers = self.formatMonitorAlertHeaders(alerts['sastHealth']['failedCount'], actionNeededTitle, actionNeededHeader)
                text = self.formatMonitorAlertText(alerts['sastHealth'], alertType, alertFile)
                self.monitorAlerts.append({'status': headers['status'], 'title': headers['title'], 'header': headers['header'], 'text': text})
            else:
                self.monitorAlerts.append({'status': False, 'title': ">*All SAST Scans Were Successful*  :heavy_check_mark:"})
        except:
            pass
        try:
            if alerts['dastHealth']['failedCount'] > 0:
                self.color = "#8C2C2C"
                alertType = 'dastHealth'
                alertFile = 'failedScans'
                actionNeededTitle = f">:red_siren:  *DAST Scans Failed*  *`Total Failures: {alerts['dastHealth']['failedCount']}`*"
                actionNeededHeader = "Failed DAST Scans"
                headers = self.formatMonitorAlertHeaders(alerts['dastHealth']['failedCount'], actionNeededTitle, actionNeededHeader)
                text = self.formatMonitorAlertText(alerts['dastHealth'], alertType, alertFile)
                self.monitorAlerts.append({'status': headers['status'], 'title': headers['title'], 'header': headers['header'], 'text': text})
            else:
                self.monitorAlerts.append({'status': False, 'title': ">*All DAST Scans Were Successful*  :heavy_check_mark:"})
        except:
            pass
        try:
            if alerts['newSastFindings']['totalToVerify'] > 0:
                alertType = 'newSastFindings'
                alertFile = 'newFindings'
                actionNeededTitle = f">:mag:  *SAST Findings to Verify*  *`Total Findings: {alerts['newSastFindings']['totalToVerify']}`*"
                actionNeededHeader = "SAST Findings"
                headers = self.formatMonitorAlertHeaders(alerts['newSastFindings']['totalToVerify'], actionNeededTitle, actionNeededHeader)
                text = self.formatMonitorAlertText(alerts['newSastFindings'], alertType, alertFile)
                self.monitorAlerts.append({'status': headers['status'], 'title': headers['title'], 'header': headers['header'], 'text': text})
            else:
                self.monitorAlerts.append({'status': False, 'title': ">*No SAST Findings to Verify*  :heavy_check_mark:"})
        except:
            pass
        return {'color': self.color, 'alerts': self.monitorAlerts}