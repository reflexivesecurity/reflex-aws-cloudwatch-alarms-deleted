terraform {
  backend "s3" {
    bucket = "reflex-state"
    key    = "reflex-cloudwatch-alarms-deleted"
  }
}

data "aws_caller_identity" "current" {}

module "cloudwatch-alarms-deleted-cwe" {
  source = "../../terraform/cwe"
}

module "cloudwatch-alarms-deleted" {
  source                    = "../../terraform/sqs_lambda"
  cloudwatch_event_rule_id  = module.cloudwatch-alarms-deleted-cwe.id
  cloudwatch_event_rule_arn = module.cloudwatch-alarms-deleted-cwe.arn
  sns_topic_arn             = module.central-sns-topic.arn
  reflex_kms_key_id         = module.reflex-kms-key.key_id
}

module "central-sns-topic" {
  topic_name         = "ReflexAlerts"
  stack_name         = "EmailSNSStackReflexAlerts"
  source             = "git::https://github.com/cloudmitigator/reflex-engine.git//modules/sns_email_subscription?ref=v1.0.0"
  notification_email = "michael.schappacher@cloudmitigator.com"
}

module "reflex-kms-key" {
  source = "git::https://github.com/cloudmitigator/reflex-engine.git//modules/reflex_kms_key?ref=v1.0.0"
}

resource "aws_sqs_queue" "test_queue" {
  name          = "test-queue"
  delay_seconds = 0
}

resource "aws_sqs_queue_policy" "test_queue_policy" {
  queue_url = aws_sqs_queue.test_queue.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqspolicy",
  "Statement": [
   {
      "Sid": "AllowSNSTopic",
      "Effect": "Allow",
      "Principal": {
        "Service": "sns.amazonaws.com"
      },
      "Action": "sqs:SendMessage",
      "Resource": "${aws_sqs_queue.test_queue.arn}"
    },
   {
      "Sid": "AllowUserAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "${data.aws_caller_identity.current.arn}"
      },
      "Action": "sqs:ReceiveMessage",
      "Resource": "${aws_sqs_queue.test_queue.arn}"
    }
  ]
}
POLICY
}

resource "aws_sns_topic_subscription" "test_queue_target" {
  topic_arn = module.central-sns-topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.test_queue.arn
}