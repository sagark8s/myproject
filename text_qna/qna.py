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
