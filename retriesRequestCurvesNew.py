import boto3
import time
import random
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

def requestCurves(refDate: str, resource: any, source: str, limit: int = 50, max_retries: int = 9, base_delay: float = 0.1) -> list:
    if source not in sources.keys():
        return {'statusCode': 500, 'message': 'Source {} not found'.format(source), 'data': ''}

    try:
        table = resource.Table(sources[source]['curves'])
    except Exception as e:
        return {'statusCode': 500, 'message': str(e), 'data': ''}

    scan_kwargs = {
        'FilterExpression': Attr('refDate').eq(refDate),
        'Limit': limit,
    }

    paginator = resource.meta.client.get_paginator('scan')
    page_iterator = paginator.paginate(
        TableName=sources[source]['curves'],
        **scan_kwargs
    )

    curves = []
    retries = 0

    try:
        for page in page_iterator:
            while retries <= max_retries:
                try:
                    curves.extend(page.get('Items', []))
                    break
                except ClientError as e:
                    if e.response['Error']['Code'] == 'ProvisionedThroughputExceededException':
                        retries += 1
                        delay = base_delay * (2 ** retries) + random.uniform(0, base_delay)
                        time.sleep(delay)
                    else:
                        return {'statusCode': 500, 'message': str(e), 'data': ''}
    except Exception as e:
        return {'statusCode': 500, 'message': str(e), 'data': ''}

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
