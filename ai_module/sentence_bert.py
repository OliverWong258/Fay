# Sentence Bert model

from sentence_transformers.util import cos_sim  
from sentence_transformers import SentenceTransformer as SBert, util
import torch

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("SBert running on", device)
# load pretrained model
model = SBert('paraphrase-multilingual-MiniLM-L12-v2').to(device)

def similarity(s1, s2):
    embeddings1 = model.encode(s1, convert_to_tensor=True)
    embeddings2 = model.encode(s2, convert_to_tensor=True)

    # Compute cosine-similarits
    return float(util.pytorch_cos_sim(embeddings1, embeddings2))

# compute the cosine similarity in a batch in order to accelerate
def batch_similarity(target, texts):
    target_embedding = model.encode(target, convert_to_tensor=True)
    text_embeddings = model.encode(texts, convert_to_tensor=True)
    
    similarities = util.pytorch_cos_sim(target_embedding, text_embeddings)
    
    return similarities.cpu().numpy()
