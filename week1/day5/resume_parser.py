import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
import time
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("api key not found error")

client = Groq(api_key = my_api_key)
model = "openai/gpt-oss-120b"

job_description = """
We’re seeking a skilled and motivated IT engineer to join our team at [Company X].

As an IT Engineer, you will be responsible for installing, configuring, and supporting various IT infrastructures and tools, ensuring that all technology works efficiently, securely, and is properly maintained. The ideal candidate has a solid technical background and the ability to manage complex IT systems, troubleshoot issues, and ensure smooth operation of all hardware, software, and network systems.

If you are passionate about IT infrastructure and enjoy solving complex technical challenges, we invite you to apply for the position. We offer a dynamic work environment, growth opportunities, and comprehensive benefits to help you thrive in your career. 

Objectives of this role
Designing, configuring, and maintaining network infrastructures and IT systems to ensure optimal performance, connectivity, and security.
Ensuring data security by implementing firewalls, antivirus software, and other security measures to prevent unauthorised access.
Managing and troubleshooting server environments, cloud platforms, and network systems to ensure maximum uptime.
Performing regular backups, system updates, and monitoring system performance for potential problems.
Monitoring network performance and resolving any connectivity or network issues that arise.
Collaborating with other teams to integrate new technologies and systems into the existing infrastructure.
Documenting IT procedures, configurations, and troubleshooting steps to create a knowledge base for the team.
Providing technical IT support to staff and resolving IT-related issues quickly and efficiently.
Your tasks
Monitor and maintain IT infrastructure, including server uptime, network speed, and security protocols.
Install and set up new computer systems, servers, workstations, applications, and other equipment based on company needs.
Respond to user-reported technical issues and resolve problems related to hardware, software, or network connectivity.
Perform regular diagnostics and troubleshooting to identify and fix system errors or inefficiencies.
Ensure regular backup and recovery of critical business data, setting up disaster recovery protocols when necessary.
Implement software updates, patches, and security fixes to protect systems from vulnerabilities.
Assist in migrating IT infrastructure to cloud platforms or integrating new systems into the organisation.
Maintain detailed records of network configurations, incidents, and maintenance schedules.
Keep up with industry trends and technological advancements to recommend improvements and updates to the organisation’s systems.
Required skills and qualifications
Bachelor’s degree in Computer Science, Information Technology, Engineering, or a related field.
3-5 years of experience in IT support, system/network administration, or a similar role.
Strong understanding of IT systems, networks, hardware, and software.
Experience with network management tools, server administration, and cloud platforms.
Knowledge of networking protocols, such as TCP/IP, DNS, HTTP, etc.
Familiarity with firewalls, VPNs, and other security systems.
Proficiency in operating systems (Windows, Linux, Mac OS), networking protocols, and system monitoring tools.
Solid knowledge of cybersecurity practices and tools in India and globally.
Experience with cloud computing platforms like AWS, Google Cloud, or Microsoft Azure.
Problem-solving skills and the ability to diagnose and resolve technical issues quickly.
Excellent problem-solving and communication skills to interact effectively with non-technical teams and end users.
Ability to work independently and as part of a team to support IT functions and projects.
Preferred skills and qualifications
Relevant professional certifications, such as Cisco Certified Network Associate (CCNA), CompTIA Network+, or Microsoft Certified Solutions Expert (MCSE).
Familiarity with virtualisation technologies like VMware or Hyper-V.
Knowledge of IT automation tools and scripting (Python, PowerShell, Bash).
Experience with database management systems (SQL, MySQL).
Ability to design and deploy solutions for business continuity and disaster recovery.
Project management skills, especially in IT infrastructure projects.
Experience with security-focused certifications like Certified Information Systems Security Professional (CISSP) or Certified Ethical Hacker (CEH).
Familiarity with ITIL framework and service management principles.
Ability to manage multiple projects and prioritise tasks effectively.

"""
from pydantic import BaseModel
class JobD(BaseModel):
    role:str
    required_skills:list[str]
    preferred_skills:list[str]
    minimum_experience:float |None
    eduacation_requirements:list[str]
    responsibilites:list[str]

jobd_schema = JobD.model_json_schema()

