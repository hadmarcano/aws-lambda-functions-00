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
        'ExpressionAttributeValues': {':refDate': refDate},
    }

    done = False
    start_key = None
    curves = []

    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key

        try:
            response = table.scan(**scan_kwargs)
        except Exception as e:
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