# **Deploying DeepSeek-R1 on AWS Bedrock with FastAPI & React**

## **📌 Overview**

This guide walks you through **importing and using DeepSeek-R1 on AWS Bedrock**, setting up a **FastAPI backend** to interact with the model, and building a **React frontend** to create a simple UI for testing it. We will also cover **IAM role setup, CORS fixes, and common AWS Bedrock issues** to help you successfully deploy and share your custom model.

We will be following the steps outlined in the AWS Community article on [Deploying DeepSeek-R1 on Amazon Bedrock](https://community.aws/content/2sECf0xbpgEIaUpAJcwbrSnIGfu/deploying-deepseek-r1-model-on-amazon-bedrock). This guide includes step-by-step details with **exact commands** to ensure everything works smoothly.

---

# **🔹 Step 1: AWS Bedrock Setup & IAM Configuration**

### **1️⃣ Configure AWS CLI**

Ensure your AWS CLI is set up and configured:

```bash
aws configure
```

Enter your:

- **AWS Access Key ID**
- **AWS Secret Access Key**
- **Region (us-east-1 recommended)**

Verify your setup:

```bash
aws s3 ls
```

This should list your S3 buckets if everything is configured correctly.

### **2️⃣ IAM Role & Permissions**

To use AWS Bedrock, you need an **IAM user with proper permissions**.

#### **Create a new IAM role with the following permissions:**

1. **AmazonBedrockFullAccess** – Grants access to AWS Bedrock services.
2. **AmazonS3FullAccess** – Enables access to S3 where models are stored.
3. **AdministratorAccess** – (Optional) Grants full AWS permissions.

Check IAM role assignment:

```bash
aws sts get-caller-identity
```

If your IAM user does not have Bedrock access, assign the **AmazonBedrockFullAccess** policy manually through the AWS console.

---

# **🔹 Step 2: Import DeepSeek-R1 Model to AWS Bedrock**

Unlike previous versions, AWS Bedrock now **only allows fine-tuning for custom models**, meaning the import **does not require deployment**.

### **1️⃣ List Available Imported Models**

```bash
aws bedrock list-imported-models --region us-east-1
```

This will return model details, including the **model ARN** you need.

### **2️⃣ Store Model ARN for Future Use**

From the above output, copy the `modelArn` of **DeepSeek-R1**.
Example:

```
arn:aws:bedrock:us-east-1:061051254608:imported-model/762nd8bmvux1
```

This will be used in the FastAPI backend.

---

# **🔹 Step 3: Setting Up FastAPI Backend**

### **1️⃣ Install Required Dependencies**

```bash
pip install fastapi uvicorn boto3 fastapi-cors
```

### **2️⃣ Create `app.py` Backend**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import boto3
import json
from pydantic import BaseModel

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = boto3.client("bedrock-runtime", region_name="us-east-1")
MODEL_ID = "arn:aws:bedrock:us-east-1:061051254608:imported-model/762nd8bmvux1"

class QueryRequest(BaseModel):
    prompt: str

@app.post("/generate/")
async def generate_text(request: QueryRequest):
    payload = {
        "prompt": request.prompt,
        "max_tokens_to_sample": 100,
        "temperature": 0.5,
        "top_p": 0.9,
        "stop_sequences": [".", "\n"]
    }
    response = client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(payload),
        accept="application/json",
        contentType="application/json"
    )
    result = json.loads(response["body"].read().decode("utf-8"))
    return {"response": result["generation"]}
```

### **3️⃣ Start the FastAPI Server**

```bash
uvicorn app:app --reload
```

✅ Now your backend is running at **`http://localhost:8000`**

---

# **🔹 Step 4: Setting Up React Frontend**

### **1️⃣ Create React App**

```bash
npx create-react-app deepseek-ui
cd deepseek-ui
npm install axios
```

### **2️⃣ Update `src/App.js`**

```javascript
import React, { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");

  const handleGenerate = async () => {
    if (!prompt) return;
    try {
      const res = await axios.post("http://localhost:8000/generate/", {
        prompt,
      });
      setResponse(res.data.response);
    } catch (error) {
      console.error("Error fetching response:", error);
      setResponse("Failed to generate response.");
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>DeepSeek-R1 Chat</h1>
      <textarea
        rows="4"
        cols="50"
        placeholder="Enter a prompt..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <br />
      <button onClick={handleGenerate} style={{ marginTop: "10px" }}>
        Generate
      </button>
      <h2>Response:</h2>
      <p>{response}</p>
    </div>
  );
}

export default App;
```

### **3️⃣ Start React Frontend**

```bash
npm start
```

✅ UI available at **`http://localhost:3000`**

---

🚀 **Enjoy using DeepSeek-R1 on AWS Bedrock!** 🎉
