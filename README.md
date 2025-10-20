![Aprendia](images/banner.png "Aprendia")

# Aprendia

A modern web application for conversational language study and learning.

Summary: This scaffold provides a working prototype of Aprendia, a story-based language learning demo app powered by Google Gemini and Google Text-to-Speech (TTS). The backend runs on FastAPI, the frontend on Next.js + TailwindCSS, and all data is stored in a simple in-memory Python dict — no persistence or user accounts. Audio files are stored locally under the backend’s static_audio/ directory.

## Features

- **Web-Based Interface**: AI assisted story creation
- **Interactive Learning**: Flashcards based on chapters and quizzes.


Summary: This scaffold provides a working prototype of Aprendia, a story-based language learning demo app powered by Google Gemini and Google Text-to-Speech (TTS). The backend runs on FastAPI, the frontend on Next.js + TailwindCSS, and all data is stored in a simple in-memory Python dict — no persistence or user accounts. Audio files are stored locally under the backend’s static_audio/ directory.

## Quick Start

### Web Application (Recommended)

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions.

#### Local Development

1. **Backend Setup**:
```bash
cd backend
python3.10 -m venv venv
source venv/bin/activate
pip3.10 install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
python3.10 api_main.py
# or uvicorn api_main:app --reload
```

2. **Frontend Setup** (in a new terminal):
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

3. Open http://localhost:3000 and upload a session JSON file

### CLI Usage

The original CLI is still available:

```bash
cd backend
python src/cli_create_story # creates the first chapter of a new story
```

## Architecture

```
evals-for-ai-assisted-engineering/
├── frontend/                           # Next.js 15 web application
│   ├── app/
│   ├── components/
│   └── package.json
│
├── backend/                            # FastAPI + LangGraph backend
│   ├── api_main.py                    # FastAPI server
│   ├── src/
│   │   ├── models.py                  # Pydantic models
│   │   ├── extractor.py               # Session parsing
│   │   ├── evaluators/                # Seven evaluators
│   │   ├── summarizer.py              # Weighted scoring
│   │   └── workflow.py                # LangGraph orchestration
│   ├── requirements.txt
│   └── Dockerfile
│
└── DEPLOYMENT.md                       # Deployment guide
```

## Technology Stack

### Frontend
- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS
- Recharts (visualizations)
- Server-Sent Events

### Backend
- FastAPI
- LangGraph
- LangChain (OpenAI)
- Python 3.10+
- Pydantic


## Deployment

### Production Deployment

Deploy the frontend to Vercel and backend to Railway:

1. **Backend (Railway)**:
   - Deploy from GitHub
   - Set `GEMINI_API_KEY` environment variable
   - Automatically builds using Dockerfile

2. **Frontend (Vercel)**:
   - Deploy from GitHub
   - Set `NEXT_PUBLIC_BACKEND_URL` to your Railway URL
   - Automatically detects Next.js configuration

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Development

### Backend Development

```bash
cd backend
source venv/bin/activate

# Format code
black src/

# Lint
ruff check --fix src/

# Type check
mypy src/

# Run server
python api_main.py
```

### Frontend Development

```bash
cd frontend

# Run dev server
npm run dev

# Build
npm run build

# Lint
npm run lint
```

## API Endpoints

- `POST /stories/{story_id}/studiables` - create quiz or chapter
- `GET /stories` - Get list of stories
- `POST /stories` - create new story, with 1 chapter

## Environment Variables

### Backend
- `OPENAI_API_KEY` (required): Your OpenAI API key

### Frontend
- `NEXT_PUBLIC_BACKEND_URL` (required): Backend API URL

## License

MIT

## Contributing

Contributions welcome! Please open an issue or submit a pull request.