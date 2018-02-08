import boto3,os

SQS_URL = os.getenv('SQS_URL')
ENV = os.getenv('ENV')
AWS_REGION = os.getenv('AWS_REGION')

# Create SQS client
sqs = boto3.client('sqs', region_name=AWS_REGION)

# List SQS queues
response = sqs.list_queues()

print(response)
print(response['QueueUrls'])
