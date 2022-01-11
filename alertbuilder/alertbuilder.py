##########################################
# Slack Alert Builder
##########################################

from alertbuilder.alertformatter import AlertFormatter
from appsecmonitor.connector import Connector
import shutil
import json

class AlertBuilder(AlertFormatter, Connector):

    def __init__(self, monitorAlerts, details):
        super().__init__(details['slackAlertFile'])
        self.monitorAlerts = monitorAlerts
        self.details = details
        self.file = details['slackAlertFile']

    def parseAlertTitles(self):
        '''
        writes title section to alert
        '''
        for alert in self.monitorAlerts['alerts']:
            self.sectionMrkdwn(alert['title'])

    def parseAlertData(self):
        '''
        writes Header and text section to alert
        - Adds alert header
        - Adds markdown text
        - Adds divider between each section
        '''
        for alert in self.monitorAlerts['alerts']:
            if alert['status']:
                self.divider()
                self.header(alert['header'])
                self.sectionMrkdwn(alert['text'])

    def updateAlertColor(self, color):
        '''
        Adds attachment color based on criticality of alert
        '''
        with open(self.file, 'r') as file:
            message = json.load(file)
        attachments = message['attachments']
        attachments[0]['color'] = color
        with open(self.file, 'w') as file:
            json.dump(message, file, indent=4)

    def createAlert(self):
        shutil.copy(self.details['slackAlertTemplate'], self.file)
        self.updateAlertColor(self.monitorAlerts['color'])
        self.parseAlertTitles()
        self.parseAlertData()
        with open(self.file, 'r') as file:
            alert = json.load(file)
        return alert