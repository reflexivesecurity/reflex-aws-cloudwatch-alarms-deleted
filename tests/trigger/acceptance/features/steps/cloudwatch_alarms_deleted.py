from behave import *
import boto3
import uuid
import logging
import time
from reflex_acceptance_common import ReflexAcceptance

acceptance_client = ReflexAcceptance("s3-bucket-policy-public-access")
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

@given("cloudwatch-alarms-deleted rule is deployed in the account")
def assert_reflex_rule_deployed():
    assert acceptance_client.get_queue_url_count("S3BucketPolicyPublicAccess-DLQ") == 1
    assert acceptance_client.get_queue_url_count("S3BucketPolicyPublicAccess") == 2
    assert acceptance_client.get_queue_url_count("test-queue") == 1
    sqs_test_response = SQS_CLIENT.list_queues(QueueNamePrefix="test-queue")
    context.config.userdata["test_queue_url"] = sqs_test_response["QueueUrls"][0]

@when("a Cloudwatch alarm is deleted")
def delete_alarm():
    response = CLOUDWATCH_CLIENT.delete_alarms(
        AlarmNames=[
            f'gherkin-test-{GHERKIN_UUID}'
        ]
    )
    logging.info("Metric alarm deleted: %s", response)

@then("a Reflex notification should be received")
def inspect_sqs_queue():
    pass


if __name__ == "__main__":
    create_alarm()
    time.sleep(30)
    delete_alarm()