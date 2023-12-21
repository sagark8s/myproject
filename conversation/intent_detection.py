"""Intent detection module based on openai function calling module"""
# from openai import AzureOpenAI
from openai import AzureOpenAI
from conversation.examples import ( greeting_and_general_knowledge_examples,
                                    financial_data_examples,
                                    trend_and_historical_data_examples,
                                    application_help_guide_faq_examples,
                                    )   
import json

messages = [
    {
        "role": "system",
        "content": "You are an AI assistant whose role is select a function based on the user's input. \
     You are given a list of functions and their descriptions. Select a function which best matches the user_input.",
    },
]

functions = [
    {
        "name": "greeting_and_general_knowledge",
        "description": f"When the user_input is a greeting or a general knowledge question or a polite expression or thank you.If the user_input is also \
        not related to any of the other categories, please call this function.examples of questions - {greeting_and_general_knowledge_examples}",
        "parameters": {
            "type": "object",
            "properties": {
                "user_input": {"type": "string", "description": "The question asked by the user"},
            },
            "required": ["user_input"],
        },
    },
    {
        "name": "financial_data",
        "description": f"When the user_input is a a financial question or the user_input looking for financial data. Give most preference to this function.\
        Also when the user_input is looking for current year or \
        the last year data.\
        \nExamples - {financial_data_examples}",
        "parameters": {
            "type": "object",
            "properties": {
                "user_input": {"type": "string", "description": "The question asked by the user"},
            },
            "required": ["user_input"],
        },
    },
    {
        "name": "trend_and_historical_data",
        "description": f"When the user_input contains `trend` or is looking for the past 2-5 years related data or also user_input contains `past n years` or `previous n years`.\
        This function has to be called when the \
        data the user_input is looking for is in 2022 and before.\
        , please call this function. \nExamples - {trend_and_historical_data_examples}",
       "parameters": {
            "type": "object",
            "properties": {
                "user_input": {"type": "string", "description": "The question asked by the user"},
            },
            "required": ["user_input"],
        },
    },
    {
        "name": "application_help_guide_faq",
        "description": f"When the user_input is looking for help or guide or faq and how to use the application.\
        examples. - {application_help_guide_faq_examples}",
        "parameters": {
            "type": "object",
            "properties": {
                "user_input": {"type": "string", "description": "The question asked by the user"},
            },
            "required": ["user_input"],
        },
    },
]

client = AzureOpenAI(api_key="74d66ba999504ea1a0fbdcf4c44f9637",
                    api_version="2023-10-01-preview",
                    azure_endpoint="https://covalenseazureopenaiuks.openai.azure.com/",
                    )


def detect_intent(pipeline):
    """intent detection function based on openai function calling module

    Args:
        user_input (_type_): _description_

    Returns:
        _type_: _description_
    """
    global messages
    global functions
    years = ["2018", "2019", "2020", "2021", "2022"]
    user_input = pipeline.latest_query
    messages += [{"role": "user", "content": user_input}]
    response = client.chat.completions.create(model="chatbot-sql-generation-16k",  # model = "deployment_name"
                                                messages=messages,
                                                functions=functions,
                                                function_call="auto",
                                                )

    function_name = json.loads((response.choices[0].message.model_dump_json(indent=2)))["function_call"]["name"]
    pipeline.load_stats(query_=pipeline.latest_query,
                        answer_=function_name, #The result of this layer.
                        data_points_="Classify the question into either greeting , financial current year data , trend and historical data or application help guide faq",
                        thought_=messages[0]['content'],
                        stage_="Intent Detection",
                        token_=response.usage.total_tokens,
                        )

    print(function_name)

    #sometimes if financial_data is used then , we need to pass to trend and histor data
    if function_name=='financial_data' and any(year in user_input for year in years):
        function_name='trend_and_historical_data'

    #if trend is present in the user_input then we need to pass to trend and historical data
    if 'trend' in pipeline.latest_query.lower():
        function_name='trend_and_historical_data'
    return function_name