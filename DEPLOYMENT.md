# 🚀 Deployment Guide for Render.com

This guide will help you deploy the AI-Driven Learning Platform to Render.com.

## 📋 Prerequisites

1. **Render.com Account**: Sign up at [render.com](https://render.com)
2. **GitHub Repository**: Your code should be pushed to GitHub
3. **Environment Variables**: Prepare your production environment variables

## 🔧 Pre-Deployment Setup

### 1. Environment Variables Setup

Copy the example environment file and configure it:

```bash
cp backend/.env.example backend/.env
```

**Required Environment Variables:**
- `DATABASE_URL` - PostgreSQL connection string (Render will provide this)
- `SECRET_KEY` - A secure random string for JWT tokens
- `OPENAI_API_KEY` or `GEMINI_API_KEY` - Your AI service API key

### 2. Generate a Secure Secret Key

```python
# Run this Python script to generate a secure secret key
import secrets
print(secrets.token_urlsafe(32))
```

## 🐳 Render Deployment Steps

### Step 1: Create PostgreSQL Database

1. Go to your Render Dashboard
2. Click "New" → "PostgreSQL"
3. Configure:
   - **Name**: `ai-learning-db`
   - **Database**: `learning_platform`
   - **User**: `postgres`
   - **Region**: Choose closest to your users
4. Click "Create Database"
5. **Save the DATABASE_URL** from the database info page

### Step 2: Deploy Backend Service

1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `ai-learning-backend`
   - **Environment**: `Docker`
   - **Region**: Same as your database
   - **Branch**: `main`
   - **Dockerfile Path**: `backend/Dockerfile`
   - **Root Directory**: `backend`

4. **Environment Variables** (Add these in Render):
   ```
   DATABASE_URL=<your-render-postgres-url>
   SECRET_KEY=<your-generated-secret-key>
   OPENAI_API_KEY=<your-openai-key>
   DEBUG=false
   ALLOWED_ORIGINS=https://your-frontend-url.onrender.com
   ```

5. Click "Create Web Service"

### Step 3: Deploy Frontend Service

1. Click "New" → "Static Site"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `ai-learning-frontend`
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

4. **Environment Variables**:
   ```
   VITE_API_BASE_URL=https://your-backend-url.onrender.com
   ```

5. Click "Create Static Site"

### Step 4: Update CORS Settings

After getting your frontend URL, update the backend environment variables:

1. Go to your backend service in Render
2. Update `ALLOWED_ORIGINS` to include your frontend URL:
   ```
   ALLOWED_ORIGINS=https://your-frontend-url.onrender.com,http://localhost:3000,http://localhost:5173
   ```

## 🔄 Database Migration

Render will automatically run database migrations when deploying the backend service. The `Dockerfile` includes migration setup.

## 🌐 Custom Domains (Optional)

### Backend Custom Domain
1. Go to backend service → Settings → Custom Domains
2. Add your API domain (e.g., `api.yourdomain.com`)

### Frontend Custom Domain
1. Go to frontend service → Settings → Custom Domains
2. Add your main domain (e.g., `yourdomain.com`)

## 📊 Monitoring & Logs

- **Backend Logs**: Backend service → Logs tab
- **Database Metrics**: PostgreSQL service → Metrics tab
- **Frontend Deploys**: Static site → Deploys tab

## 🔐 Security Checklist

- ✅ Environment variables are properly configured
- ✅ Secret key is randomly generated and secure
- ✅ Database credentials are not hardcoded
- ✅ CORS is properly configured
- ✅ `.env` files are not committed to Git
- ✅ API keys are stored in Render environment variables

## 🚨 Troubleshooting

### Common Issues:

1. **Migration Errors**: Check backend logs for database connection issues
2. **CORS Errors**: Verify `ALLOWED_ORIGINS` includes your frontend URL
3. **API Connection**: Ensure `VITE_API_BASE_URL` points to your backend
4. **Build Failures**: Check if all dependencies are listed in requirements.txt/package.json

### Getting Help:

- Check Render logs for detailed error messages
- Verify all environment variables are set correctly
- Ensure database is running and accessible

## 🎉 Success!

Once deployed, your application will be available at:
- **Frontend**: `https://your-frontend-url.onrender.com`
- **Backend API**: `https://your-backend-url.onrender.com`
- **API Docs**: `https://your-backend-url.onrender.com/docs`

## 📱 Testing Your Deployment

1. Visit your frontend URL
2. Register a new account
3. Try generating a lesson
4. Check that admin features work (login with admin@admin.com / admin123)

---

**Need help?** Check the [Render Documentation](https://render.com/docs) or contact support.
