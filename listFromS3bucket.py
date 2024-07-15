import json
import boto3
import os

def lambda_handler(event, context):
    # Initialize the S3 client
    s3 = boto3.client('s3')
    
    # Retrieve the bucket name from an environment variable or directly
    bucket_name = os.getenv('BUCKET_NAME', 'your-bucket-name')
    
    # List objects in the specified S3 bucket
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        
        # Extract the file names
        if 'Contents' in response:
            files = [obj['Key'] for obj in response['Contents']]
        else:
            files = []
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'files': files
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
