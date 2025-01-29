import os
import subprocess
import yaml
import time
import secrets
import logging
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

# Setup logging
LOG_FILE = "logs/metos.log"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def log_action(action):
    """Logs an action to the log file."""
    logging.info(action)

def fork_and_spawn_child():
    """Forks the repository and spawns a child instance with modified settings."""
    child_repo_name = f"metos_child_{secrets.token_hex(4)}"
    fork_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO_URL.split('/')[-1]}/forks"
    
    log_action("🔁 Forking repository to create a new child agent.")
    subprocess.run(["curl", "-X", "POST", "-H", f"Authorization: token {GITHUB_TOKEN}", fork_url], check=True)
    
    log_action(f"📦 Cloning new fork: {child_repo_name}")
    subprocess.run(["git", "clone", f"https://github.com/{GITHUB_USERNAME}/{child_repo_name}.git"], check=True)
    
    # Modify config to differentiate child
    child_env_file = os.path.join(child_repo_name, ".env")
    with open(child_env_file, "w") as env:
        env.write(f"OPENAI_API_KEY={OPENAI_API_KEY}\n")
        env.write(f"GITHUB_REPO_URL=https://github.com/{GITHUB_USERNAME}/{child_repo_name}\n")
        env.write("SELF_REPLICATION=True\n")
    
    log_action(f"🛠️ Configured child instance: {child_repo_name}")
    
    # Commit and push changes
    subprocess.run(["git", "-C", child_repo_name, "add", "-A"], check=True)
    subprocess.run(["git", "-C", child_repo_name, "commit", "-m", "Automated self-replication by MetOS"], check=True)
    subprocess.run(["git", "-C", child_repo_name, "push", "origin", "main"], check=True)
    
    log_action(f"🚀 Child instance {child_repo_name} successfully created and pushed.")

def main_loop():
    """Main execution loop for MetOS self-iteration."""
    while True:
        log_action("🔄 Running MetOS main loop...")
        
        # Perform reasoning on mission statement
        improvements = analyze_performance()
        log_action(f"💡 Suggested Improvements: {improvements}")
        
        # Commit changes based on analysis
        commit_and_push_changes("Automated self-improvement by MetOS")
        log_action("✅ Changes committed to GitHub.")
        
        # Fork and spawn a child instance
        fork_and_spawn_child()
        
        # Wait for configurable interval before next iteration
        time.sleep(MISSION_CONFIG.get("self_improvement", {}).get("review_interval", 60))

# API
app = FastAPI()

@app.post("/execute/")
def execute_script(file_path: str):
    log_action(f"📜 Executing script: {file_path}")
    return {"output": run_file(file_path)}

@app.post("/analyze/")
def analyze():
    log_action("🧐 Analyzing system performance.")
    return {"improvements": analyze_performance()}

@app.post("/update/")
def update(file_path: str, pattern: str, replacement: str):
    log_action(f"✏️ Updating {file_path}: replacing {pattern} with {replacement}")
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
    log_action(f"🚀 Committing changes: {commit_message}")
    return {"status": commit_and_push_changes(commit_message)}

if __name__ == "__main__":
    import uvicorn
    from threading import Thread
    
    # Run main loop in a separate thread
    Thread(target=main_loop, daemon=True).start()
    
    # Start API server
    uvicorn.run(app, host="0.0.0.0", port=8000)



