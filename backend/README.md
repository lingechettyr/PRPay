# PRPay Backend

FastAPI backend for PRPay - a GitHub PR review payment and tracking system.

## Getting Started

### Prerequisites

- Python 3.10+
- Supabase account and project

### Environment Setup

1. Create a `.env` file in the backend directory with your Supabase credentials:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

### Installation

Install the required dependencies using a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running Locally

Start the development server with uvicorn:

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Start server (default port 8000)
uvicorn main:app --reload

# Or specify a different port
uvicorn main:app --reload --port 8001
```

The server will be available at:
- API: `http://127.0.0.1:8000` (or your specified port)
- Interactive API docs (Swagger): `http://127.0.0.1:8000/docs`
- Alternative API docs (ReDoc): `http://127.0.0.1:8000/redoc`

The `--reload` flag enables auto-reload on code changes for development.


## Deploying to Vercel

Deploy your project to Vercel with the following command:

```bash
npm install -g vercel
vercel --prod
```

Or `git push` to your repository with our [git integration](https://vercel.com/docs/deployments/git).
