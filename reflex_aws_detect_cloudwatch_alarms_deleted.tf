module "reflex_aws_detect_cloudwatch_alarms_deleted" {
  source           = "git::https://github.com/cloudmitigator/reflex-engine.git//modules/cwe_lambda"
  rule_name        = "DetectCloudwatchAlarmsDeleted"
  rule_description = "Rule to check when Cloudwatch Alarms are Deleted"

  event_pattern = <<PATTERN
{
  "eventType": [
    "AwsApiCall"
  ],
  "eventSource": [
    "monitoring.amazonaws.com"
  ],
  "eventName": [
    "DeleteAlarms"
  ]
  }
}
PATTERN

  function_name   = "DetectCloudwatchAlarmsDeleted"
  source_code_dir = "${path.module}/source"
  handler         = "reflex_aws_detect_cloudwatch_alarms_deleted.lambda_handler"
  lambda_runtime  = "python3.7"
  environment_variable_map = {
    SNS_TOPIC = var.sns_topic_arn,

  }



  queue_name    = "DetectCloudwatchAlarmsDeleted"
  delay_seconds = 60

  target_id = "DetectCloudwatchAlarmsDeleted"

  sns_topic_arn  = var.sns_topic_arn
  sqs_kms_key_id = var.reflex_kms_key_id
}
