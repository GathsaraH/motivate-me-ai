# Motivate Me AI - Python Backend

## Setup Instructions

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set your OpenAI API Key:**
Create a `.env` file in this folder with the following content:
```
OPENAI_API_KEY=your-openai-api-key-here
```

3. **Run the server:**
```bash
uvicorn main:app --reload
```

## Endpoint
- `POST /generate` with JSON `{ "theme": "productivity" }`
- Returns: `{ "quote": "..." }`
