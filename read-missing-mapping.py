
# coding: utf-8



import boto3
import json

region_name = 'eu-central-1'
queue_name = 'missing-mapping'
max_queue_messages = 10
message_bodies = []
sqs = boto3.resource('sqs', region_name=region_name)
queue = sqs.get_queue_by_name(QueueName=queue_name)
while True:
    messages_to_delete = []
    for message in queue.receive_messages(MaxNumberOfMessages=max_queue_messages):
        # process message body
        body = json.loads(message.body)
        message_bodies.append(body)
        # add message to delexte
        messages_to_delete.append({
            'Id': message.message_id,
            'ReceiptHandle': message.receipt_handle
        })

    # if you don't receive any notifications the
    # messages_to_delete list will be empty
    if len(messages_to_delete) == 0:
        break
    # delete messages to remove them from SQS queue
    # handle any errors
    else:
        delete_response = queue.delete_messages(
                Entries=messages_to_delete)




results = {}
for i in message_bodies:
    if 'key' in i and i['key'] in results:
        results[i['key']] = results[i['key']]+1
    elif 'key' not in i:
        pass
    elif 'key' in i and i['key'] not in results:
        results[i['key']] = 1




with open("mapping.txt", 'w') as f:
    for k,v in results.items():
        f.write(str(k)+','+str(v)+'\n')




get_ipython().system(' cat mapping.txt')

