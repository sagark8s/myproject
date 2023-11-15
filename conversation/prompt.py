''' This is the classifier prompt template which is fired at the beginning of the conversation to determine the user intention '''
CLASSIFER_PROMPT_TEMPLATE = """
human_input : {human_input}

You role is to classify human_input into 2 classes-

class_1: A greeting or personal question or question about you or a question about general knowledge or a polite expression about you or a compliment.
class_2: If the user input contains a question or topic related to finance, investments, money management, or any financial matters or reports. If it contains comparision or performance related questions also.
if you are not able to determine which class it is then classify it as class_1.

Please follow this format without deviation to generate response-
human_input response,class of human_input
"""

CHAT_OPTIMIZATION_PROMPT ="""
    chat_history={chat_history}
    latest_question={latest_question}
    optimized_question=
    You need to optimize the latest_question based on chat_history provided.
    Please follow these steps to do your role-
    1.You will need to see if they are relevant to the questions asked by user in chat_history.
    2.if the question is relevant or a continuation of chat_history then optimize the latest_question , else return the latest_question as optimized_question.
    3.If the optimized_question can't be improved any further please output the
    latest_question as the optimized_question.
    4.If you are unsure about what to do , output latest_question as optimized_question.
    5.Please do not explain yourself or ask the user anything if you are unsure.
    6.Please generate the optimized question only and nothing else."""