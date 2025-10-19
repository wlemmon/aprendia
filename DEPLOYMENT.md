# Deployment Guide

This guide covers deploying the Aprendia web application with a Next.js frontend on Vercel and a Python FastAPI backend on Railway.

## Architecture

- **Frontend**: Next.js 15 app deployed on Vercel
- **Backend**: Python FastAPI server deployed on Railway (or Render/DigitalOcean)
- **Communication**: REST API + Server-Sent Events for real-time progress

## Prerequisites

- Vercel account (https://vercel.com)
- Railway account (https://railway.app) or alternative hosting
- OpenAI API key
- Git repository with the code

## Backend Deployment (Railway)

### Why Railway?

Railway is the recommended platform for the FastAPI backend because:
- ✅ No execution timeouts (LangGraph workflows can take several minutes)
- ✅ Full Docker support with `backend/Dockerfile`
- ✅ Native SSE (Server-Sent Events) support for real-time progress
- ✅ No file size limits (handles LangChain dependencies)

### Configuration

The backend is configured via `backend/railway.toml`:
- Uses Docker builder with health checks at `/health`
- Auto-restart on failure
- Runs on port 8000

### Option 1: Deploy via Railway CLI (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Navigate to backend directory
cd backend

# Initialize Railway project
railway init

# Add environment variable
railway variables set OPENAI_API_KEY=your_openai_api_key_here

# Deploy (uses backend/railway.toml configuration)
railway up

# Get your deployment URL
railway open
```

The backend will be built using Docker and deployed with automatic health checks.

### Option 2: Deploy via Railway Dashboard

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. **Important**: After creating the service, go to **Settings** and set:
   - **Root Directory**: `backend`
5. Add environment variable in the **Variables** tab:
   - Key: `OPENAI_API_KEY`
   - Value: your OpenAI API key
6. Deploy

Railway will automatically detect `backend/railway.toml` and use Docker to build your service.

### Alternative: Render Deployment

1. Go to https://render.com
2. New → Web Service
3. Connect your repository
4. Configure:
   - Environment: Docker
   - Root Directory: `backend`
   - Instance Type: Free or Starter
5. Add environment variable: `OPENAI_API_KEY`
6. Deploy

## Frontend Deployment (Vercel)

### Why Vercel?

Vercel is the optimal platform for the Next.js frontend:
- ✅ Built by the creators of Next.js
- ✅ Zero configuration deployment
- ✅ Automatic HTTPS and CDN
- ✅ Free tier perfect for this project
- ✅ Excellent performance

### Option 1: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend directory
cd frontend

# Deploy
vercel

# Add environment variable
vercel env add NEXT_PUBLIC_BACKEND_URL production
# Enter your Railway backend URL (e.g., https://backend-production-xxxx.up.railway.app)

# Redeploy with environment variable
vercel --prod
```

### Option 2: Deploy via Vercel Dashboard (Recommended)

1. Go to https://vercel.com
2. Click "New Project" → "Import Git Repository"
3. Select your repository
4. Configure:
   - Framework Preset: Next.js (auto-detected)
   - Root Directory: `frontend`
5. Add environment variable:
   - Key: `NEXT_PUBLIC_BACKEND_URL`
   - Value: your Railway backend URL (e.g., `https://backend-production-xxxx.up.railway.app`)
6. Click "Deploy"

Vercel will automatically detect Next.js and configure build settings.

## Local Development

### Backend

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file:
```bash
cp .env.example .env
```
Add your `GEMINI_API_KEY`

5. Run the server:
```bash
python api_main.py
```

Backend will be available at http://localhost:8000

### Frontend

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create .env.local file:
```bash
cp .env.example .env.local
```

4. Run development server:
```bash
npm run dev
```

Frontend will be available at http://localhost:3000

## Testing the Application

1. Start both backend and frontend servers
2. Navigate to http://localhost:3000

## Environment Variables

### Backend (Railway)
- `GEMINI_API_KEY` (required): Your Gemini API key
- `PORT` (optional): Server port, defaults to 8000 (Railway sets this automatically)

### Frontend (Vercel)
- `NEXT_PUBLIC_BACKEND_URL` (required): Your Railway backend URL
  - Example: `https://backend-production-xxxx.up.railway.app`
  - Find this in Railway dashboard → your service → Settings → Domain

## CORS Configuration

The backend is pre-configured to accept requests from:
- `http://localhost:3000` (local development)
- `https://*.vercel.app` (Vercel deployments)

No changes needed for Railway backend + Vercel frontend setup.

## Monitoring and Logs

### Railway
- View logs: `railway logs`
- Or visit the Railway dashboard

### Vercel
- View logs in the Vercel dashboard
- Real-time function logs available

## Troubleshooting

### Backend Issues

**Error: GEMINI_API_KEY not set**
- Ensure environment variable is set in Railway/Render dashboard

**Error: Module not found**
- Check that all dependencies are in `requirements.txt`
- Verify the build completed successfully

**CORS errors**
- Update allowed origins in `api_main.py`
- Ensure frontend URL is correctly added

### Frontend Issues

**Error: Failed to fetch**
- Check `NEXT_PUBLIC_BACKEND_URL` is correct
- Verify backend is running and accessible

**Build fails**
- Check Node version compatibility (requires Node 18+)
- Verify all dependencies are installed

### Railway Backend Issues

**Error: "Script start.sh not found" or "Railpack could not determine how to build"**
- Solution: Set the **Root Directory** to `backend` in Railway service settings
- The `backend/railway.toml` file will then configure the Docker build automatically

**Backend not building with Dockerfile**
- Verify `backend/railway.toml` exists and specifies `builder = "DOCKERFILE"`
- Check that `backend/Dockerfile` exists and is valid
- View build logs in Railway dashboard for specific errors

**Long evaluation timeouts**
- Railway has no execution timeout limits - this is normal
- LangGraph workflows can take 2-5 minutes for complex sessions
- Check Railway logs if it exceeds 10 minutes

### Frontend-Backend Connection Issues

**Frontend can't reach backend**
- Verify `NEXT_PUBLIC_BACKEND_URL` in Vercel matches your Railway backend URL
- Check that Railway backend service is running (green status in dashboard)
- Test backend directly: visit `https://your-backend.railway.app/health`
- Ensure CORS is configured correctly (should work by default with Vercel)

## Cost Estimation

### Recommended Setup (Railway + Vercel)

**Railway (Backend)**
- Hobby Plan: $5/month (500 hours)
- Estimated usage: ~10-50 hours/month for moderate use
- **Cost**: $5/month

**Vercel (Frontend)**
- Hobby: Free for personal projects
- **Cost**: $0/month

**OpenAI API**
- Varies by usage
- Per evaluation: $0.10-0.30
- Monthly (100 evaluations): ~$10-30

**Total Monthly Cost**: ~$15-35/month for moderate usage

## Security Notes

1. Never commit API keys to the repository
2. Use environment variables for all secrets
3. Keep dependencies up to date
4. Monitor API usage to avoid unexpected costs
5. Consider rate limiting for production use

## Scaling Considerations

For high-volume usage:
1. Consider upgrading to Railway Pro or Render paid tier
2. Implement request queuing
3. Add Redis for better state management
4. Consider caching evaluation results
5. Monitor OpenAI API rate limits