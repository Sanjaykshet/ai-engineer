import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
from pydantic import BaseModel

my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("api error")

sanjay = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"


class complaint(BaseModel):
    name:str
    email:str
    issue:str
    place:str
schema = complaint.model_json_schema()
response_format = {
    "type":"json_object"
}
system_prompt = f"""
return output in json format matching provided schema.{schema}
"""
system_role = "system" 
system_message={
    "role":system_role,
    "content": system_prompt
}

text = "hello my name is kobe from delhi. My complaint is that when is used headphones it doesnot work properly but some third person uses it ,it seems to work correctly. i request you to resolve this issue and if you need to communicate please contact to this email address abc@gmail.com"
prompt=f"""this is customer complaint please extract only necessary details about the message{text}"""
message={
    "role":"user",
    "content":prompt
}
messages = [system_message,message] # store each request in list 
response = sanjay.chat.completions.create(model=model,messages=messages,temperature=2,response_format =response_format)
#print(response) ## response is in object format meaning key-value pair
print(response.choices[0].message.content)

import json
raw_json = response.choices[0].message.content
data_file = json.loads(raw_json)
complaint_raised = complaint(**data_file)
print(complaint_raised.name)
print(complaint_raised.email)
print(complaint_raised.issue)
print(complaint_raised.place)
