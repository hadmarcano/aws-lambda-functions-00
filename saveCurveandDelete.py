import boto3
from bootstrapprocess.savelogs import serialize
from datetime import datetime


def saveCurves(results: list, table: str = 'cf-discount-curves') -> None:
    client = boto3.client('dynamodb')
    updatedAt = datetime.now().isoformat(sep='T', timespec='auto')
    for result in results:
        result['updatedAt'] = updatedAt        
        client.put_item(TableName=table, Item=serialize(result))
    return None
