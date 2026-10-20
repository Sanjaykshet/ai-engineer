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

messages = [
    {
        "role": "system",
        "content": "Answer in one or two lines only."
    }
]
knowledge_base={
    "age":"age of sanjay is 23",
    "profession":"he is artist",
    "language":"he knows kannada and hindi language"
}

def retrieve(question):
    question = question.lower()
    if "age" in question:
        return knowledge_base["age"]
    elif "profession" in question:
        return knowledge_base["profession"]
    elif "language" in question:
        return knowledge_base["language"]
    else:
        return "no data available about this figure"
def ask_llm(question):
    
    answer = retrieve(question)
    messages.append({
        "role":"system",
        "content":f"""provide result based on provided context {answer}"""
    })
    messages.append({
        "role": "user",
        "content": question
    })

    response = sanjay.chat.completions.create(model=model,messages=messages)
    answer = response.choices[0].message.content

    messages.append({
        "role": "assistant",
        "content": answer
    })

    print(answer)

ask_llm("what is  sanjay's job")


