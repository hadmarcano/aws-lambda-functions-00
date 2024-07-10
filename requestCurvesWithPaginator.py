import boto3
from boto3.dynamodb.conditions import Attr

def requestCurves(refDate: str, resource: any, source: str) -> list:
    if source not in sources.keys():
        return {'statusCode': 500, 'message': 'Source {} not found'.format(source), 'data': ''}

    try:
        table = resource.Table(sources[source]['curves'])
    except Exception as e:
        return {'statusCode': 500, 'message': str(e), 'data': ''}

    scan_kwargs = {
        'FilterExpression': Attr('refDate').eq(refDate),
    }

    paginator = resource.meta.client.get_paginator('scan')
    page_iterator = paginator.paginate(
        TableName=sources[source]['curves'],
        **scan_kwargs
    )

    curves = []
    try:
        for page in page_iterator:
            curves.extend(page.get('Items', []))
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


# 1-element_to_delete {'statusCode': 500, 'message': "Parameter validation failed:\nInvalid type for parameter TableName, value: dynamodb.Table(name='cf-discount-curves'), type: <class 'boto3.resources.factory.dynamodb.Table'>, valid types: <class 'str'>\nInvalid type for parameter ExpressionAttributeValues.:updatedAt, value: 2024-06-30T19:47:04.964826, type: <class 'str'>, valid types: <class 'dict'>", 'data': ''}