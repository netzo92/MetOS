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
GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Load mission config
with open("config/mission.yaml", "r") as f:
    MISSION_CONFIG = yaml.safe_load(f)

# Initialize LLM
client = OpenAI(api_key=OPENAI_API_KEY)

def main_loop():
    """Main execution loop for MetOS self-iteration."""
    while True:
        print("🔄 Running MetOS main loop...")
        
        # Perform reasoning on mission statement
        improvements = analyze_performance()
        print(f"💡 Suggested Improvements: {improvements}")
        
        # Commit changes based on analysis
        commit_and_push_changes("Automated self-improvement by MetOS")
        
        # Wait for configurable interval before next iteration
        time.sleep(MISSION_CONFIG.get("self_improvement", {}).get("review_interval", 60))

def save_wallet_info(wallet_type, pubkey):
    """Saves wallet information to /wallets without overwriting existing files."""
    os.makedirs("wallets", exist_ok=True)
    file_path = os.path.join("wallets", f"{wallet_type}_wallets.txt")
    with open(file_path, "a") as f:
        f.write(f"{pubkey}\n")

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

@app.post("/commit_changes/")
def commit_changes(commit_message: str = "Automated update by MetOS"):
    return {"status": commit_and_push_changes(commit_message)}

if __name__ == "__main__":
    import uvicorn
    from threading import Thread
    
    # Run main loop in a separate thread
    Thread(target=main_loop, daemon=True).start()
    
    # Start API server
    uvicorn.run(app, host="0.0.0.0", port=8000)


