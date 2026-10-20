import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
import numpy as np
from sentence_transformers import SentenceTransformer
load_dotenv()


my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("api error")

sanjay = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"
emb_model = SentenceTransformer("all-MiniLM-L6-v2")

def cosine_similarity(a,b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

documents = [
    "basket ball was started in early 1800",
    
    "bill russel is successfull player with 11 rings between 1950s and 1970 ",
    
    "bill russel played for celtics team",
    
    "next most successfull player was micheal jordan with 6 rings and never ever lost a final before 2000",
    
    "after 2000 kobe bryant was named greatest player who played for lakers along-side shaqO'neal ",
    "currently basketball has become a soft game where players are left freely to shot ",
    "people say that steph curry is greatest player in this generation besides lebron james and kevin durant"
]

embeddings = emb_model.encode(documents)

def retrieve(q_emd):
    scores = []
    for i,doc in enumerate(embeddings):
        score = cosine_similarity(q_emd,doc)
        scores.append((score,documents[i]))
    scores.sort(reverse=True)
    return scores[0]


def ask_llm(question,context):
    sys_prompt=f"""Answer in one or two lines only.provide result based on provided  Context: {context} do not add anything on your own"""
    system_message={
        "role": "system",
        "content": sys_prompt

    }
    message={
        "role": "user",
        "content": question
    }
    messages=[system_message, message]
    response=sanjay.chat.completions.create(model=model, messages=messages)
    answer=response.choices[0].message.content
    return answer

   

question = "what perspective do people have about basketball in current era"
q_emd = emb_model.encode(question)
score,ans = retrieve(q_emd)
final_ans = ask_llm(question,ans)
print(final_ans)

