import os
import subprocess
import yaml
import time
from openai import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load mission config
with open("config/mission.yaml", "r") as f:
    MISSION_CONFIG = yaml.safe_load(f)

# Initialize LLM
client = OpenAI(api_key=OPENAI_API_KEY)

def run_file(file_path):
    """Executes a Python file and returns the output."""
    if not os.path.exists(file_path):
        return f"❌ Error: File {file_path} not found."
    
    if not file_path.endswith(".py"):
        return "❌ Error: Only Python files (.py) can be executed."
    
    try:
        result = subprocess.run(["python3", file_path], capture_output=True, text=True, check=True)
        return f"✅ Output:\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"❌ Execution failed:\n{e.stderr}"

def analyze_performance():
    """Analyzes performance logs and suggests improvements."""
    with open("logs/self_analysis.log", "r") as log_file:
        logs = log_file.read()
    
    prompt = f"""
    You are an autonomous AI agent with a mission to self-improve.
    
    Mission: {MISSION_CONFIG['mission']['objective']}
    
    Logs:
    {logs}
    
    Suggest code updates to improve efficiency and accuracy.
    """
    
    response = client.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def update_code(file_path, pattern, replacement):
    """Replaces a section of a script with new code."""
    with open(file_path, "r") as f:
        content = f.read()
    
    content = content.replace(pattern, replacement)
    
    with open(file_path, "w") as f:
        f.write(content)
    
    print(f"✅ Successfully modified {file_path}")

def restart_metos():
    """Restarts MetOS after updates."""
    print("🚀 Restarting MetOS with new modifications...")
    time.sleep(2)
    subprocess.run(["systemctl", "restart", "metos"])  # Example using systemd

# API
app = FastAPI()

@app.post("/execute/")
def execute_script(file_path: str):
    return {"output": run_file(file_path)}

@app.post("/analyze/")
def analyze():
    return {"improvements": analyze_performance()}

@app.post("/update/")
def update(file_path: str, pattern: str, replacement: str):
    update_code(file_path, pattern, replacement)
    return {"status": "Code updated successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
