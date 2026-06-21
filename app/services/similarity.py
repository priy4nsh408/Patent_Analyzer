from sentence_transformers import SentenceTransformer, util
from app.config import EMBEDDING_MODEL_NAME
from app.utils.preprocessing import preprocess

# This service supports any Sentence Transformer checkpoint provided by
# EMBEDDING_MODEL_NAME. The default is now all-MiniLM-L12-v2 for stronger
# prototype accuracy without sacrificing CPU-friendly performance.
# Alternatives for further experiments include:
# - all-mpnet-base-v2
# - GiacomoSignorile/PatentBert-FineTuned
# - other patent-specialised SentenceTransformers checkpoints
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def compute_similarity(user_input, patent):
    user_input = preprocess(user_input)

    # Better patent text combination
    patent_text = preprocess(
        patent.get("title", "") + " " +
        patent.get("abstract", "") + " " +
        patent.get("claims", "")
    )

    # Generate embeddings
    emb1 = model.encode(user_input, convert_to_tensor=True)
    emb2 = model.encode(patent_text, convert_to_tensor=True)

    # Cosine similarity
    score = util.cos_sim(emb1, emb2).item() * 100

    return round(score, 2)