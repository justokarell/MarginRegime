# Deploy Your Margin Debt Regime Monitor Website

## 🚀 Quick Deploy Options

You have a complete standalone website. Choose your deployment method:

---

## **Option 1: Netlify (EASIEST - 2 minutes)**

### Steps:
1. Go to https://app.netlify.com/drop
2. Drag and drop these files:
   - `index.html`
   - `regime_history.csv`
3. **Done!** You get a URL like: `https://random-name.netlify.app`

### To get custom domain:
- Click "Domain settings"
- Add your custom domain (e.g., `margin-regime.yoursite.com`)

### To update:
- Just drag new files to the same site

**Cost: FREE forever**

---

## **Option 2: GitHub Pages (FREE, with custom domain)**

### Steps:
1. Create GitHub repository: `margin-regime-monitor`
2. Upload files:
   - `index.html`
   - `regime_history.csv`
3. Go to Settings → Pages
4. Select "Deploy from main branch"
5. **Done!** URL: `https://yourusername.github.io/margin-regime-monitor`

### Custom domain:
- Add CNAME file with your domain
- Update DNS settings

**Cost: FREE**

---

## **Option 3: Vercel (FREE, professional)**

### Steps:
1. Go to https://vercel.com
2. Click "Import Project"
3. Upload files or connect GitHub
4. **Done!** URL: `https://margin-regime.vercel.app`

### Custom domain:
- Add in dashboard (free SSL included)

**Cost: FREE**

---

## **Option 4: Your Own Web Hosting**

If you have hosting (Bluehost, GoDaddy, etc.):

1. Upload files via FTP or cPanel
2. Put in public_html folder
3. Access at `https://yoursite.com`

**Cost: Whatever you pay for hosting**

---

## 📁 Files You Need

**Required:**
- `index.html` (the website)
- `regime_history.csv` (your data)

That's it! Just 2 files.

---

## 🔄 Monthly Updates

### Method 1: Manual
1. Run `regime_classification.py` monthly
2. Upload new `regime_history.csv`
3. Site auto-updates (no code changes needed)

### Method 2: Automated (GitHub Actions)

Create `.github/workflows/update.yml`:

```yaml
name: Update Data
on:
  schedule:
    - cron: '0 0 1 * *'  # First of each month
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      
      - name: Install dependencies
        run: pip install pandas openpyxl scipy scikit-learn
      
      - name: Fetch and process data
        run: |
          python fetch_margin_data.py
          python regime_classification.py
      
      - name: Deploy
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add regime_history.csv
          git commit -m "Auto-update $(date)"
          git push
```

---

## 🎨 Customization

### Change colors:
Edit the CSS in `<style>` section of index.html

### Add your logo:
```html
<div class="header">
    <img src="your-logo.png" alt="Logo" style="height: 50px;">
    <h1>Margin Debt Regime Monitor</h1>
</div>
```

### Add Google Analytics:
```html
<!-- Before </head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-ID');
</script>
```

---

## 📱 Features

### Your website has:
- ✅ **Fully responsive** (works on phones, tablets, desktop)
- ✅ **Interactive charts** (zoom, pan, hover)
- ✅ **3 tabs** (Overview, Deep Dive, Historical)
- ✅ **Real-time warnings** based on thresholds
- ✅ **No backend needed** - pure HTML/JavaScript
- ✅ **Works offline** once loaded
- ✅ **Fast loading** (<1 second)

---

## 🔗 How to Share

### In your newsletter:
```markdown
📊 **[View Live Regime Monitor →](https://your-url.com)**

Current Status: Late-Cycle Expansion (+36.3% YoY)
⚠️ Deceleration Active | Mean Reversion Risk
```

### Social media:
```
📊 New tool: Real-time Margin Debt Regime Monitor

Track market expansion/contraction with signal processing
🟡 Currently: Late-cycle expansion
⚠️ Watch for: Deceleration + mean reversion

👉 [your-url]
```

### Embed in your site:
```html
<iframe src="https://your-url.com" 
        width="100%" height="800px" 
        frameborder="0">
</iframe>
```

---

## 🐛 Troubleshooting

**Charts not loading?**
- Check browser console for errors
- Make sure `regime_history.csv` is in same folder
- Try different browser

**Data not updating?**
- Clear browser cache
- Check CSV file format (must have headers)

**Site too slow?**
- Reduce data points (use last 200 rows instead of all)
- Host CSV on CDN

---

## 📊 Advanced: Embed Data in HTML

If you don't want a separate CSV file, you can embed data directly:

In the `<script>` section, replace:
```javascript
async function loadDataFromCSV() {
```

With:
```javascript
function useEmbeddedData() {
    regimeData = [
        {Date: "2025-11", YoY_Change_pct: "36.31", ...},
        {Date: "2025-10", YoY_Change_pct: "45.17", ...},
        // ... all your data
    ];
    initializeDashboard();
}
useEmbeddedData();
```

Then you only need `index.html` (no CSV file).

---

## 🎯 Recommended Path

**For most users:**
1. Use **Netlify Drop** for instant deployment
2. Get free `https://margin-regime.netlify.app` URL
3. Update monthly by dragging new CSV
4. Later: Add custom domain when ready

**Total time: 2 minutes**
**Total cost: $0**

---

## 💡 Pro Tips

1. **Bookmark the deploy URL** for easy updates
2. **Set calendar reminder** to update monthly
3. **Test on mobile** before sharing
4. **Add to your email signature** for visibility
5. **Pin in newsletter** header for subscribers

Your website is production-ready and looks professional!
