from locust import HttpUser,task,between
import random
from rich.console import Console
console = Console()
questions = ['What are the hotels in seychelles?','Who founded Seychelles?','show me some good seafood restraunts in La Digue','What are the popular Languages']
def get_api_payload():
    return {"history":[{"user":random.choice(questions)}],"approach":"rrr","overrides":{"semantic_ranker":True,
                                                                                      "semantic_captions":False,"top":3,"suggest_followup_questions":False}}
class QuickstartUser(HttpUser):
    wait_time = between(1, 2)
    def on_start(self):
        print('started')

    @task
    def predict_test(self):
        try:
            global count
            json_data = get_api_payload()
            result = self.client.post("/chat", json=json_data)
            console.log(f"request : {json_data} | result: {result.text}",style='green')
            console.log('#'*10,style='red')
        except Exception as e:
            print(e)

#{"history":[{"user":"Show me some hotels?"}],"approach":"rrr","overrides":{"semantic_ranker":true,"semantic_captions":false,"top":3,"suggest_followup_questions":false}}
