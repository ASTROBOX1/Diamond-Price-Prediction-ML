# Deployment Guide - Diamond Price Prediction API

This guide provides steps to deploy your ML system to production environments.

## 1. Local Production Test (Docker Compose)
Before pushing to the cloud, verify the production setup locally:

```bash
docker-compose up --build
```
This will start the API using **Gunicorn** (4 workers) on `localhost:8000`.

---

## 2. Cloud Deployment (Render) - Recommended
Render is the easiest platform for this project.

1. **Push your code** to a GitHub repository.
2. **Create a New Web Service** on [Render](https://dashboard.render.com/).
3. **Connect your repo**.
4. **Choose Runtime**: `Docker`.
5. **Environment**:
   - No additional environment variables are strictly required by default, but you can set `PYTHONPATH=/app/src` if needed.
6. **Plan**: Free tier is sufficient for this model.
7. **Deploy**. Render will build the image from the `Dockerfile` and go live.

---

## 3. Cloud Deployment (Railway)
1. **GitHub connection**: Link your repository.
2. **Automatic Detection**: Railway will detect the `Dockerfile` automatically.
3. **Deploy**: Click deploy. It will provide a public URL.

---

## 4. Manual Deployment (VPS/DigitalOcean)
If using a Linux server:

1. **Install Docker & Docker Compose**.
2. **Clone the repo**.
3. **Run**:
   ```bash
   docker-compose up -d --build
   ```
4. **Proxy**: (Recommended) Set up Nginx as a reverse proxy to handle SSL (HTTPS) and route traffic to port 8000.

---

## 📊 Monitoring & Health
Once deployed, reach your service at:
- `https://your-app-domain.com/docs` (Interactive documentation)
- `https://your-app-domain.com/health` (Service health status)
