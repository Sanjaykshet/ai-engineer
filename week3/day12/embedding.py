import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
import numpy as np
from sentence_transformers import SentenceTransformer
load_dotenv()
# from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def cosine_similarity(a,b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )
t1 = "she is very beautyfull"
t2 = "she is beautyfull"


e1 = model.encode(t1)
e2 = model.encode(t2)

print(cosine_similarity(e1, e2))