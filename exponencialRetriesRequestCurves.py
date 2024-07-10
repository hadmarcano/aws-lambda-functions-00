import boto3
import time
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

def requestCurves(refDate: str, resource: any, source: str) -> list:
    if source not in sources.keys():
        return {'statusCode': 500, 'message': 'Source {} not found'.format(source), 'data': ''}

    try:
        table = resource.Table(sources[source]['curves'])
    except Exception as e:
        return {'statusCode': 500, 'message': str(e), 'data': ''}

    scan_kwargs = {
        'FilterExpression': Attr('refDate').eq(refDate),
        'Limit': 100  # Limit the number of items returned per scan operation
    }

    done = False
    start_key = None
    curves = []
    retries = 0
    max_retries = 9

    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key

        try:
            response = table.scan(**scan_kwargs)
            retries = 0  # Reset retries after a successful scan
        except ClientError as e:
            if e.response['Error']['Code'] == 'ProvisionedThroughputExceededException':
                if retries < max_retries:
                    retries += 1
                    sleep_time = (2 ** retries) * 0.1  # Exponential backoff
                    time.sleep(sleep_time)
                    continue
                else:
                    return {'statusCode': 500, 'message': 'Max retries exceeded', 'data': ''}
            else:
                return {'statusCode': 500, 'message': str(e), 'data': ''}

        curves.extend(response.get('Items', []))
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None

    for c in curves:
        if 'curveType' not in c.keys():
            c['curveType'] = 'Discount'
        if 'dayCounter' not in c.keys():
            c['dayCounter'] = 'Actual360'

    if curves:
        return curves
    
    else:
        return {
            'statusCode': 404,
            'message': 'No curves found for refDate {}'.format(refDate),
            'data': []
        }

# Example usage:
# dynamodb = boto3.resource('dynamodb')
# result = requestCurves('2023-07-01', dynamodb, 'mySource')
