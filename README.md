# Physical AI & Humanoid Robotics Textbook

An intelligent textbook platform combining Docusaurus (frontend), FastAPI (backend), and three AI agent skills (quiz generation, Urdu translation, personalization) to deliver adaptive learning experiences for robotics students.

## Features

- **Adaptive Learning**: Content personalization based on user's technical background (Python knowledge, GPU availability)
- **Multilingual Support**: Urdu translation of technical content while preserving code and LaTeX
- **Interactive Quizzes**: AI-generated quizzes appended to each chapter
- **Intelligent Chat**: RAG-based chatbot with textbook context and source citations
- **Select-to-Ask**: Highlight text and ask questions directly from content

## Architecture

### Backend (FastAPI)
- User authentication and profiles (Better-Auth pattern)
- PostgreSQL database (Neon Serverless) for user data
- Qdrant vector store for textbook content embeddings
- OpenAI integration for AI agent skills
- API endpoints for personalization, translation, and chat

### Frontend (Docusaurus)
- Interactive textbook with Docusaurus documentation framework
- Personalize and Translate buttons on each page
- Floating chat widget for textbook Q&A
- Responsive design for multiple devices

### AI Agent Skills (Python CLI Tools)
- `quiz_agent.py`: Generates chapter quizzes from markdown content
- `translator_agent.py`: Translates content to Urdu while preserving code/LaTeX
- `personalize_agent.py`: Rewrites content based on user profile

## Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or Neon Serverless account)
- Qdrant Cloud account
- Google Generative AI API key (Gemini API)

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r backend/requirements.txt
```

2. Set up environment variables:
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your actual credentials
```

3. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/textbook_db
QDRANT_URL=https://your-cluster-url.qdrant.tech
QDRANT_API_KEY=your-qdrant-api-key
OPENAI_API_KEY=your-google-generative-api-key
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
```

## API Endpoints

- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `POST /api/personalize` - Content personalization
- `POST /api/translate` - Content translation
- `POST /chat` - Textbook Q&A chatbot

## Tech Stack

- **Frontend**: Docusaurus (React), TypeScript
- **Backend**: FastAPI (Python), PostgreSQL
- **Database**: Neon Serverless Postgres
- **Vector Store**: Qdrant Cloud
- **Authentication**: JWT-based (Better-Auth pattern)
- **AI Framework**: Google Generative AI (Gemini Pro, Embedding-001 model)
- **Deployment**: Vercel/Netlify (frontend), Railway/Render (backend)

## Development

The project follows a 4-phase implementation approach:
1. **Agent Skills** - CLI tools for AI functionality
2. **Backend Infrastructure** - API and data management
3. **Content Creation** - Textbook chapters and quizzes
4. **Frontend Integration** - UI and user experience

## Contributing

This project was developed as part of a hackathon focused on Physical AI & Humanoid Robotics education. Contributions are welcome for educational use cases, additional robotics content, and improved AI interactions.

## License

[Specify license here]