system_prompt = f"""
act as expert hr 
your job is to analyze the job description  and extract structured information from it
provide valid json format matching this schema{jobd_schema}

important:
do not return the schema itself
also dont return unnecessary fields
fill the schema with actual information extracted from job_description
do not produce any information on your own
 
"""

user_prompt=f"""
analyze the following job description
{job_description}
"""
system_message ={
    "role":"system",
    "content":system_prompt
}
user_message={
    "role":"user",
    "content":user_prompt
}
response_format = {
    "type":"json_object"
}
messages = [system_message,user_message]
response = client.chat.completions.create(model = model,messages= messages,response_format = response_format) # llm call 1
ans = response.choices[0].message.content
# print(ans)

raw_json = ans

import json
data_file = json.loads(raw_json)
jd = JobD(**data_file)

class MatchResult(BaseModel):
    score:float
    details:dict

result_schema = MatchResult.model_json_schema()
    
class Experience(BaseModel):
    company:str|None = None
    role:str|None = None
    duration:str|None = None
    skills_acquired:list[str]= []


class resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    total_experience_years: float | None = None
    skills: list[str] = []
    experiences: list[str] = []
    education: list[str] = []
    projects: list[str] = []
    certifications: list[str] = []
    
resume_schema = resume.model_json_schema()



def final_score(jd,resume):
    prompt = f"""
        you are hr recruiter 
        comapre the resume against job description 
        and provide score and details my comparing job_description and student_resume and give output in json format that matches this scheme{result_schema}
        -details
        1.skills
        2.exprience
        3.projects
        4.education 
        5.final verdict
        
        
        -job description:{jd.model_dump_json(indent =2)}
        -candidates resume:{resume.model_dump_json(indent = 2)}
        
        at last provide a small verdit about the resume
        keep the response in easy to readable format
    """
    
    message ={
        "role":"user",
        "content":prompt
    }
    response_format={
        "type":"json_object"
    }
    messages = [message]
    response = client.chat.completions.create(model = model,messages = messages,temperature=2,response_format=response_format)
    raw_ans = response.choices[0].message.content
    ans = json.loads(raw_ans)
    final_ans = MatchResult(**ans)
    
    return final_ans
    
    
def parse_resume(resume_text):
    system_prompt = f"""
        act as expert resume parser and extract info based on resume_text 
        each resumes will be different so analyze each one of them according to their described section
        For example:
        -education
        -skills
        -projects 
        -experience
        -other ciricular activites
        
        return response in json format that follows resume schema {resume_schema}
    
    """
    user_prompt = f"""
    parse the following resume {resume_text}
    """
    message_system={
        "role" : "system",
        "content" : system_prompt
    }
    message_user={
        "role" : "user",
        "content" : user_prompt
    }
    messages=[message_system, message_user]
    response_format={
        "type": "json_object"
    }
    response=client.chat.completions.create(model=model, messages=messages, response_format=response_format)
    raw_output = response.choices[0].message.content
    data = json.loads(raw_output)
    r = resume(**data)
    return r
    
from pypdf import PdfReader
from docx import Document

def readPdf(file_path):
    pdf = PdfReader(file_path)
    text=""

    for pages in pdf.pages:
        page_text = pages.extract_text()
        if page_text:
            text+=page_text+"\n"
    return text

def readWord(file_path):
    doc = document(file_path)
    text = ""
    for para in doc.paragraph:
        if para.text.strip():
            text+=para.text + "\n"

    for table in doc.tables:
        for row in table.rows():
            for cell in row.cells():
                if cell.text.strip():
                    text+=cell.text + "\n"
                    
    return text
def read_resume(file_path):
    if file_path.suffix.lower() == ".pdf":
        return readPdf(file_path)
    elif file_path.suffix.lower() == ".word":
        return readWord(file_path)
    else:
        return None
    
    
resume_folder = Path("Resumes")
results = []
for file_path in resume_folder.iterdir():
    if file_path.suffix.lower() not in [".pdf",".docx"]:
        continue
    resume_text = read_resume(file_path)
    parsed_text = parse_resume(resume_text) #llm call 2
    time.sleep(5)
    result = final_score(jd,parsed_text) # llm call 3
    time.sleep(5)
    print(result.score)
    results.append({
        "name":parsed_text.name,
        "score":result.score,
        "details":result.details
    })
    
    
print("Full result:", result)
    
