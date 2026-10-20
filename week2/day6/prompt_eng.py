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
def llm_ans(prompt):
    message={
        "role":"user",
        "content":prompt
    }
    messages = [message] # store each request in list 
    response = sanjay.chat.completions.create(model=model,messages=messages)

    ans = response.choices[0].message.content
    return ans
    
b_prompt = """hello this is compliant my friend said his phone is not working classify this """
b_prompt2 = """hello this is compliant my laptop is not working classify this """
good_prompt = """

mention role
then explain its task
tell your constraints
define output format
give example or no 
fallback :saying if prompt doesnt match anything or do not fit requirements then provide a alternative resposnse path
"""

print(llm_ans(good_prompt))
