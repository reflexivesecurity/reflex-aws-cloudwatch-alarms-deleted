""" Module for DetectCloudwatchAlarmsDeleted """

import json
import os

import boto3
from reflex_core import AWSRule


class DetectCloudwatchAlarmsDeleted(AWSRule):
    """ AWS rule for CloudWatch Alarms Deleted """

    def __init__(self, event):
        super().__init__(event)

    def extract_event_data(self, event):
        """ Extract required data from the event """
        self.alarm_names = event["detail"]["requestParameters"]["alarmNames"]

    def resource_compliant(self):
        """
        Determine if the resource is compliant with your rule.
        """
        # We simply want to know when this event occurs. Since this rule was
        # triggered we know that happened, and we want to alert. Therefore
        # the resource is never compliant.
        return False

    def get_remediation_message(self):
        """ Returns a message about the remediation action that occurred """
        alarms = ', '.join(self.alarm_names)
        return f"CloudWatch Alarms were deleted: {alarms}"

def lambda_handler(event, _):
    """ Handles the incoming event """
    rule = DetectCloudwatchAlarmsDeleted(json.loads(event["Records"][0]["body"]))
    rule.run_compliance_rule()
