# LLM_Kickstart
This contains simple modules to kickstart your learning path for LLMs, LangGraph and RAG

Setup
1. Download and Install Ollama on Windows
   
•	Go to Ollama’s official website.
•	Download the Windows installer (.exe file).
•	Run the installer and follow the setup instructions.
•	After installation, restart your system if required.
________________________________________
2. Verify the Installation
   
Open Command Prompt (cmd) or PowerShell and run:
```ollama list```
If Ollama is installed correctly, this command should return a list of installed models (or an empty list if no models are downloaded yet).
________________________________________
3. Pull the Required Model
   
Since your script uses Eomer/gpt-3.5-turbo, download the model by running:
```ollama pull Eomer/gpt-3.5-turbo```
```ollama run Eomer/gpt-3.5-turbo```
Wait for the model to finish downloading.
________________________________________
4. Continue with Python Setup
   
Once Ollama is installed, proceed with setting up your Python environment and installing dependencies as mentioned before:
```python -m venv venv```
```venv\Scripts\activate```
```pip install streamlit langchain langchain-community chromadb sentence-transformers pypdfs pypika chromadb```

Then, run your Streamlit app:
```streamlit run chatbot.py```
