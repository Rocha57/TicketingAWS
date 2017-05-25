import boto3

cost = '5'

sqs = boto3.resource('sqs')
sqs_client = boto3.client('sqs')

client_db = boto3.client('dynamodb')
table_name = 'project3'

output_queue = sqs.get_queue_by_name(QueueName='project3_output')
payment_queue = sqs.get_queue_by_name(QueueName='project3_payment')

def run():
	while True:
		message = sqs_client.receive_message(
		    QueueUrl=payment_queue.url,
		    MessageAttributeNames=['response'],
		    MaxNumberOfMessages=1,
		    WaitTimeSeconds=1,
		)
		if 'Messages' in message:
			print("Paying")
			remove = sqs_client.delete_message(QueueUrl=payment_queue.url, ReceiptHandle = message['Messages'][0]['ReceiptHandle'])
			user = message['Messages'][0]['MessageAttributes']['response']['StringValue']
			response = client_db.get_item(
				TableName = table_name,
				Key = {
					'name': {
						'S': user
					}
				},
				AttributesToGet=['credit']
			)
			if response['Item']:
				credit = response['Item']['credit']['N']
				if int(credit) >= int(cost):
					response = client_db.update_item(
						TableName = table_name,
						Key = {
							'name': {
								'S': user
							}
						},
						UpdateExpression = "set credit = credit - :cost",
						ExpressionAttributeValues={
						':cost': {
            				'N': cost
            				}
            			}
					)
					send_message(output_queue, "Automatic payment successful", "SUCCESS")
				else:
					send_message(output_queue, "ardeu", "FAILED")

def send_message(queue, message, body):
	request = sqs_client.send_message(
		QueueUrl = queue.url,
		MessageBody = body,
		DelaySeconds = 10,
		MessageAttributes = {
			'response' : {
				'StringValue': message,
				'DataType': 'String'
			}
		}
	)


if __name__ == "__main__":
	run()