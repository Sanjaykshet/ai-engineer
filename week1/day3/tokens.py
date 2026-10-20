import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("api error")

sanjay = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"
role="user"
prompt1="hi ai"
prompt2="explain any tough dsa topic"
prompt3="write a 100 words paragragraph on current situation on unemployment"

prompts = [prompt1,prompt2,prompt3]
for prompt in prompts:
    message={
    "role":role,
    "content":prompt
    }
    messages = [message] # store each request in list 
    response = sanjay.chat.completions.create(model=model,messages=messages,temperature=1.3,max_tokens=60)
    usage = response.usage
    print(f"Prompt :{prompt} ========> response:{response.choices[0].message.content}")
    print(f"prompt-tokens:{usage.prompt_tokens} completion-tokens:{usage.completion_tokens } total_tokens:{usage.total_tokens} finish_reason:{response.choices[0].finish_reason}")
    
# if stoped naturally it will show stop and if abruptly it will say length
# also if the ans is big and tokens are limited it will trip and provide the ans until the use of suggested token   

#messages = [message] # store each request in list 
#response = sanjay.chat.completions.create(model=model,messages=messages,temperature=1.3)
#print(response)

