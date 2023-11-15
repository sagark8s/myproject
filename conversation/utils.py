import tiktoken

def num_tokens_from_string(text, encoding_name='gpt-4'):
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(text['content']))
    return num_tokens
def format_message(messages,limit=7000):
    system_message=messages[0]
    system_message_len = num_tokens_from_string(system_message)
    total_message_len = system_message_len
    formatted_messages = []
    for i in messages[:0:-1]:
        total_message_len = total_message_len + num_tokens_from_string(i)
        if total_message_len<=limit:
            formatted_messages.append(i)
        else:
            break
    return [system_message]+formatted_messages[::-1]


def get_chat_history_as_text(history,specific_role=None):
    messages=[]
    for i in range(len(history)-1):
        messages.append({'role':'user','content':history[i]['user']})
        system='assistant'
        if i==(len(history)-2):
            system='assistant'
        messages.append({'role':system,'content':history[i]['bot']})
    else:
        messages.append({'role':'user','content':history[-1]['user']})
    if specific_role=='user':
        user_messages =[]
        for i in messages:
            if i['role']=='user':
                user_messages.append(i)
        print(user_messages)
        return user_messages
    return messages