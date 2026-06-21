import json
import random

# Seed for reproducibility
random.seed(42)

# Domain categories and related ideas/patents
domains = {
    "healthcare": {
        "ideas": [
            "A real-time patient monitoring system using wearable sensors",
            "A medication reminder app that tracks adherence",
            "A telehealth platform for remote diagnostics",
            "A robotic surgery assistant for precise incisions",
            "A disease screening tool using deep learning on medical images",
            "A smartwatch app that detects irregular heartbeat",
            "An AI-powered drug discovery system",
            "A hospital resource allocation optimizer",
            "A medical records encryption system",
            "A voice-activated emergency alert system for elderly",
        ],
        "patents": [
            ("Wearable Biometric Sensor Network", "Collects vital signs continuously", "Wireless transmission of health data"),
            ("Medication Management Platform", "Tracks pill intake through computer vision", "Sends alerts via SMS and app"),
            ("Remote Patient Consultation System", "Video calls with real-time health metric sharing", "Integration with EHR systems"),
            ("Precision Surgical Robot", "AI-guided incision trajectory planning", "Haptic feedback to surgeon"),
            ("Medical Image Analysis Engine", "Detects tumors and anomalies", "Generates diagnostic reports"),
            ("Cardiac Arrhythmia Detector", "Real-time ECG analysis", "Cloud-based alerting"),
            ("Pharmaceutical Research Accelerator", "Simulates molecular interactions", "Predicts drug efficacy"),
            ("Hospital Resource Management", "Predicts bed and OR availability", "Optimizes staff scheduling"),
            ("Healthcare Data Encryption", "End-to-end encryption for patient records", "Blockchain-based audit trail"),
            ("Emergency Response System", "Voice recognition for SOS triggering", "Automatic location sharing"),
        ],
    },
    "iot_smart_home": {
        "ideas": [
            "A system that controls lights based on circadian rhythm",
            "A smart door lock with facial recognition",
            "A home security system using radar sensors",
            "A water usage monitoring system for conservation",
            "A smart irrigation controller for gardens",
            "An AC system that predicts maintenance needs",
            "A voice assistant for home automation",
            "A smart refrigerator that orders groceries",
            "A motion-activated security camera system",
            "A smart window that adjusts tint based on sunlight",
        ],
        "patents": [
            ("Circadian Rhythm Lighting Control", "Adjusts color temperature throughout day", "Sync with occupancy sensors"),
            ("Facial Recognition Door Lock", "Matches faces against database", "Dual-factor authentication"),
            ("Radar-Based Security System", "Detects intruders through walls", "24/7 monitoring"),
            ("Smart Water Meter", "Real-time consumption tracking", "Alerts on anomalies"),
            ("IoT Irrigation System", "Weather-adaptive watering schedule", "Soil moisture sensors"),
            ("Predictive HVAC Maintenance", "ML-based failure prediction", "Automated service requests"),
            ("Voice-Controlled Home Automation", "Integrates multiple device types", "Natural language processing"),
            ("Smart Grocery Ordering Fridge", "Tracks inventory via weight sensors", "Auto-reorders staples"),
            ("AI-Powered Security Cameras", "Person detection and tracking", "Cloud and edge recording"),
            ("Electrochromic Smart Windows", "Auto-dimming glass technology", "Energy efficiency optimization"),
        ],
    },
    "transportation": {
        "ideas": [
            "A vehicle routing system that avoids congestion in real-time",
            "An autonomous shuttle service for campuses",
            "A parking lot management system using computer vision",
            "A vehicle battery diagnostic tool",
            "A traffic prediction system for city planning",
            "A fleet management system with predictive maintenance",
            "A ride-sharing app with dynamic pricing",
            "A vehicle-to-infrastructure communication system",
            "A drone delivery coordination platform",
            "A fuel efficiency tracking system for trucks",
        ],
        "patents": [
            ("Real-time Route Optimization Engine", "Calculates fastest paths dynamically", "Crowd-sourced traffic data"),
            ("Autonomous Campus Shuttle", "Self-driving vehicle for defined routes", "Passenger safety features"),
            ("Computer Vision Parking System", "Detects available spots automatically", "Mobile app integration"),
            ("EV Battery Health Monitor", "Predicts remaining battery life", "Optimization recommendations"),
            ("Urban Traffic Forecasting", "Deep learning traffic prediction", "Integration with traffic lights"),
            ("Fleet Maintenance Predictor", "Detects component wear patterns", "Optimizes maintenance schedule"),
            ("Dynamic Ride-Sharing Platform", "Adjusts prices based on demand", "Real-time matching algorithm"),
            ("V2X Communication Protocol", "Vehicle-to-road infrastructure messaging", "Collision avoidance alerts"),
            ("Drone Delivery Router", "Plans optimal delivery sequences", "Weather-aware path planning"),
            ("Fuel Economy Tracking System", "Monitor and optimize consumption", "Driver behavior scoring"),
        ],
    },
    "agriculture": {
        "ideas": [
            "A crop disease detection system using drone imagery",
            "A soil health monitoring platform",
            "A weather-based yield prediction model",
            "A precision fertilizer application system",
            "A pest detection and control system",
            "A livestock monitoring system using IoT collars",
            "An automated greenhouse control system",
            "A farm-to-market traceability system",
            "A water efficiency optimization platform",
            "A crop rotation recommendation engine",
        ],
        "patents": [
            ("Drone-Based Crop Analysis", "Detects disease and nutrient deficiency", "Real-time reporting to farmer"),
            ("Soil Composition Analyzer", "Measures pH, moisture, nutrients", "Recommendation engine"),
            ("Climate-Based Yield Forecaster", "Predicts harvest based on weather", "Historical data analysis"),
            ("Variable Rate Fertilizer Application", "Adjusts fertilizer per zone", "GPS-guided spreader"),
            ("Pest Population Monitor", "Tracks pest levels from traps", "Alerts farmer for intervention"),
            ("Livestock Health Tracker", "Monitors vitals and location of animals", "Alerts on health issues"),
            ("Automated Greenhouse System", "Controls temperature, humidity, light", "Sensor-driven adjustments"),
            ("Agricultural Blockchain Ledger", "Records supply chain from farm to store", "Transparency and verification"),
            ("Drip Irrigation Optimizer", "Adjusts water based on soil and weather", "Reduces water waste"),
            ("Crop Rotation Planner", "Suggests optimal crop sequences", "Improves soil health"),
        ],
    },
    "manufacturing": {
        "ideas": [
            "A predictive maintenance system for factory equipment",
            "A quality control system using computer vision",
            "A production line optimization algorithm",
            "An energy consumption monitoring system",
            "A supply chain visibility platform",
            "A worker safety monitoring system",
            "A robotic arm for assembly tasks",
            "An inventory management system",
            "A defect detection and sorting system",
            "A production forecasting tool",
        ],
        "patents": [
            ("Equipment Failure Predictor", "ML-based anomaly detection on sensor data", "Maintenance scheduling system"),
            ("Visual Quality Inspection", "Computer vision for defect detection", "99.9% accuracy claims"),
            ("Production Efficiency Optimizer", "Simulates production scenarios", "Scheduling algorithms"),
            ("Industrial Energy Monitor", "Real-time power consumption tracking", "Cost and waste reduction"),
            ("Supply Chain Tracker", "End-to-end visibility from supplier to customer", "Blockchain integration"),
            ("Worker Safety Monitor", "Tracks PPE usage and compliance", "Real-time alerts"),
            ("Automated Assembly Robot", "Adaptive gripping and placement", "Collaborative human-robot work"),
            ("Warehouse Inventory System", "Real-time stock tracking via RFID", "Automated reordering"),
            ("Automated Defect Sorter", "Sorts parts by quality grade", "ML-trained classification"),
            ("Factory Production Forecaster", "Predicts output based on conditions", "Demand planning"),
        ],
    },
    "finance": {
        "ideas": [
            "A fraud detection system for credit cards",
            "An investment portfolio optimization tool",
            "A personal finance assistant using AI",
            "A loan approval system with ML",
            "A cryptocurrency price prediction model",
            "A stock market sentiment analyzer",
            "A robo-advisor for retirement planning",
            "A peer-to-peer lending platform",
            "A transaction categorization system",
            "A budgeting assistant with spending predictions",
        ],
        "patents": [
            ("Credit Card Fraud Detector", "Real-time anomaly detection", "Multi-factor verification"),
            ("Portfolio Rebalancer", "Optimizes asset allocation", "Tax-aware recommendations"),
            ("Personal Finance AI", "Tracks spending and budgets", "Savings goal optimization"),
            ("Loan Risk Assessor", "Evaluates creditworthiness", "Automated decision making"),
            ("Crypto Price Forecaster", "Time-series prediction models", "Real-time alerts"),
            ("Market Sentiment Analyzer", "Analyzes news and social media", "Predicts market movements"),
            ("Retirement Planning Engine", "Calculates required savings", "Scenario-based planning"),
            ("Peer Lending Platform", "Connects borrowers and lenders", "Risk assessment model"),
            ("Smart Transaction Categorizer", "Automatically classifies transactions", "Machine learning classifier"),
            ("Adaptive Budgeting System", "Learns spending patterns", "Provides recommendations"),
        ],
    },
    "education": {
        "ideas": [
            "A personalized learning platform using adaptive algorithms",
            "A virtual tutor for math and science",
            "An automated essay grading system",
            "A student performance predictor",
            "A plagiarism detection tool",
            "A real-time language translation for classrooms",
            "A student engagement monitoring system",
            "A collaborative learning platform",
            "A curriculum recommendation engine",
            "A skill gap analysis tool",
        ],
        "patents": [
            ("Adaptive Learning Engine", "Adjusts difficulty based on performance", "Personalized learning paths"),
            ("AI Tutor System", "Provides explanations and problem solving", "Interactive exercises"),
            ("Automated Essay Grading", "Evaluates writing quality and content", "Rubric-based scoring"),
            ("Student Success Predictor", "Identifies at-risk students early", "Intervention recommendations"),
            ("Plagiarism Detector", "Compares against online and offline sources", "Similarity scoring"),
            ("Classroom Translation", "Real-time speech translation", "Multi-language support"),
            ("Student Engagement Monitor", "Tracks attention and participation", "Alert system for teachers"),
            ("Collaborative Learning Platform", "Enables group projects and discussions", "Version control for documents"),
            ("Curriculum Optimizer", "Suggests courses based on goals", "Career path mapping"),
            ("Skill Assessment Tool", "Evaluates competency level", "Certification readiness check"),
        ],
    },
}

