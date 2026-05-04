from app.config import HIGH_THRESHOLD, MEDIUM_THRESHOLD

def classify_risk(score):
    if score > HIGH_THRESHOLD:
        return "High"
    elif score > MEDIUM_THRESHOLD:
        return "Medium"
    else:
        return "Low"