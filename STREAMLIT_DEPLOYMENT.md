# Streamlit Cloud Deployment Guide

## Step 1: Connect GitHub Repository to Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Select "GitHub repository"
4. Choose: `bhaktofmahakal/llm-task`
5. Select branch: `main`
6. Select file: `streamlit_app.py`

## Step 2: Add Secrets

In Streamlit Cloud dashboard:

1. Click on your app
2. Go to "Settings" → "Secrets"
3. Add the following in TOML format:

```toml
GROQ_API_KEY = "your-groq-api-key-here"
```

**Do NOT paste the API key in the browser!** 

Instead:
1. Copy your API key from https://console.groq.com
2. Paste it carefully into the Secrets section

## Step 3: Deploy

The app will automatically deploy when you add secrets. It may take 2-5 minutes.

## Step 4: Monitor

- View logs to check for errors
- App URL will be: `https://[your-username]-llm-task.streamlit.app`

---

## Important: Secrets Format

The format must be valid TOML. Keep it simple:

```toml
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxxx"
```

**NOT:**
- `GROQ_API_KEY="value"` (bad spacing)
- `GROQ_API_KEY: value` (YAML syntax)
- `GROQ_API_KEY value` (missing =)

## Troubleshooting Deployment

### Error: "Invalid format: please enter valid TOML"
- Copy the secret value exactly as is
- No extra spaces
- No special characters before/after
- Use double quotes: `"value"`

### Error: "Module not found"
- All packages are in requirements.txt
- Streamlit Cloud will install them automatically

### Error: "Timeout or API not responding"
- Check your Groq API key is valid
- Test locally first with `python sample_usage.py`

### Error: "ChromaDB initialization failed"
- This is normal for first run
- The database will be created in `/tmp`
- May take 30+ seconds first time

## Performance Notes

- First load: 30-60 seconds (downloading models)
- Subsequent loads: 2-5 seconds
- Cold start: Streamlit Cloud may take longer

## Regional Availability

Streamlit Cloud servers are in US. If experiencing latency:
- Consider alternative: Railway, Render, or Vercel
- Or deploy locally and use ngrok for sharing

## Cost

- Streamlit Community Cloud: **FREE** (one public app per account)
- Pro plan available for multiple private apps

---

## After Deployment

Share your app link:
```
https://share.streamlit.io/[username]/llm-task/main/streamlit_app.py
```

Or shorter version (if using Streamlit domain):
```
https://[username]-llm-task.streamlit.app
```

## Updating the App

1. Make changes locally
2. Push to GitHub: `git push origin main`
3. Streamlit Cloud auto-deploys (takes 1-2 minutes)

No manual redeploy needed!

