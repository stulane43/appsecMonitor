##########################################
# Slack Alert Formatter
##########################################

import json
import requests

class AlertFormatter():
    
    def __init__(self, file):
        self.file = file

    def sendAlert(self, webhook, message):
        '''
        Sends Slack message
        - Requires slack generated webhook
        '''
        requests.post(url=webhook, json=message)

    def appendAlert(self, text):
        '''
        Adds content to json file used to send alert message
        '''
        with open(self.file, 'r+') as file:
            message = json.load(file)
            attachments = message['attachments']
            blocks = attachments[0]['blocks']
            blocks.append(text)
            file.seek(0)
            json.dump(message, file, indent=4)
            file.close()

    def divider(self):
        '''
        Adds divider to json file used to send alert message
        '''
        divider = {'type': 'divider'}
        self.appendAlert(divider)

    def header(self, text):
        '''
        Adds header to json file used to send alert message
        '''
        header = {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{text}",
            }
        }
        self.appendAlert(header)

    def sectionMrkdwn(self, text):
        '''
        Adds markdown section to json file used to send alert message
        '''
        sectionTitles = ['type', 'text']
        sectionDetails = ['mrkdwn', text]
        data = dict(zip(sectionTitles, sectionDetails))
        section = {'type': 'section', 'text': data}
        self.appendAlert(section)