# Sentence Bert model

from sentence_transformers.util import cos_sim  
from sentence_transformers import SentenceTransformer as SBert

# load pretrained model
model = SBert('paraphrase-multilingual-MiniLM-L12-v2')

def similarity(s1, s2):
    embeddings1 = model.encode(s1)
    embeddings2 = model.encode(s2)

    # Compute cosine-similarits
    return float(cos_sim(embeddings1, embeddings2))