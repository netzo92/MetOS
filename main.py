import os
import subprocess
import yaml
import time
import secrets
from openai import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from fastapi import FastAPI
from dotenv import load_dotenv
from bitcoinlib.wallets import Wallet
from eth_account import Account
from solders.keypair import Keypair

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load mission config
with open("config/mission.yaml", "r") as f:
    MISSION_CONFIG = yaml.safe_load(f)

# Initialize LLM
client = OpenAI(api_key=OPENAI_API_KEY)

def save_wallet_info(wallet_type, pubkey):
    """Saves wallet information to /wallets without overwriting existing files."""
    os.makedirs("wallets", exist_ok=True)
    file_path = os.path.join("wallets", f"{wallet_type}_wallets.txt")
    with open(file_path, "a") as f:
        f.write(f"{pubkey}\n")

def generate_btc_wallet():
    """Generates a new Bitcoin wallet."""
    wallet = Wallet.create('metos_btc_wallet')
    pubkey = wallet.address
    save_wallet_info("btc", pubkey)
    return pubkey

def generate_eth_wallet():
    """Generates a new Ethereum wallet."""
    acct = Account.create()
    pubkey = acct.address
    save_wallet_info("eth", pubkey)
    return pubkey

def generate_solana_wallet():
    """Generates a new Solana wallet."""
    keypair = Keypair()
    pubkey = keypair.pubkey()
    save_wallet_info("solana", pubkey)
    return pubkey

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

@app.post("/generate_wallets/")
def generate_wallets():
    return {
        "btc_wallet": generate_btc_wallet(),
        "eth_wallet": generate_eth_wallet(),
        "solana_wallet": generate_solana_wallet()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

