from sentence_transformers import SentenceTransformer, util
from app.utils.preprocessing import preprocess

# Load model once (VERY IMPORTANT)
model = SentenceTransformer('all-MiniLM-L6-v2')

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