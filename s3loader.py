import boto3
import json

def gettingReportFile(source: dict) -> dict:
    '''
    Get report file from external S3
    '''
    s3_client = boto3.client('s3')
    # Get object from S3
    response = s3_client.get_object(
        Bucket=source['bucket'], Key=source['key'])
    file_content = response['Body'].read()
    
    return file_content
    

def puttingReportFile(source: dict) -> dict:
    '''
    Put report file to internal S3
    '''
    s3_client = boto3.client('s3')
    
    try:
        # Put object into S3
        s3_client.put_object(Bucket=source['bucket'], Key=source['key'], body=source['file'])
        
        return {
                'statusCode': 200,
                'body': f'Success copied to {source['bucket']} in {source['key']}'
                }
    
    except Exception as e:
        
        return {
                'statusCode': 500,
                'body': f'Error processing to {source['bucket']} in {source['key']}'
                }

def listFiles():
    '''
    List files from external S3
    '''
    s3_client = boto3.client('s3')
    
    access_point_arn = 'arn:aws:s3:us-east-1:695011528394:accesspoint/dl-3b97f658-d6d3-41e6-96e2-612046047229'
    
    try:
        print("access_point_arn",access_point_arn)
        response = s3_client.list_objects_v2(access_point_arn)
        print("response_s3",response)
        
        return "Testing connection"
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
    