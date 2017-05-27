import boto3
import time

s3 = boto3.resource('s3')
bucket_name = 'esproject3bucket'

filename = input('enter filename of your photograph: ');
cost = input('enter the value: ')
filename1 = 'photos/'+filename
s3.meta.client.upload_file(filename1, bucket_name, filename);

client = boto3.client('stepfunctions')
response = client.start_execution(
	stateMachineArn='arn:aws:states:eu-west-1:124607185617:stateMachine:esproject3',
	name=str(time.time()),
	input='{"filename": "'+filename+'","cost":'+cost+'}'
)

while True:
	time.sleep(1)
	result = client.describe_execution(
	    executionArn=response['executionArn']
	)
	try:
		if result['status'] == 'RUNNING':
			pass
		else:
			print(result['output'])
			break
	except:
		print("ardeu")
		break