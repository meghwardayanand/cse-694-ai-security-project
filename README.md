# Set up Project
1. Create .env file.
2. Add following details:
```
    OPENAI_API_KEY=sk-<your-open-ai-key>
    
    #DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/mydatabase
    DATABASE_URL=sqlite:///./demo.db

    echo 'export OPENAI_API_KEY=sk-<your-open-ai-key>' >> ~/.bashrc

```

# Create Environment Install Packages
1. Open terminal. (make sure you're in project directory & python 3 is installed)
2. Create environment with command `python3 -m venv .venv`
3. Activate environment with command `source .venv/bin/activate`
4. Upgrate pip with command `python -m pip install --upgrade pip`
5. Install requirements.txt with commands `pip install -r requirements.txt`
6. Execute `pip install -U langchain langchain-community sqlalchemy psycopg2-binary`
7. Execute `pip install langchain-experimental`
8. Download Ollama from: https://ollama.com/download
9. Install ollama with command: `pip install ollama-llm`
10. Verify with command: `ollama --version`
11. Download specific version with command: `ollama pull llama3.1`

# Activate Environment
Execute `source .venv/bin/activate` to activate the environment

# Run Program
Execute `python main.py`
