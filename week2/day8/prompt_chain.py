import os
from pathlib import Path
from dotenv import load_dotenv
import time
from groq import Groq
load_dotenv()


my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("api key error")
client = Groq(api_key = my_api_key)
model = "openai/gpt-oss-120b"

JD = """"
    we are hiring web developer.
    requiements:
    -react.js
    -html,css,js
    -git
    -node.js
    -designing
    -Restapis  
    should have worked on minminum of 2 projects 
"""
RESUME="""
    NAME : sachin
    COLLEGE : sdmcet
    CGPA : 9.12
    EXPERICNCE: Fresher
    SKILLS : react.js,node.js,rest-api,java,c++,git,html,css,js
    PROJECTS : build sign language detection system and developed a web application for voting system
"""

def llm_call(sys_prompt,usr_prompt):
    sys_msg={
            "role" : "system",
            "content":sys_prompt
        }
    user_msg={
        "role" : "user",
        "content":usr_prompt
    }
    messages = [sys_msg,user_msg]
    response = client.chat.completions.create(model = model,messages=messages)
    result = response.choices[0].message.content
    return result
    
    
def step_1_extract_resume(resume):
    system_prompt = """
    you are hr assistant your job is to extract the skills from provided resume 
    return only the mentioned skills do not add your own"""
    user_prompt = f"""
    extract only skills form resume with  comma separated values:{resume}"""
    
    return llm_call(system_prompt,user_prompt)
    
def step_2_extract_jb(jd):
    system_prompt = """
    you are hr assistant your job is to extract the skills from provided Job_description 
    return only the mentioned skills do not add your own"""
    user_prompt = f"""
    extract the skills form jd with  comma separated values:{jd}"""
        
    return llm_call(system_prompt,user_prompt)
    
def step_3_match_skills(res,sys):
    system_prompt="""
    act as hr assistant .your job is to match the skills of the candidate against the job description and show what all skills are matched and at last proivde a score out of 10 based on the matches and provide a short comment about the candidate dont provide any unnecessary information"""
    user_prompt=f"""
    compare jd :{JD} with candidates resume:{RESUME}"""
    return llm_call(system_prompt,user_prompt)


candidate = step_1_extract_resume(RESUME)
print(candidate)
time.sleep(1)
job_des = step_2_extract_jb(JD)
print(job_des)
time.sleep(1)
response = step_3_match_skills(candidate,job_des)
print(response)