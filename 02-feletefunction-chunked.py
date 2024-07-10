import boto3
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Attr

def deleteOldRecords(table_name: str = 'cf-discount-curves') -> None:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    # Calculate the date 10 days ago
    cutoff_date = datetime.now() - timedelta(days=10)
    cutoff_date_iso = cutoff_date.isoformat(sep='T', timespec='auto')
    
    scan_kwargs = {
        'FilterExpression': Attr('updatedAt').lt(cutoff_date_iso)
    }
    
    done = False
    start_key = None
    items_to_delete = []

    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
            
        response = table.scan(**scan_kwargs)
        items_to_delete.extend(response.get('Items', []))
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    
    # Optionally, process the items to delete
    # for item in items_to_delete:
    #     print(f"Deleting item with key: {item['PrimaryKey']}")
    #     table.delete_item(Key={'PrimaryKey': item['PrimaryKey']})

    return items_to_delete

# Example usage
deleted_items = deleteOldRecords()
print(f"Items to delete: {deleted_items}")
