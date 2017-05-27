import boto3
client_db = boto3.client('dynamodb')
client_rek = boto3.client('rekognition')
table_name = 'project3'
bucket_name = 'esproject3bucket'
bucket_register_name = 'esproject3bucketregister'

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
		if response['FaceMatches']:
			print(response['FaceMatches'][0]['Similarity'])
			if response['FaceMatches'][0]['Similarity'] > 90:
				return item['name']['S']
	return None

def lambda_handler(event, context):
	# TODO implement
	filename = event['filename']
	cost = event['cost']
	table_items = client_db.scan(TableName=table_name)
	name = rekognition(filename, table_items)
	correct = 0
	if name != None:
		correct = 1
	return {'name' : name, 'cost' : str(cost), 'correct' : correct}