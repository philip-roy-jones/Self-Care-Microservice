from fastapi import FastAPI
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random
import json

# Initialize FastAPI app and sentiment analysis
app = FastAPI()
analyzer = SentimentIntensityAnalyzer()

# Request body model
class JournalEntry(BaseModel):
    mood: str
    journal_text: str

# Load motivational messages from JSON
with open("motivational_messages.json", "r") as file:
    MOTIVATIONAL_MESSAGES = json.load(file)

@app.post("/api/analyze")
def analyze_journal(entry: JournalEntry):
    
    # Prepend the mood to the journal text
    combined_text = f"{entry.mood}. {entry.journal_text}"

    # Analyze sentiment
    scores = analyzer.polarity_scores(combined_text)
    
    # Get the compound score and convert to percentage
    compound_score = scores['compound']                             # This is a value between -1 and 1, -1 is very negative, 1 is very positive
    positivity_percentage = round((compound_score + 1) * 50, 2)

    # Determine sentiment for message selection
    if positivity_percentage > 60:
        sentiment = "positive"
    elif positivity_percentage < 40:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    # Pick a random message
    message = random.choice(MOTIVATIONAL_MESSAGES.get(sentiment, []))

    # Response
    return {
        "positivity_score": f"{positivity_percentage}%",
        "motivational_message": message
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
