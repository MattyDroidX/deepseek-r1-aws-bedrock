import boto3
import os

s3_client = boto3.client('s3', region_name='us-east-1')
bucket_name = 'deepseek-r1-distill-llama-8b-test'
local_directory = 'DeepSeek-R1-Distill-Llama-8B'

for root, dirs, files in os.walk(local_directory):
    for file in files:
        local_path = os.path.join(root, file)
        s3_key = os.path.relpath(local_path, local_directory)
        s3_client.upload_file(local_path, bucket_name, s3_key)