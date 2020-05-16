module "cwe" {
  source      = "git::https://github.com/cloudmitigator/reflex-engine.git//modules/cwe?ref=v0.6.0"
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