# Generate dataset
entries = []

# First, load existing entries
with open("data/evaluation_dataset.json", "r") as f:
    existing_entries = json.load(f)
    entries.extend(existing_entries)

print(f"Starting with {len(entries)} existing entries")

# Generate new entries from each domain
for domain, content in domains.items():
    ideas = content["ideas"]
    patents = content["patents"]
    
    # Generate combinations with varying risk levels
    for i, idea in enumerate(ideas):
        # Create 5-7 patent-idea combinations per idea
        num_patents = random.randint(5, 7)
        for j in range(num_patents):
            patent_idx = (i + j) % len(patents)
            patent_title, patent_abstract, patent_claims = patents[patent_idx]
            
            # Determine risk based on similarity heuristic
            # Similar domain, title/abstract overlap -> Higher risk
            idea_words = set(idea.lower().split())
            patent_words = set((patent_title + " " + patent_abstract).lower().split())
            overlap = len(idea_words & patent_words) / max(len(idea_words), 1)
            
            if overlap > 0.4:
                true_risk = random.choice(["High", "High", "Medium"])
            elif overlap > 0.2:
                true_risk = random.choice(["Medium", "Medium", "Low"])
            else:
                true_risk = random.choice(["Low", "Low", "Low"])
            
            entry = {
                "idea": idea,
                "patent_title": patent_title,
                "patent_abstract": patent_abstract,
                "patent_claims": patent_claims,
                "true_risk": true_risk,
            }
            entries.append(entry)

