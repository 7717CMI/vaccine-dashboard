# 🚀 Deployment Checklist for Render

## ✅ Pre-Deployment Verification

### Required Files (All Present ✓)
- [x] `app.py` - Main application with `server = app.server`
- [x] `pages.py` - Page layouts for all 8 modules
- [x] `callbacks.py` - Interactive callback functions
- [x] `requirements.txt` - All Python dependencies
- [x] `Procfile` - Gunicorn configuration for Render
- [x] `runtime.txt` - Python 3.11.6 specification
- [x] `assets/custom.css` - Custom styling
- [x] `README.md` - Comprehensive documentation
- [x] `.gitignore` - Git exclusions
- [x] `Dockerfile` - Docker containerization (optional)
- [x] `docker-compose.yml` - Docker Compose config (optional)
- [x] `render.yaml` - Infrastructure as code (optional)

### Files to EXCLUDE from Git
- [x] `__pycache__/` - Python cache
- [x] `*.pyc` - Compiled Python files
- [x] `venv/` - Virtual environment
- [x] `.env` - Environment variables
- [x] `*.bat` - Windows batch files
- [x] `DASHBOARD_GUIDE.md` - Internal guide
- [x] Excel files (using mock data)

---

## 📋 Step-by-Step Deployment Guide

### Step 1: Verify Local Setup
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Test locally
python app.py

# Verify at http://localhost:8050
# Test all 8 buttons work
# Test filters update correctly
```

### Step 2: Push to GitHub
```bash
# Check git status
git status

# Add all files (respecting .gitignore)
git add .

# Commit with descriptive message
git commit -m "Deploy: Enterprise vaccine analytics dashboard v1.0"

# Push to main branch
git push origin main
```

### Step 3: Deploy on Render

#### Option A: Via Render Dashboard (Recommended)
1. Go to https://dashboard.render.com/
2. Click "New +" → "Web Service"
3. Connect GitHub: https://github.com/7717CMI/vaccine-dashboard
4. Configure:
   ```
   Name: vaccine-analytics-dashboard
   Region: Oregon (US West) or closest to users
   Branch: main
   Root Directory: (leave empty)
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:server --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120
   Instance Type: Free (for demo) or Starter ($7/month for production)
   ```
5. Environment Variables (Optional):
   - `PYTHON_VERSION`: `3.11.6`
   - `PORT`: `8050` (Render auto-sets this)
6. Click "Create Web Service"

#### Option B: Via render.yaml (Infrastructure as Code)
1. Push repository with `render.yaml` to GitHub
2. On Render: "New +" → "Blueprint"
3. Connect repository
4. Render auto-detects configuration
5. Click "Apply"

#### Option C: Docker Deployment
1. On Render: "New +" → "Web Service"
2. Select "Docker" as Environment
3. Render auto-detects `Dockerfile`
4. Click "Deploy"

### Step 4: Monitor Deployment
1. Watch build logs in real-time
2. Look for:
   ```
   ✓ Generating comprehensive vaccine market data...
   ✓ [OK] Generated 3600 records
   ✓ [START] Global Vaccine Market Analytics Dashboard
   ✓ Dashboard ready at: http://0.0.0.0:8050
   ```
3. Initial build: 5-10 minutes
4. Subsequent builds: 2-3 minutes

### Step 5: Verify Deployment
1. Access URL: `https://your-service-name.onrender.com`
2. Test checklist:
   - [x] Landing page loads with 8 buttons
   - [x] Each button navigates to correct page
   - [x] Year filter shows 2021-2035
   - [x] All filters work correctly
   - [x] KPI cards update with filters
   - [x] Charts render properly
   - [x] Back button returns to home
   - [x] Responsive on mobile/tablet

---

## 🔧 Configuration Summary

### Gunicorn Settings (Optimized for Render Free Tier)
```
Workers: 2          # Number of worker processes
Threads: 4          # Threads per worker (Total: 8)
Timeout: 120s       # Request timeout
Bind: 0.0.0.0:$PORT # Bind to all interfaces on Render's PORT
Logging: Enabled    # Access and error logs
```

### Resource Requirements
- **Free Tier**: 512 MB RAM, 0.1 CPU
- **Recommended**: Starter ($7/mo) - 2 GB RAM, 1 CPU
- **Data Size**: 3,600 mock records (~2 MB in memory)

---

## 🐛 Troubleshooting

### Build Fails
```bash
# Check requirements.txt versions
cat requirements.txt

# Verify Python version
cat runtime.txt

# Check Procfile syntax
cat Procfile
```

### App Crashes on Startup
```bash
# Verify server variable in app.py
grep "server = app.server" app.py

# Check for import errors
python -c "import app"

# Verify all modules exist
ls -la app.py pages.py callbacks.py
```

### Memory Issues on Free Tier
- Reduce data generation size in `app.py`
- Current: 3,600 records is optimized for free tier
- If needed, reduce to 1,800 records

### Port Binding Errors
- Ensure Procfile uses `$PORT` variable
- Render auto-assigns port, don't hardcode

### Slow Loading
- Enable caching (already implemented)
- Consider upgrading to Starter plan
- Optimize chart rendering

---

## 📊 Post-Deployment

### Monitor Performance
1. Render Dashboard → Your Service → Metrics
2. Watch: CPU, Memory, Response Time
3. Check logs for errors

### Custom Domain (Optional)
1. Render Dashboard → Settings → Custom Domain
2. Add your domain: `dashboard.yourdomain.com`
3. Update DNS: CNAME record to Render

### HTTPS
- ✅ Automatically enabled by Render
- Free SSL certificate
- Auto-renewal

### Scaling (If Needed)
1. Upgrade to Starter or higher
2. Increase workers/threads in Procfile
3. Enable autoscaling (Pro plans)

---

## 🎯 Success Criteria

✅ **Deployment Successful When:**
1. URL loads without errors
2. Landing page shows 8 analysis buttons
3. All buttons navigate correctly
4. Filters work on all pages
5. Charts render and update dynamically
6. KPI cards show data
7. Year filter includes 2021-2035
8. Mobile responsive
9. No console errors
10. Performance < 3s load time

---

## 📞 Support Resources

- **Render Docs**: https://render.com/docs
- **Dash Docs**: https://dash.plotly.com/
- **GitHub Issues**: https://github.com/7717CMI/vaccine-dashboard/issues
- **Plotly Community**: https://community.plotly.com/

---

## 🔄 Continuous Deployment

Render automatically deploys when you push to `main`:

```bash
# Make changes locally
git add .
git commit -m "Update: description of changes"
git push origin main

# Render auto-detects push and redeploys
# Monitor at: https://dashboard.render.com/
```

---

## ✨ Deployment Complete!

Your dashboard is now live at: `https://your-service-name.onrender.com`

**Next Steps:**
1. Share the URL with stakeholders
2. Monitor usage via Render metrics
3. Collect feedback for improvements
4. Consider custom domain
5. Enable monitoring/alerts

---

**Last Updated**: 2025-01-29
**Version**: 1.0
**Status**: Production Ready ✅

