import boto3
import json

# Initialize the Bedrock Runtime client
client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Use the correct provisioned model ID
model_id = 'arn:aws:bedrock:us-east-1:061051254608:imported-model/762nd8bmvux1'
prompt = "Provide a one-sentence summary of Albert Einstein's achievements."

# Invoke the model with the corrected parameters
response = client.invoke_model(
    modelId=model_id,
    body=json.dumps({'prompt': prompt}),
    accept='application/json',
    contentType='application/json'
)

# Parse and print the response
result = json.loads(response['body'].read().decode('utf-8'))
print(result)
