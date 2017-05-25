import boto3

sqs = boto3.resource('sqs')
sqs_client = boto3.client('sqs')
s3 = boto3.resource('s3')
bucket_name = 'esproject3bucket'

input_queue = sqs.get_queue_by_name(QueueName='project3_input')
output_queue = sqs.get_queue_by_name(QueueName='project3_output')

filename = input('enter filename of your photograph: ');
filename1 = 'photos/'+filename
s3.meta.client.upload_file(filename1, bucket_name, filename);

request = sqs_client.send_message(
	QueueUrl = input_queue.url,
	MessageBody = 'request',
	DelaySeconds = 10,
	MessageAttributes = {
		'Photo' : {
			'StringValue': filename,
			'DataType': 'String'
		}
	}
)

while True:
		print(".")
		message = sqs_client.receive_message(
		    QueueUrl=output_queue.url,
		    MessageAttributeNames=['response'],
		    MaxNumberOfMessages=1,
		    WaitTimeSeconds=1,
		)
		if 'Messages' in message:
			if message['Messages'][0]['Body'] == "FAILED":
				print("FAILED - Pay at the Window")
			else:
				print("Welcome "+ message['Messages'][0]['MessageAttributes']['response']['StringValue'])
			remove = sqs_client.delete_message(QueueUrl=output_queue.url, ReceiptHandle = message['Messages'][0]['ReceiptHandle'])
			break