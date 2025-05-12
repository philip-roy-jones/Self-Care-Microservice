# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline, logging
import random
import json

logging.set_verbosity_error()  # Suppress warnings from transformers library

# Initialize FastAPI app and sentiment analysis pipeline
app = FastAPI()

# Load the multi-class sentiment model
model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    ignore_mismatched_sizes=True  # Suppress warnings about mismatched sizes
)

# Define the sentiment pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Request body model
class JournalEntry(BaseModel):
    mood: str
    journal_text: str

# Load motivational messages from JSON
with open("motivational_messages.json", "r") as file:
    MOTIVATIONAL_MESSAGES = json.load(file)

# Expand the lists to around 100 entries
for category in MOTIVATIONAL_MESSAGES:
    while len(MOTIVATIONAL_MESSAGES[category]) < 100:
        MOTIVATIONAL_MESSAGES[category] += MOTIVATIONAL_MESSAGES[category][:5]

@app.post("/analyze")
def analyze_journal(entry: JournalEntry):
    # Analyze sentiment
    result = sentiment_pipeline(entry.journal_text)[0]
    # print("Raw Model Output:", result)  # For debugging

    # Extract sentiment and score
    sentiment = result['label']

    # Special handling for neutral
    if sentiment == "neutral":
        # Randomly pick between 40 and 60
        score = round(random.uniform(40, 60), 2)
    elif sentiment == "negative":
        # Randomly pick between 0 and 40
        score = round(random.uniform(0, 40), 2)
    elif sentiment == "positive":
        # Randomly pick between 60 and 100
        score = round(random.uniform(60, 100), 2)
    else:
        # Default to -1 if sentiment is not recognized
        sentiment = "unknown"
        score = -1

    # Pick a random message
    message = random.choice(MOTIVATIONAL_MESSAGES.get(sentiment, []))

    # Response
    return {
        "positivity_score": f"{score}%",
        "motivational_message": message
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
