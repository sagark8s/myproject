
from utils.utils import console,kill_after
from langchain.chat_models import AzureChatOpenAI
from .openai_config import load_openai
from langchain import  LLMChain, PromptTemplate
from langchain.callbacks import get_openai_callback
from text_qna.qna import TextQnA
import os
from utils.utils import api_sleep

''' Query pipeline imports'''
from database.samodels import insert_chat_to_db,get_latest_id



openai=load_openai()
llm_conv=AzureChatOpenAI(deployment_name='chatbot-sql-generation',model_name=os.getenv('OPENAI_MODEL_NAME'),temperature=0.0,max_tokens=2000)

@api_sleep(1)
def optimize_query(pipeline,config):
    ''' To prevent request overload to openai server'''

    ''' we are only passing user questions '''
    tokens=0
    optimize_prompt = config.GetOptimizationPrompt(pipeline.history)
    console.log(optimize_prompt,style='red')
    if len(pipeline.history)>1:
        optimize_message =[{'role':'system','content':optimize_prompt}]
        completion = openai.ChatCompletion.create(
        engine='chatbot-sql-generation',
        messages=optimize_message,
        temperature=0,
        max_tokens=200,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
        result = completion.choices[0]['message']['content'].lower()
        tokens = completion['usage']['total_tokens']
    else:
        result = pipeline.latest_query
        tokens = 0
    pipeline.latest_query = result.lower()
    pipeline.load_stats(query_=result,answer_=result,data_points_=f"For optimize layer - {pipeline.latest_query}",
                        thought_=optimize_prompt,stage_='optimize_layer',token_=tokens)
    
    return pipeline

@api_sleep(1)
def classify_user_query(pipeline,config):
    console.log("Running Classifcation Query : langchain",style='green1')
    ''' to save across api calls '''

    prompt = PromptTemplate(input_variables=["human_input"], template=config.CLASSIFER_PROMPT_TEMPLATE)

    chatgpt_chain = LLMChain(llm=llm_conv,prompt=prompt)
    with get_openai_callback() as cb:
        output = chatgpt_chain.predict(human_input=pipeline.answer[-1])
    classify_flag = True
    if 'class_2' in output and 'class_1' in output:
        pass
    elif 'class_1' in output:
        classify_flag = False
        pipeline.latest_query = output.replace('class_1','').replace(':','')
    pipeline.load_stats(query_=pipeline.history[-1]['user'],data_points_=f"For classify layer - {pipeline.latest_query}"
                        ,answer_=output.lower(),thought_=config.CLASSIFER_PROMPT_TEMPLATE,stage_='classify_layer',token_=cb.total_tokens)
   
    return pipeline,classify_flag

''' Runnning pipeline for conversation '''
''' Steps within pipeline , query optimization , entity recognition , Tabular + Expert Analysis '''
@kill_after(60)
def run_query_pipeline(pipeline,configs):

    ''' Optimize query layer '''
    pipeline = optimize_query(pipeline,configs['conversation'])
    console.log(f'Finished optimizing query : {pipeline.latest_query}',style='green')
    ''' Query Classification layer '''
    #pipeline,flag = classify_user_query(pipeline,config=configs['conversation'])
    #if not flag:
    #    return pipeline
    pipeline = TextQnA(pipeline,configs['text_qna'])
    return pipeline
    





  