# MetOS - Autonomous AI Agent

## Overview
MetOS is an AI-driven autonomous system that:
- Self-improves by analyzing logs and modifying its own code.
- Generates secure **Bitcoin, Ethereum, and Solana wallets**.
- Executes Python scripts safely.
- Provides a FastAPI-based interface for external integrations.

## Features
### ✅ AI-Powered Self-Improvement
- Uses **GPT-4** to analyze performance logs and suggest improvements.
- Automatically updates its own code based on LLM feedback.

### ✅ Cryptocurrency Wallet Generation
- Generates **Bitcoin, Ethereum, and Solana** wallets.
- Only returns public keys (no private key leaks).
- Saves wallet addresses to `/wallets/` securely without overwriting data.

### ✅ Secure Code Execution
- Runs Python scripts and captures output.
- Ensures only safe `.py` files are executed.

## Installation
### **1. Clone Repository**
```bash
git clone https://github.com/netzo92/MetOS.git
cd metos
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Set Up Environment Variables**
Create a `.env` file in the `config/` directory:
```ini
OPENAI_API_KEY=your_openai_key
```

### **4. Run MetOS**
```bash
python main.py
```

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/execute/` | POST | Run a Python script securely |
| `/analyze/` | POST | Analyze logs and suggest improvements |
| `/update/` | POST | Modify and update code dynamically |
| `/generate_wallets/` | POST | Generate BTC, ETH, and SOL wallets |

## Security Considerations
- **No private keys** are ever exposed.
- All wallet data is **appended** to prevent overwriting.
- Execution of non-Python scripts is **blocked**.

## Contributing
Feel free to submit issues and pull requests to improve MetOS.

## License
MIT License
