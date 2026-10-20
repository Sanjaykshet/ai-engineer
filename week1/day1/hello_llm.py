import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
my_api_key=os.getenv("GORQ_API_KEY")
if not my_api_key:
    raise ValueError("api error")

sanjay = Groq(api_key=my_api_key)
# model = "llama-3.3-70b-versatile"
model = "openai/gpt-oss-120b"
role="user"
prompt="do you know about virat kohli"
message={
    "role":role,
    "content":prompt
}
messages = [message] # store each request in list 
response = sanjay.chat.completions.create(model=model,messages=messages)
#print(response)
print(response.choices[0].message.content)
