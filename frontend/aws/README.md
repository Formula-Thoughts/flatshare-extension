## Handy commands

Create the stack after changing the template

```
aws cloudformation create-stack \
--stack-name Flatini-Web-Stack \
--template-body file://aws/template.yml \
--parameters \
ParameterKey=DomainName,ParameterValue=formulathoughts.com \
ParameterKey=SubdomainName,ParameterValue=flatini \
ParameterKey=AliasTargetHostedZoneId,ParameterValue=Z2FDTNDATAQYW2 \
ParameterKey=HostedZoneId,ParameterValue=****** \
ParameterKey=GoogleClientId,ParameterValue=****** \
ParameterKey=GoogleClientSecret,ParameterValue=******
```

`aws s3 sync build/ s3://flatini.com`

`aws cloudfront create-invalidation --distribution-id ******** --paths "/*"`

** remember to pull and npm install before anything **
