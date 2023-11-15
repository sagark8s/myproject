import openai
openai.api_type = "azure"
openai.api_base = "https://covalenseazureopenaiuks.openai.azure.com/"
openai.api_version = "2023-07-01-preview" # this one has to be present its gpt3.5turbo
openai.api_key = "74d66ba999504ea1a0fbdcf4c44f9637"
def load_openai():
    return openai

