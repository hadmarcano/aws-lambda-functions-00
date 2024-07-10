import boto3
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Attr

def deleteOldRecords(table_name: str = 'cf-discount-curves') -> None:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    # Calculate the date 10 days ago
    cutoff_date = datetime.now() - timedelta(days=10)
    cutoff_date_iso = cutoff_date.isoformat(sep='T', timespec='auto')
    
    # Scan items with 'updatedAt' attribute older than the cutoff date
    response = table.scan(
        FilterExpression=Attr('updatedAt').lt(cutoff_date_iso)
    )
    
    items_to_delete = response.get('Items', [])
    
    # Delete each item
    while 'Items' in response and response['Items']:
        for item in response['Items']:
            table.delete_item(
                Key={
                    'primaryKeyAttribute': item['primaryKeyAttribute'],  # Replace with your primary key attribute
                    'sortKeyAttribute': item['sortKeyAttribute']  # Include sort key if applicable
                }
            )
        
        # Check if there are more items to scan
        if 'LastEvaluatedKey' in response:
            response = table.scan(
                FilterExpression=Attr('updatedAt').lt(cutoff_date_iso),
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
        else:
            break
    
    return None

# Example usage
deleteOldRecords()
