import boto3

s3 = boto3.resource('s3')
bucket_name = 'esproject3bucketregister'
client_db = boto3.client('dynamodb')
table_name = 'project3'

name = input('enter your name: ');
filename = input('enter filename of your photograph: ');
filename = 'photos/'+filename
credit = input('enter your initial credit: ');

s3.meta.client.upload_file(filename, bucket_name, filename);

response = client_db.put_item(
	TableName = table_name,
	Item = {
		'name': {
			'S': name
		},
		'filename': {
			'S': filename
		},
		'credit': {
			'N': credit
		}

	}
)