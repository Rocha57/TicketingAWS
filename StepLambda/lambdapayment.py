import boto3

client_db = boto3.client('dynamodb')
table_name = 'project3'

def lambda_handler(event, context):
    user = event['name']
    cost = event['cost']
    response = client_db.get_item(
		TableName = table_name,
		Key = {
			'name': {
				'S': user
			}
		},
		AttributesToGet=['credit']
	)
	correct = 0
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
    		correct = 1
    return {'correct' : correct}