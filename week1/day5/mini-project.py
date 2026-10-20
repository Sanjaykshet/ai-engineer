import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

from pydantic import BaseModel
class resume(BaseModel):
    eligible: bool
    reason: str
    missing_requirements: str
    suggestions: str
    
schema = resume.model_json_schema()
response_format={
    "type":"json_object"
}
system_text = "cgpa should be above 8 and miminmum skill should be he should have mastered one programming language and should have experience of 6 months and he should have worked on aiml and java projects"
system_prompt = f""" 
act as hr and match the senders resume against the given list :{system_text} and Return the output in JSON format matching the provided schema.

Schema:{schema}
"""
system_message= {
    "role":"system",
    "content": system_prompt
}
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("api key not found")

sanjay =Groq(api_key = my_api_key)
model = "llama-3.3-70b-versatile"

role = "user"
user_text = "my name is rock studied from abc college of engineering and technology my cgpa is 8.5 out of 10.i have mastered react,dsa java and backend engineering understading.My experience is i am fresher who is looking for oppurtunity to upskill my self.During my engineering course i have worked on 3 projects .First one is based on web application and second one on machine learning,and finally java based cli project for better understanding of oops concepts.I actively participate in sports such as basketball and table tennis."
prompt = f"""
hey i have shared my resume{user_text} please check wheather i am eligible for this particular role/position and suggest me what needs to be added to match this given role
"""

message = {
    "role" :role,
    "content": prompt
}
messages = [system_message,message]

response = sanjay.chat.completions.create(model=model,messages=messages,response_format=response_format)
print(response.choices[0].message.content)
