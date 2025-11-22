# Deployment Checklist

## Local Setup ✓
- [x] Python 3.8+ installed
- [x] Dependencies in requirements.txt
- [x] .env file with GROQ_API_KEY
- [x] Tested with `python sample_usage.py`
- [x] Tested with `streamlit run streamlit_app.py`

## GitHub Setup ✓
- [x] Repository created: bhaktofmahakal/llm-task
- [x] Initial commit pushed
- [x] .gitignore configured
- [x] All source files committed

## Streamlit Cloud Deployment

### Pre-Deployment
- [ ] Visit https://streamlit.io/cloud
- [ ] Sign in with GitHub account
- [ ] Authorize Streamlit to access your repositories
- [ ] Refresh to see your repositories

### Create New App
- [ ] Click "New app"
- [ ] Select "GitHub repository"
- [ ] Choose `bhaktofmahakal/llm-task`
- [ ] Select branch: `main`
- [ ] Select file: `streamlit_app.py`

### Configure Secrets
- [ ] Click on deployed app
- [ ] Go to Settings → Secrets
- [ ] Enter secrets in TOML format:
```toml
GROQ_API_KEY = "gsk_..."
```
- [ ] Make sure format is valid TOML
- [ ] Save

### Verify Deployment
- [ ] Wait 2-5 minutes for deployment
- [ ] Check app URL works
- [ ] Try entering a test claim
- [ ] Verify fact checking works
- [ ] Check results display correctly

## Documentation

### For Users/Reviewers
- [ ] README.md explains what the system does
- [ ] DEPLOYMENT_GUIDE.md has setup instructions
- [ ] STREAMLIT_DEPLOYMENT.md has cloud deployment steps
- [ ] Example usage in README

### For Demo
- [ ] DEMO_SCRIPT.md ready (NOT on GitHub)
- [ ] Test statements prepared
- [ ] Recording setup tested
- [ ] Audio quality verified

## Final Checks

### Code Quality
- [ ] All modules import correctly
- [ ] No hardcoded secrets in code
- [ ] Error handling implemented
- [ ] Clear variable names

### Performance
- [ ] Fact checking completes in <30 seconds
- [ ] Web interface responsive
- [ ] Database initializes on startup
- [ ] No memory leaks on repeated runs

### Security
- [ ] API key in environment variables only
- [ ] No API keys in git history
- [ ] .gitignore includes secrets files
- [ ] HTTPS enforced in Streamlit Cloud

## Deployment Commands

### Git Push
```bash
cd u:\llm-task
git add .
git commit -m "docs: add deployment guides"
git push origin main
```

### Test Locally
```bash
python sample_usage.py
```

### Run Web App
```bash
python -m streamlit run streamlit_app.py
```

## Post-Deployment

### Share Links
```
GitHub: https://github.com/bhaktofmahakal/llm-task
Streamlit: https://[username]-llm-task.streamlit.app
```

### Monitor
- [ ] Check Streamlit Cloud logs
- [ ] Test with different claims
- [ ] Monitor for errors
- [ ] Check performance metrics

### Update
- [ ] Make code changes
- [ ] Push to GitHub
- [ ] Streamlit auto-deploys
- [ ] Verify changes live

## Estimated Timeline

- Local setup: 10 minutes
- GitHub push: 2 minutes
- Streamlit deployment: 5 minutes
- Testing: 10 minutes
- **Total: ~30 minutes**

## Troubleshooting

### Won't Deploy
1. Check `requirements.txt` is valid
2. Check `streamlit_app.py` exists
3. Check .gitignore not excluding critical files
4. Check GitHub repo is public

### Says "Invalid format" for secrets
1. Use only: `KEY = "value"`
2. No extra spaces around `=`
3. Double quotes around value
4. No trailing spaces

### Model not found error
1. Check GROQ_API_KEY is correct
2. Visit https://console.groq.com to verify
3. Check config.py for correct model name
4. Deploy new version after fix

### Fact checking returns error
1. Check chroma_db folder isn't in .gitignore
2. Database initializes on first run (takes 30s)
3. Check fact_base.csv is in repo
4. Restart app if needed

## Success Indicators

✅ App deploys without errors
✅ Can enter a claim in web interface
✅ System returns verdict with evidence
✅ Multiple claims are handled correctly
✅ Confidence scores display
✅ App doesn't crash on invalid input

---

**Next Steps:**
1. Complete GitHub setup
2. Deploy to Streamlit Cloud
3. Record demo video
4. Submit assignment

