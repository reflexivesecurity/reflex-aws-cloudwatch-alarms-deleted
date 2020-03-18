# reflex-aws-cloudwatch-alarms-deleted

A Reflex rule for detecting AWS Cloudwatch alarms that are deleted.

## Usage
To use this rule either add it to your `reflex.yaml` configuration file:
```
rules:
  - reflex-aws-cloudwatch-alarms-deleted:
    version: latest
```

or add it directly to your Terraform:
```
...

module "reflex-aws-cloudwatch-alarms-deleted" {
  source           = "github.com/cloudmitigator/reflex-aws-cloudwatch-alarms-deleted"
}

...
```

## License
This Reflex rule is made available under the MPL 2.0 license. For more information view the [LICENSE](https://github.com/cloudmitigator/reflex-aws-cloudwatch-alarms-deleted/blob/master/LICENSE) 
