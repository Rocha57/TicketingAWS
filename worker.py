import boto3

sqs = boto3.resource('sqs')
sqs_client = boto3.client('sqs')

s3 = boto3.resource('s3')
bucket_name = 'esproject3bucket'
bucket_register_name = 'esproject3bucketregister'

client_s3 = boto3.client('s3')
client_db = boto3.client('dynamodb')
client_rek = boto3.client('rekognition')

table_name = 'project3'

input_queue = sqs.get_queue_by_name(QueueName='project3_input')
output_queue = sqs.get_queue_by_name(QueueName='project3_output')

def run():
	while True:
		print(".")
		message = sqs_client.receive_message(
		    QueueUrl=input_queue.url,
		    MessageAttributeNames=['Name','Photo'],
		    MaxNumberOfMessages=1,
		    WaitTimeSeconds=1,
		)
		if 'Messages' in message:
			remove = sqs_client.delete_message(QueueUrl=input_queue.url, ReceiptHandle = message['Messages'][0]['ReceiptHandle'])
			table_items = client_db.scan(
		    	TableName=table_name
			)
			name = rekognition(message['Messages'][0]['MessageAttributes']['Photo']['StringValue'], table_items)
			if name == None:
				send_message(output_queue, "ardeu", "FAILED")
			else:
				send_message(output_queue, name, "SUCCESS")

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

def rekognition(filename, table_items):
	for item in table_items['Items']:
		response = client_rek.compare_faces(
			SourceImage={
        		'S3Object': {
	            'Bucket': bucket_name,
	            'Name': filename,
       			}
    		},
		    TargetImage={
		        'S3Object': {
		            'Bucket': bucket_register_name,
		            'Name': item['filename']['S'],
		        }
		    },
		    SimilarityThreshold=90
		)
		if  response['FaceMatches']:
			print(response['FaceMatches'][0]['Similarity'])
			if response['FaceMatches'][0]['Similarity'] > 90:
				return item['name']['S']
	return None

if __name__ == "__main__":
	run()