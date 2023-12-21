from .pg_semantic_search import semantic_search
from .openai_config import load_openai
from langchain.chat_models import AzureChatOpenAI
from utils.utils import console,api_sleep
from concurrent.futures.thread import ThreadPoolExecutor as pool
import re
openai = load_openai()
engine = 'chatbot-sql-generation'
llm=AzureChatOpenAI(deployment_name='chatbot-sql-generation',model_name='gpt-35-turbo-16k',temperature=0.0,max_tokens=4000)

def call_openai(messages,temperature=0):
    return openai.ChatCompletion.create(
            engine=engine,
            messages=messages,
            temperature=temperature,
            max_tokens=1000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None)

def clean_answer(answer):
    try:
        https_links =  re.findall(r'https?://[^\s,\!\(\)]+',  answer)
        for link in https_links:
            try:
                new_link = f'<a href="{link}" target="_blank">{link}</a>'
                answer = answer.replace(link,new_link)
            except:pass
        return answer
    except Exception as e:
        print("Exception:",e)
        return answer
    
@api_sleep(1)
def TextQnA(pipeline,config):
    latest_result = ''
    tool_token_count = 0
    def set_latest_result(content):
        nonlocal latest_result
        latest_result = content
    def get_latest_result():
        nonlocal latest_result
        return latest_result

    console.log('Started semantic search',style='red')
    semantic_search_result,map_url,related_links = semantic_search(pipeline.latest_query)
    #console.log(semantic_search_result,style='yellow')
    console.log('Finished semantic search',style='red')
    QNA_PROMPT = config.QNA_PROMPT.format(content=semantic_search_result)
    # print("51 QNA_PROMPT :",QNA_PROMPT)
    messages = [{'role':'system','content':QNA_PROMPT},{'role':'user','content':pipeline.latest_query}]
    completion = openai.ChatCompletion.create(
    engine=engine,
    messages=messages,
    temperature=1,
    max_tokens=1000,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None)
    result = completion.choices[0]['message']['content']
    result = clean_answer(result)
    if map_url!='':
        map_url = f"""<a href="{map_url}" target="_blank">Map</a>"""
        result = f"{result} \n Please check the locations on map {map_url}"
    if related_links!='':
        result = f"{result} \n<b>Related Links</b>:{related_links}"
    pipeline.load_stats(query_=pipeline.latest_query,answer_=result,
                        data_points_=f"Question and answer - {semantic_search_result}"
                ,thought_=QNA_PROMPT,stage_='Question and answer',token_=completion['usage']['total_tokens'])
    console.log(result)
    return pipeline


def facebook_result(text):
    console.log('Started semantic search',style='red')
    semantic_search_result,map_url,related_links = semantic_search(text)
    console.log('Finished semantic search',style='red')
    
    facebook_PROMPT="""content:
                        /*
                        You are a expert on seychelles. You role is to answer questions based on the content provided.
                        Response should not exceed 1950 words.
                        If the user is looking for places to visit or tours to plan , please suggest them places to visit and activities to do.
                        If the user is looking for general information , please answer them only that information.
                        If the user is looking for FAQ on seychelles website , please guide them to the website.
                        Below is the content for the question asked.
                        {content}
                        */
                        For bulletin points please display using <ul> and <li> tags.
                        Please answer the user in their preferred language.
                        The answer should be in bulletins.
                        Always return the url provided to the user.
                        Always Answer should not exceed 1950 words.
                        Please suggest places to visit also depending on your own knowledge.
                        """
    facebook_PROMPT = facebook_PROMPT.format(content=semantic_search_result)
    messages = [{'role':'system','content':facebook_PROMPT},{'role':'user','content':text}]
    
    completion = openai.ChatCompletion.create( engine=engine,messages=messages,temperature=1,max_tokens=1000,
                                                top_p=0.95,frequency_penalty=0,presence_penalty=0,stop=None)
    result = completion.choices[0]['message']['content']
    result = clean_answer(result)
    return result

def recommended_query(pipeline_obj):
    print("288 pipeline_obj :",pipeline_obj)
    pipeline_obj = pipeline_obj
    chat_history = []

    system_prompt = """You are an expert in BERT model. Your role is to generate recommended queries based on a user's previous response. The user has just asked: "{user_response}".
                    1.Please generate three questions related to the previous response that would be beneficial for further learning.
                    2.Always return only recommended queries in a list.
                    3.Avoid repeating questions that the user has already asked.
                    4. Don't ask the question, where solution is already provided in the answer. Please use your own intelligence before generating the question
                    5.If the response includes multiple categories or brands, modify the questions accordingly to each specific category or brand.
                """
    print("129 openai :",openai)

    system_message = {'role': 'system', 'content': system_prompt}
    chat_history.append(system_message)

    user_message = {'role': 'user', 'content': pipeline_obj}
    chat_history.append(user_message)
    # request = openai.ChatCompletion.create(engine="chatbot-sql-generation", model="gpt-3.5-turbo", messages=chat_history)
    request = openai.ChatCompletion.create(engine=engine, model="gpt-3.5-turbo", messages=chat_history)
    result = request.choices[0]['message']['content'].strip()
    result = result.split('\n')
    result = result[1:]
    result = [query.strip('1234567890. ') for query in result if query.strip('1234567890. ')]
    return result