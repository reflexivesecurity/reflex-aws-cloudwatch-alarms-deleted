module "cwe" {
  source      = "git::https://github.com/reflexivesecurity/reflex-engine.git//modules/cwe?ref=v2.1.0"
  name        = "CloudwatchAlarmsDeleted"
  description = "Rule to check when Cloudwatch Alarms are Deleted"

  event_pattern = <<PATTERN
{
  "source": [
    "aws.monitoring"
  ],
  "detail-type": [
    "AWS API Call via CloudTrail"
  ],
  "detail": {
    "eventSource": [
      "monitoring.amazonaws.com"
    ],
    "eventName": [
      "DeleteAlarms"
    ]
  }
}
PATTERN

}
