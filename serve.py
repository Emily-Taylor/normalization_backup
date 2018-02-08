import os
import json
import logging
import random
import boto3
log = logging.getLogger()
log.setLevel(logging.DEBUG)

import common

SQS_URL = os.getenv('SQS_URL')
ENV = os.getenv('ENV')
AWS_REGION = os.getenv('AWS_REGION')

def publish_to_sqs(message):
    sqs = boto3.client('sqs', region_name=AWS_REGION)
    return sqs.send_message(
    QueueUrl=SQS_URL,
    MessageBody=json.dumps(message),
    DelaySeconds=123
 )


def dispatch(event, context):
    #log.debug("Received event {}".format(json.dumps(event)))
    
    threshold_millis = 10 * 1000  # leave when there are only 10 seconds left
    # some of your work here
    try:
        msg = json.loads(event['Records'][0]['Sns']['Message'])
    except:
        raise NameError("couldn't locate json on SNS payload")
    # check remain time by accessing context object
    remain_millis = context.get_remaining_time_in_millis()
    if remain_millis < threshold_millis:
        #print(type(msg))
        if 'parts' in msg:
            for part in msg['parts']:
                #print(part.keys())
            # check if key is in list of keys we know how to normalize. 
            # if it doesn't exists, it's new and we need to learn how to handle it.
            # if it exists, rename it, and apply the functions listed.
            # add source to pricing

            # emit to SQS each part that's ready for storage.  
                res = publish_to_sqs(part)

        else:
            logger.error("couldn't locate  'parts' in payload")
        
        msg = {"necessary information for next function":   event}
        res = publish_to_sqs(msg)
        #log.debug(res)
        return {"partially completed": True}

    return {"completed": True}