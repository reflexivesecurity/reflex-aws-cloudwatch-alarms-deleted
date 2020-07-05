from behave import *
import boto3
import uuid
import logging
import time
from reflex_acceptance_common import ReflexAcceptance

acceptance_client = ReflexAcceptance("cloudwatch-alarms-deleted")
CLOUDWATCH_CLIENT = boto3.client("cloudwatch")
SQS_CLIENT = boto3.client("sqs")
GHERKIN_UUID = uuid.uuid4()

def create_alarm():
    response = CLOUDWATCH_CLIENT.put_metric_alarm(
        AlarmName=f'gherkin-test-{GHERKIN_UUID}',
        ActionsEnabled=False,
        MetricName='test',
        Namespace='test',
        Statistic='Sum',
        Dimensions=[
            {
                'Name': 'test',
                'Value': 'test'
            },
        ],
        Period=30,
        Unit='Seconds',
        EvaluationPeriods=3,
        DatapointsToAlarm=1,
        Threshold=1,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='ignore',
    )
    logging.info("Created metric alarm: %s", response)

def get_message_from_queue(queue_url):
    x = 0
    while x < 3:
        try:
            message = SQS_CLIENT.receive_message(QueueUrl=queue_url, WaitTimeSeconds=20)
            message_body = message["Messages"][0]["Body"]
            if message_body:
                break
        except KeyError:
            logging.info("Message not avaliable yet, retrying.")
            x += 1
    return message_body

@given("cloudwatch-alarms-deleted rule is deployed in the account")
def assert_reflex_rule_deployed(context):
    assert acceptance_client.get_queue_url_count("CloudwatchAlarmsDeleted-DLQ") == 1
    assert acceptance_client.get_queue_url_count("CloudwatchAlarmsDeleted") == 2
    assert acceptance_client.get_queue_url_count("test-queue") == 1
    sqs_test_response = SQS_CLIENT.list_queues(QueueNamePrefix="test-queue")
    context.config.userdata["test_queue_url"] = sqs_test_response["QueueUrls"][0]

@when("a Cloudwatch alarm is deleted")
def delete_alarm(context):
    response = CLOUDWATCH_CLIENT.delete_alarms(
        AlarmNames=[
            f'gherkin-test-{GHERKIN_UUID}'
        ]
    )
    logging.info("Metric alarm deleted: %s", response)

@then("a Reflex notification should be received")
def inspect_sqs_queue(context):
    message = get_message_from_queue(context.config.userdata["test_queue_url"])
    print(message)