# Add additional cross-domain pairs to increase dataset size
print(f"Generated entries from domain combinations: {len(entries)}")

# Generate more random cross-domain pairs to reach ~500
all_ideas = [entry["idea"] for entry in entries[:50]]  # Take sample of existing ideas
all_patents = [(entry["patent_title"], entry["patent_abstract"], entry["patent_claims"]) 
               for entry in entries[:50]]

target_size = 500
while len(entries) < target_size:
    idea = random.choice(all_ideas)
    patent_title, patent_abstract, patent_claims = random.choice(all_patents)
    
    # Randomly assign risk for variety
    true_risk = random.choices(
        ["High", "Medium", "Low"],
        weights=[0.3, 0.4, 0.3],  # Weighted distribution
        k=1
    )[0]
    
    entry = {
        "idea": idea,
        "patent_title": patent_title,
        "patent_abstract": patent_abstract,
        "patent_claims": patent_claims,
        "true_risk": true_risk,
    }
    entries.append(entry)

# Save expanded dataset
with open("data/evaluation_dataset.json", "w") as f:
    json.dump(entries, f, indent=2)

print(f"✅ Expanded dataset to {len(entries)} entries")

# Analyze distribution
high_count = sum(1 for e in entries if e["true_risk"] == "High")
medium_count = sum(1 for e in entries if e["true_risk"] == "Medium")
low_count = sum(1 for e in entries if e["true_risk"] == "Low")

print(f"Distribution: High={high_count}, Medium={medium_count}, Low={low_count}")
