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
prompt="my is abc from xyz i graudated form qwe my cpa is 9.9 and my skills are dsa,react,node.js,rest-api and blender "
system_message={
    'role':"system",
    'content':"act as company recruiter can check wheather the user is suitable for any kind of job"
}
message={
    "role":role,
    "content":prompt
}
messages = [system_message,message] # store each request in list 
response = sanjay.chat.completions.create(model=model,messages=messages,temperature=1.3)
#print(response)
print(response.choices[0].message.content)
