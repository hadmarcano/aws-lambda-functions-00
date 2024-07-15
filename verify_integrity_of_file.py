import hashlib
   
    # snsInfo = processEvent(event)
    # print("snsContext",snsInfo)
    
     # Expected hash value (pre-computed SHA-256 hash of the file)
expected_hash = 'your_precomputed_sha256_hash_value'
   
def verify_file_integrity(file_data, expected_signature):
       
       
    # Compute the SHA256 hash of the file data
    file_hash = hashlib.sha256(file_data).hexdigest()
    
    # Compare the computed hash with the expected signature
    return file_hash == expected_signature
   
    # try:
    
    #     # Get report file from bbg s3
    #     file = gettingReportFile()
        
    #     # Compute SHA-256 hash of the file content
    #     sha256_hash = hashlib.sha256(file).hexdigest()
        
    #     # Verify the hash
    #     if sha256_hash == expected_hash:
    #         return {
    #         'statusCode': 200,
    #         'body': 'File integrity verified. Hash matches.'
    #         }
    #     else:
    #         return {
    #         'statusCode': 400,
    #         'body': 'File integrity check failed. Hash does not match.'
    #         }
    
    # except Exception as e:
    #     return {
    #         'statusCode': 500,
    #         'body': f'An error occurred: {str(e)}'
    #         }
    
    # "{\"type\": \"ArchivePublishedActivity\", \"endedAtTime\": \"2022-06-10T19:00:48.435348\", \"generated\": {\"type\": \"Archive\", \"identifier\": \"equityMifidEuroHistoricalPricing.20220610.parquet\", \"contentType\": \"Parquet\", \"key\": \"Xjx6tvrO/catalogs/bbg/datasets/equityMifidEuroHistoricalPricing/archives/equityMifidEuroHistoricalPricing.20220610.parquet\", \"contentEncoding\": null, \"contentLength\": 3011859, \"digest\": {\"type\": \"Digest\", \"digestValue\": \"4dfd1abc1ac1bb18f6269ac2aea54529cdd0ec73f0f0135b9d3bfb9bacee71f9fed1b7ab3d0cdabf7dbea247e29c0400d87859ac272d47b4e6eb7f07db822a19\", \"digestAlgorithm\": \"SHA512\"}, \"S3AccessPointARN\": \"arn:aws:s3:us-east-1:695011528394:accesspoint/dl-catalog-123456\", \"eTag\": \"\\\"68eb4f87c0f94cbc638e65bccee37a36\\\"\", \"status\": \"ongoing\", \"startDate\": \"2022-06-10\", \"issued\": \"2022-06-10T18:49:30.440000+00:00\", \"dataset\": {\"type\": \"Dataset\", \"identifier\": \"equityMifidEuroHistoricalPricing\", \"catalog\": {\"type\": \"Catalog\", \"identifier\": \"bbg\"}}, \"endDate\": \"2022-06-10\"}}"