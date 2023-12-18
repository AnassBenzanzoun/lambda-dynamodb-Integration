import boto3
import json
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('users')

    try:
        # Determine the operation
        operation = event['queryStringParameters']['operation']

        if operation == 'create':
            item = json.loads(event['body'])
            table.put_item(Item=item)
            return {
                'statusCode': 200,
                'body': json.dumps('Item created.')
            }

        elif operation == 'read':
            uuid = event['queryStringParameters']['uuid']
            response = table.get_item(Key={'pk': uuid})
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])
            }

        elif operation == 'update':
            uuid = event['queryStringParameters']['uuid']
            update_expression = event['queryStringParameters']['update_expression']
            expression_attribute_values = json.loads(event['body'])
            table.update_item(
                Key={'pk': uuid},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
            return {
                'statusCode': 200,
                'body': json.dumps('Item updated.')
            }

        elif operation == 'delete':
            uuid = event['queryStringParameters']['uuid']
            table.delete_item(Key={'pk': uuid})
            return {
                'statusCode': 200,
                'body': json.dumps('Item deleted.')
            }

        else:
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid operation.')
            }

    except ClientError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(str(e))
        }