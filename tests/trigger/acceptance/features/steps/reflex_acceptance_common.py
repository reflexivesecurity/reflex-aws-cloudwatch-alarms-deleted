import boto3


class ReflexAcceptance:
    def __init__(self, rule_name):
        self.rule_name = rule_name
        self.sqs_client = boto3.client("sqs")

    @staticmethod
    def kebab_to_camel_case(kebab_string):
        components = kebab_string.split("-")
        return components[0] + "".join(x.title() for x in components[1:])

    def get_queue_url_count(self, queue_name):
        sqs_response = self.sqs_client.list_queues(QueueNamePrefix=f"{queue_name}")
        return len(sqs_response["QueueUrls"])