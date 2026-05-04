def similarity_type(user_input, patent):
    u = user_input.lower()
    p = (patent["abstract"] + patent["claims"]).lower()

    if any(w in u for w in ["system", "method"]) and any(w in p for w in ["system", "method"]):
        return "Functional Similarity"
    elif any(w in u for w in ["sensor", "device"]) and any(w in p for w in ["sensor", "device"]):
        return "Structural Similarity"
    else:
        return "Conceptual Similarity"