import boto3
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Attr

def deleteOldRecords(table_name: str = 'cf-discount-curves') -> None:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    # Calculate the date 10 days ago
    cutoff_date = datetime.now() - timedelta(days=10)
    cutoff_date_iso = cutoff_date.isoformat(sep='T', timespec='auto')
    
    # Initialize the DynamoDB client and paginator
    client = boto3.client('dynamodb')
    paginator = client.get_paginator('scan')
    
    # Define the scan parameters
    scan_params = {
        'TableName': table_name,
        'FilterExpression': 'updatedAt < :cutoff_date',
        'ExpressionAttributeValues': {
            ':cutoff_date': {'S': cutoff_date_iso}
        }
    }
    
    # Paginate through all scan results
    for page in paginator.paginate(**scan_params):
        for item in page['Items']:
            table.delete_item(
                Key={
                    'primaryKeyAttribute': item['primaryKeyAttribute']['S'],  # Replace with your primary key attribute
                    'sortKeyAttribute': item['sortKeyAttribute']['S']  # Include sort key if applicable
                }
            )

# Example usage
deleteOldRecords()
