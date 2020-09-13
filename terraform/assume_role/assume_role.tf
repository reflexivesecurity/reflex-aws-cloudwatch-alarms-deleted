data "aws_caller_identity" "current" {}
module "assume_role" {
  source = "git::https://github.com/reflexivesecurity/reflex-engine.git//modules/sqs_lambda/modules/iam_assume_role?ref=v2.1.0"

  function_name             = "CloudwatchAlarmsDeleted"
  lambda_execution_role_arn = "arn:aws:iam::${var.parent_account}:role/ReflexCloudwatchAlarmsDeletedLambdaExecution"

}
