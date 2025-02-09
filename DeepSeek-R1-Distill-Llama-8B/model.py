from huggingface_hub import snapshot_download

model_id = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
local_dir = snapshot_download(repo_id=model_id, local_dir="DeepSeek-R1-Distill-Llama-8B")