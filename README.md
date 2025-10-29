# 🏥 Global Vaccine Market Analytics Dashboard

An enterprise-grade, multi-page vaccine analytics dashboard built with Plotly Dash. This dashboard provides comprehensive insights into global vaccine markets with 8 specialized analysis modules.

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Dash](https://img.shields.io/badge/dash-2.14.2-brightgreen.svg)](https://dash.plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ⚠️ Important Notice

**This is a DEMO dashboard using synthetic data for illustration purposes only. All statistics and data shown do not represent real-world vaccine data and have no association with actual datasets.**

---

## 🎯 Features

### 8 Specialized Analysis Modules

1. **Epidemiology Analysis** - Disease prevalence and incidence tracking
2. **Vaccination Rate** - Track vaccination coverage rates by region and country
3. **Pricing Analysis** - Market pricing trends, elasticity, and price class analysis
4. **CAGR Analysis** - Compound annual growth rate analysis by market segments
5. **MSA Comparison** - Market share analysis with value/volume/share metrics
6. **Procurement Analysis** - Public vs private procurement trends and patterns
7. **Brand-Demographic Analysis** - Brand performance across demographics
8. **FDF Analysis** - Formulation (FDF) and Route of Administration (ROA) analysis

### Dynamic Filters (Available on All Pages)
- **Year Filter**: 2021-2035 forecasting range
- **Region Filter**: North America, Europe, APAC, Latin America, Middle East, Africa
- **Income Type Filter**: Low, Middle, High income countries
- **Country Filter**: Dynamically updates based on region and income selections
- **Segment Filters**: Disease, Brand, Market, Age Group, Gender, FDF, ROA, Price Class, Procurement Type

### Interactive Visualizations
- **KPI Summary Cards**: Real-time metrics that update with filter selections
- **Interactive Charts**: Bar charts, pie charts, line charts, and trend analysis
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Professional UI**: Enterprise-grade design with smooth animations

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip package manager
- Git

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/7717CMI/vaccine-dashboard.git
cd vaccine-dashboard
```

2. **Create a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
```
http://localhost:8050
```

---

## 📦 Deployment on Render

### Method 1: Deploy via Render Dashboard (Recommended)

#### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### Step 2: Create Web Service on Render
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `https://github.com/7717CMI/vaccine-dashboard`
4. Configure the service:
   - **Name**: `vaccine-analytics-dashboard` (or your preferred name)
   - **Region**: Select closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:server --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120`
   - **Instance Type**: **Free** (for testing) or **Starter** (for production)

5. **Environment Variables** (Optional):
   - Click "Advanced" → "Add Environment Variable"
   - Add: `PYTHON_VERSION` = `3.11.6`

6. Click **"Create Web Service"**

#### Step 3: Monitor Deployment
- Watch the build logs in real-time
- Initial deployment takes 5-10 minutes
- Your dashboard will be available at: `https://your-service-name.onrender.com`

### Method 2: Deploy via render.yaml (Infrastructure as Code)

1. The repository includes a `render.yaml` file for automatic deployment
2. Connect your repository to Render
3. Render will automatically detect and use the configuration

### Method 3: Docker Deployment

The repository includes Docker support for containerized deployment:

#### Build and Run Locally
```bash
# Build the Docker image
docker build -t vaccine-dashboard .

# Run the container
docker run -p 8050:8050 vaccine-dashboard
```

#### Using Docker Compose
```bash
docker-compose up -d
```

#### Deploy to Render using Docker
1. On Render Dashboard, select **"Docker"** as environment
2. Render will automatically detect the `Dockerfile`
3. Deploy with default settings

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | Plotly Dash | 2.14.2 |
| **UI Components** | Dash Bootstrap Components | 1.5.0 |
| **Visualization** | Plotly | 5.18.0 |
| **Data Processing** | Pandas | 2.1.4 |
| **Numerical Computing** | NumPy | 1.26.2 |
| **Web Server** | Gunicorn | 21.2.0 |
| **Excel Support** | OpenPyXL | 3.1.2 |
| **HTTP Requests** | Requests | 2.31.0 |

---

## 📊 Data Schema

The dashboard generates comprehensive mock data with the following structure:

| Field | Description | Example Values |
|-------|-------------|----------------|
| `year` | Forecasting year | 2021-2035 |
| `region` | Geographic region | North America, Europe, APAC |
| `country` | Country name | USA, India, Germany |
| `income_type` | Country income level | Low, Middle, High |
| `disease` | Disease/Market | HBV, HPV, Influenza |
| `brand` | Vaccine brand | Gardasil 9, Shingrix |
| `prevalence` | Disease prevalence | 100,000 - 1,000,000 |
| `incidence` | Disease incidence | 5,000 - 500,000 |
| `vaccination_rate` | Vaccination rate % | 10% - 95% |
| `coverage_rate` | Coverage rate % | 5% - 90% |
| `price` | Price per dose (USD) | $2 - $50 |
| `price_elasticity` | Price elasticity | 0.5 - 2.5 |
| `price_class` | Price category | Premium, Standard, Budget |
| `cagr` | Growth rate % | -5% to 20% |
| `value` | Market value (USD) | $100K - $50M |
| `volume_units` | Volume units | 100 - 100,000 |
| `share` | Market share % | 0.1% - 30% |
| `yoy` | Year-over-year growth % | -10% to 25% |
| `public_private` | Procurement type | Public, Private, UNICEF |
| `qty` | Quantity procured | 100 - 100,000 |
| `age_group` | Age demographic | Pediatric, Adult, Geriatric |
| `gender` | Gender | Male, Female, Other |
| `revenue` | Revenue (USD) | $10K - $10M |
| `fdf` | Formulation | Vial, Prefilled Syringe |
| `roa` | Route of Administration | IM, SC, Oral |

---

## 🎨 UI Features

### Modern Design
- **Enterprise-Grade Layout**: Professional color palette and typography
- **Responsive Grid**: Adapts to all screen sizes
- **Gradient Backgrounds**: Soft, modern color transitions
- **Card-Based UI**: Clean, organized presentation
- **Interactive Animations**: Smooth hover effects and transitions

### User Experience
- **Intuitive Navigation**: One-click access to all 8 modules
- **Dynamic Filtering**: Real-time updates without page reload
- **Multi-Select Dropdowns**: Select multiple options simultaneously
- **Placeholder Text**: Clear guidance on filter usage
- **Show All by Default**: See complete data when no filters applied

---

## 📁 Project Structure

```
vaccine-dashboard/
├── app.py                  # Main application file with data generation and routing
├── pages.py                # Layout definitions for all 8 analysis pages
├── callbacks.py            # All callback logic for interactivity
├── assets/
│   └── custom.css         # Custom styling for enterprise UI
├── requirements.txt        # Python dependencies
├── Procfile               # Render/Heroku deployment config
├── runtime.txt            # Python version specification
├── Dockerfile             # Docker containerization
├── docker-compose.yml     # Docker Compose configuration
├── .dockerignore          # Docker build exclusions
├── render.yaml            # Render infrastructure as code
├── .gitignore             # Git exclusions
└── README.md              # This file
```

---

## 🔧 Configuration

### Environment Variables

You can set these environment variables for production deployment:

```bash
# Port configuration (Render sets this automatically)
PORT=8050

# Python version
PYTHON_VERSION=3.11.6

# Debug mode (set to False in production)
DEBUG=False
```

### Custom Styling

The dashboard includes a `custom.css` file in the `assets/` folder for global styling. To customize:

1. Edit `assets/custom.css`
2. Modify colors, fonts, spacing as needed
3. The app automatically loads CSS from the `assets/` folder

---

## 🚦 Troubleshooting

### Common Issues

**Issue**: Dashboard doesn't load after deployment
- **Solution**: Check Render logs for errors. Ensure all files are committed to Git.

**Issue**: Memory errors during data generation
- **Solution**: The mock data generates 3,600 records by default. For larger datasets, consider pagination.

**Issue**: Filters not updating
- **Solution**: Clear browser cache and hard refresh (Ctrl+F5 or Cmd+Shift+R)

**Issue**: Charts not displaying
- **Solution**: Check browser console for JavaScript errors. Ensure `plotly.js` is loading correctly.

### Render-Specific Issues

**Issue**: Build fails on Render
- **Solution**: Verify `requirements.txt` has all dependencies with correct versions

**Issue**: App crashes on startup
- **Solution**: Check that `server = app.server` is defined in `app.py`

**Issue**: Port binding errors
- **Solution**: Ensure start command uses `$PORT` variable: `--bind 0.0.0.0:$PORT`

---

## 📱 Browser Support

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | ✅ Fully Supported |
| Firefox | 88+ | ✅ Fully Supported |
| Safari | 14+ | ✅ Fully Supported |
| Edge | 90+ | ✅ Fully Supported |
| Opera | 76+ | ✅ Fully Supported |

---

## 🔒 Security

- Non-root user in Docker container
- No hardcoded credentials
- HTTPS supported on Render
- Health checks enabled
- Timeout configurations for production stability

---

## 📈 Performance Optimization

- **Data Caching**: Generated data is cached in memory
- **Efficient Filtering**: Pandas-based filtering for fast operations
- **Lazy Loading**: Charts render only when needed
- **Worker Configuration**: Gunicorn with 2 workers and 4 threads
- **Timeout Settings**: 120-second timeout for complex operations

---

## 🤝 Contributing

This is a demonstration project showcasing Dash capabilities. Feel free to:
- Fork the repository
- Create feature branches
- Submit pull requests
- Report issues

---

## 📄 License

MIT License - Feel free to use this dashboard as a template for your projects.

---

## 📧 Support

For questions or issues:
- Create an issue on GitHub: [https://github.com/7717CMI/vaccine-dashboard/issues](https://github.com/7717CMI/vaccine-dashboard/issues)
- Check the documentation: [Plotly Dash Documentation](https://dash.plotly.com/)
- Community support: [Plotly Community Forum](https://community.plotly.com/)

---

## 🙏 Acknowledgments

- Built with [Plotly Dash](https://dash.plotly.com/)
- UI components from [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
- Icons inspired by [Feather Icons](https://feathericons.com/)
- Deployment platform: [Render](https://render.com/)

---

## 📊 Sample Deployment

🔗 **Live Demo**: Your dashboard will be available at `https://your-service-name.onrender.com` after deployment

---

**© 2025 HealthData AI – Global Vaccine Market Intelligence Platform**

*Powered by Plotly Dash | Enterprise Analytics | Demo Dataset*

---

## 🎯 Quick Deployment Checklist

Before pushing to production:

- [x] All dependencies in `requirements.txt`
- [x] `server = app.server` in `app.py`
- [x] `Procfile` configured correctly
- [x] Python version in `runtime.txt`
- [x] `.gitignore` excludes unnecessary files
- [x] Environment variables set (if needed)
- [x] Test locally before deployment
- [x] README updated with project details
- [x] Docker files configured (optional)
- [x] render.yaml configured (optional)

**Ready to Deploy!** 🚀
