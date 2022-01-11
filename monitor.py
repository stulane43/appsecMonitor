##########################################
# appsecMonitor Handler
##########################################

from appsecmonitor import AppsecMonitor
from alertbuilder.alertbuilder import AlertBuilder

class Monitor(AppsecMonitor):
    def __init__(self):
        super().__init__()

    def monitorAlert(self, alerts):
        '''
        Builds and sends Slack Alert
        params (optional): {sastHealth, dastHealth, newSastFindings}
        '''
        monitorAlerts = self.monitorFormatter.getMonitorAlerts(alerts)
        self.alertBuilder = AlertBuilder(monitorAlerts, self.sastMonitor.health.details)
        alert = self.alertBuilder.createAlert()
        self.alertBuilder.sendAlert(self.alertBuilder.details['slackWebhook'], alert)

    def monitorFull(self):
        '''
        Gets SAST and DAST health and any 'To Verify' SAST Findings
        - returns dict: {sastHealth, dastHealth, newSastFindings}
        '''
        sastHealth = self.sastMonitor.health.sastHealth()
        dastHealth = self.dastMonitor.health.dastHealth()
        newSastFindings = self.sastMonitor.findings.newSastFindings()
        return {'sastHealth': sastHealth, 'dastHealth': dastHealth, 'newSastFindings': newSastFindings}

    def monitorSast(self):
        '''
        Gets SAST health and any 'To Verify' SAST Findings
        - returns dict: {sastHealth, newSastFindings}
        '''
        sastHealth = self.sastMonitor.health.sastHealth()
        newSastFindings = self.sastMonitor.findings.newSastFindings()
        return {'sastHealth': sastHealth, 'newSastFindings': newSastFindings}

    def runFullMonitor(self):
        alerts = self.monitorFull()
        self.monitorAlert(alerts)

    def runSastMonitor(self):
        alerts = self.monitorSast()
        self.monitorAlert(alerts)
