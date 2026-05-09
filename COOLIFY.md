# Coolify Deployment Configuration

## Option 1: Docker (Recommended for Coolify)

### Build Settings
- **Dockerfile**: Use existing Dockerfile
- **Docker Image**: `web-crawler-agent`

### Port
- **Internal Port**: 8501

### Start Command
```bash
streamlit run examples/app.py --server.port=8501 --server.address=0.0.0.0
```

---

## Option 2: Direct Deploy (No Docker)

### Pre-deploy script
```bash
pip install -e .
```

### Post-deploy script
```bash
echo "no post-install needed"
```

### Start Command
```bash
python3 -m streamlit run examples/app.py --server.port=8501 --server.address=0.0.0.0
```

### Port
- 8501

### Health Check
- URL: `http://localhost:8501/_stcore/health`
- Interval: 30 seconds

---

## Environment Variables (Optional)
- `STREAMLIT_SERVER_PORT=8501`
- `STREAMLIT_SERVER_HEADLESS=true`