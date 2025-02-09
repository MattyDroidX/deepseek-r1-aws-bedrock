#!/bin/bash

# Exit script on any error
set -e

# Define your S3 bucket name and region
BUCKET_NAME="deepseek-r1-distill-llama-8b"  # Replace with your actual S3 bucket name
REGION="us-east-1"  # Modify as needed

# Create the S3 bucket
echo "Creating S3 bucket: $BUCKET_NAME in region: $REGION..."
aws s3 mb s3://$BUCKET_NAME --region $REGION

# Sync the model files to the S3 bucket
echo "Uploading model files to S3..."
aws s3 sync --exclude '.git*' DeepSeek-R1-Distill-Llama-8B s3://$BUCKET_NAME/DeepSeek-R1-Distill-Llama-8B/

echo "Upload complete!"

