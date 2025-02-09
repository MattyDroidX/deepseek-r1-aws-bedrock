# Deploying DeepSeek-R1-Distill-Llama-8B on AWS Bedrock with FastAPI and React

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step 1: Clone the Model Repository from Hugging Face](#step-1-clone-the-model-repository-from-hugging-face)
4. [Step 2: Configure AWS Services](#step-2-configure-aws-services)
5. [Step 3: Upload the Model to S3](#step-3-upload-the-model-to-s3)
6. [Step 4: Import the Model into Amazon Bedrock](#step-4-import-the-model-into-amazon-bedrock)
7. [Step 5: Test the Model with Python](#step-5-test-the-model-with-python)
8. [Step 6: Develop a FastAPI Backend](#step-6-develop-a-fastapi-backend)
9. [Step 7: Create a React Frontend](#step-7-create-a-react-frontend)
10. [Estimated Cost Breakdown](#estimated-cost-breakdown)
11. [Conclusion](#conclusion)

## Overview

This guide provides a step-by-step walkthrough for deploying the DeepSeek-R1-Distill-Llama-8B model on AWS Bedrock. It includes:

- Cloning the repository containing the model.
- Configuring AWS services (S3 bucket and Amazon Bedrock credentials).
- Uploading the model to S3 and importing it into Amazon Bedrock.
- Testing the model using a Python script.
- Enhancing the deployment with a FastAPI backend and a React-based user interface.

## Prerequisites

Ensure you have the following:

- An AWS account with appropriate permissions.
- AWS CLI installed and configured.
- Python installed.
- Basic knowledge of FastAPI and React.

## Step 1: Clone the Model Repository from Hugging Face

### 1.1 Install Git LFS (if not already installed)

```bash
# For Ubuntu/Debian
sudo apt install git-lfs

# For macOS (using Homebrew)
brew install git-lfs

# For Windows (using Chocolatey)
choco install git-lfs
```

Enable Git LFS:

```bash
git lfs install
```

### 1.2 Clone the Repository

```bash
git clone https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B
cd DeepSeek-R1-Distill-Llama-8B
```

### 1.3 Pull Large Files

```bash
git lfs pull
```

This ensures all model files are downloaded correctly.

## Step 2: Configure AWS Services

### 2.1 Set Up AWS CLI

```bash
aws configure
```

Provide AWS Access Key ID, Secret Access Key, and set the default region to `us-east-1`.

### 2.2 Set Up Amazon Bedrock Credentials

Create an IAM role with:

- `AmazonBedrockFullAccess`
- `AmazonS3FullAccess`

Attach this role to your AWS account.

## Step 3: Upload the Model to S3

The `upload_to_s3.sh` script will automatically create the S3 bucket (if it does not already exist) and then upload the model files.

```bash
chmod +x upload_to_s3.sh
./upload_to_s3.sh
```

This script will:

- Create an S3 bucket named `deepseek-r1-distill-llama-8b` in the `us-east-1` region.
- Upload all model files from the `DeepSeek-R1-Distill-Llama-8B` directory to the S3 bucket.

## Step 4: Import the Model into Amazon Bedrock

1. Navigate to Amazon Bedrock in the AWS Console.
2. Import the model using the S3 URI: `s3://deepseek-r1-distill-llama-8b/DeepSeek-R1-Distill-Llama-8B/`.
3. Deploy the model.

## Step 5: Test the Model with Python

Once the model is imported and deployed in Amazon Bedrock, you can use `invoke_new_model.py` to test its functionality.

### 5.1 Install Dependencies

```bash
pip install boto3
```

### 5.2 Run the Script

```bash
python invoke_new_model.py
```

### 5.3 What This Script Does

The `invoke_new_model.py` script:

- Initializes an AWS Bedrock runtime client.
- Uses the correct provisioned model ID to invoke the model.
- Sends a prompt to the model (`"Provide a one-sentence summary of Albert Einstein's achievements."`).
- Returns and prints the model’s response.

The expected output will be a concise summary generated by the deployed model.

## Step 6: Develop a FastAPI Backend

### 6.1 Install Dependencies

```bash
pip install fastapi uvicorn
```

### 6.2 Create `main.py`

```python
from fastapi import FastAPI
import boto3

app = FastAPI()

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

@app.post("/predict/")
async def predict(prompt: str):
    response = bedrock.invoke_model(
        modelId='your-model-id',
        contentType='application/json',
        accept='application/json',
        body=prompt
    )
    result = response['body'].read().decode('utf-8')
    return {"response": result}
```

### 6.3 Run the FastAPI Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Step 7: Create a React Frontend

### 7.1 Set Up React App

```bash
npx create-react-app deepseek-ui
cd deepseek-ui
```

### 7.2 Implement UI in `App.js`

```jsx
import React, { useState } from "react";

function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch("http://localhost:8000/predict/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });
    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} />
        <button type="submit">Submit</button>
      </form>
      <div>{response}</div>
    </div>
  );
}

export default App;
```

### 7.3 Run the React App

```bash
npm start
```

## Estimated Cost Breakdown

### AWS Bedrock Pricing

- The cost per 1M tokens varies by model; for DeepSeek-R1-Distill-Llama-8B, the estimated cost is **$0.002 per token**.
- Since each response generates **512 tokens**, the cost per response would be **$1.024**.

### S3 Storage Pricing

- Amazon S3 standard storage costs **$0.023 per GB per month**.
- Model storage size can vary; assuming **10GB**, monthly storage cost is **$0.23**.

### Example Monthly Cost Estimate

- Assuming **100,000** queries per month:
  - Token cost: **$102,400** (100,000 \* $1.024 per response)
  - Storage cost: **$0.23**
- **Total estimated monthly cost: ~$102,400.23**

## Conclusion

You have successfully deployed the DeepSeek-R1-Distill-Llama-8B model on AWS Bedrock, set up a FastAPI backend, and built a React frontend to interact with the model. This setup enables scalable AI model hosting and usage, but careful cost estimation is recommended to optimize expenses.
