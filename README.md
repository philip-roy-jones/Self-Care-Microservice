# Motivational Message Microservice

This microservice analyzes journal entries for sentiment and provides a motivational message based on the sentiment. It is built using FastAPI and a pre-trained sentiment analysis model.

## Setup Instructions

1. **Clone the Repository**  
   Clone this repository to your local machine.

2. **Install Python Dependencies**  
   Ensure you have Python 3.8 or higher installed. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure JSON File Availability**  
   Make sure `motivational_messages.json` is in the same directory as `app.py`. It contains the motivational messages used by the service.

## Starting the FastAPI Server

Activate the virtual environment by running the following command in the root directory:

### Windows
```bash
.\venv\Scripts\activate
```

### macOS/Linux
```bash
source venv/bin/activate
```

### With the venv activated, run:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
The server will start on `http://0.0.0.0:8000`.

## API Usage

### POST /api/analyze

Analyze a journal entry and return a positivity score plus a motivational message.

- **Request Header**  
  `Content-Type: application/json`

- **Request Body**  
  ```json
  {
    "mood": "string",
    "journal_text": "string"
  }
  ```
  - `mood`: (optional) a string representing the user’s mood.  
  - `journal_text`: the journal entry text to analyze.

- **Response Body**  
  ```json
  {
    "positivity_score": "string",
    "motivational_message": "string"
  }
  ```

### Example with curl

```bash
curl -X POST "http://0.0.0.0:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "mood": "neutral",
    "journal_text": "Today was challenging but I kept going."
  }'
```

**Sample Response**  
```json
{
  "positivity_score": "47.89%",
  "motivational_message": "Every setback is a setup for a comeback. Keep going!"
}
```

## Notes

- The sentiment model (`cardiffnlp/twitter-roberta-base-sentiment-latest`) downloads on first run.
- Messages are categorized into `positive`, `neutral`, and `negative` and selected at random.

## License

This project is for educational purposes. No specific license is provided.