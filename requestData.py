# Getting data by batches
def requestCurves(refDate: str, resource: any, source: str) -> list:
    
    if source not in sources.keys():
        return {'statusCode':500, ' message':'Source {} not found'.format(source), 'data':''}
    
    try:
        table = resource.Table(sources[source]['curves'])
    except Exception as e:
        return {'statusCode':500, ' message':str(e), 'data':''}
    
    try:
        curves = table.scan(
            FilterExpression='refDate = :refDate',
            ExpressionAttributeValues={':refDate': refDate}
        )
    except Exception as e:
        return {'statusCode':500, ' message':str(e), 'data':''}

    if curves['Count'] > 0:
        for c in curves['Items']:
            if 'curveType' not in c.keys():
                c['curveType'] = 'Discount'
                if 'dayCounter' not in c.keys():
                    c['dayCounter'] = 'Actual360'
        return curves['Items']
    else:
        return {
            'statusCode':404,
            'message':'No curves found for refDate {}'.format(refDate, source),
            'data':[]
            }