import os
import yaml
import boto3

here = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(here,'config.yml'), 'r') as f:
    config = yaml.load(f)

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName=config['missing_queue_name'])

def send_msg(msg):
    response = queue.send_message(
    MessageBody=msg
    )
    # message ID and MD5
    return(response.get('MessageId'),response.get('MD5OfMessageBody'))

