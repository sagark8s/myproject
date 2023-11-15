import openai
import os
openai.api_type = "azure"
openai.api_base = "https://covalenseazureopenai.openai.azure.com/"
openai.api_version = "2023-07-01-preview" # this one has to be present its gpt3.5turbo
openai.api_key = "db6fbb176b0e44bca10ca4fc719689b5"
os.environ['OPENAI_API_KEY']=openai.api_key
os.environ['OPENAI_API_BASE']=openai.api_base
os.environ['OPENAI_API_VERSION']=openai.api_version
os.environ['OPENAI_DEPLOYMENT_NAME']=f'chatbot-gpt-prod'
os.environ['OPENAI_MODEL_NAME']=f'gpt-35-turbo'
def load_openai():
    return openai
