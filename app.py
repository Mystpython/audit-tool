from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

# Main Home Page jahan client aakar apni website ka URL daale ga
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Mudassir HQ | Instant Free SEO Audit</title>
        <style>
            body { background-color: #0a0a0a; color: #fff; font-family: 'Arial', sans-serif; text-align: center; padding-top: 50px; }
            h1 { color: #00ffff; letter-spacing: 2px; }
            input { padding: 12px; width: 350px; border-radius: 5px; border: 1px solid #333; background: #111; color: #fff; margin-right: 10px; }
            button { padding: 12px 24px; background-color: #00ffff; color: #000; font-weight: bold; border: none; border-radius: 5px; cursor: pointer; }
            #results { margin-top: 30px; text-align: left; max-width: 600px; margin-left: auto; margin-right: auto; background: #111; padding: 20px; borderRadius: 8px; border: 1px solid #222; display: none; }
            .broken-link { color: #ff0055; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>🤖 Instant SEO Broken Link Audit Tool</h1>
        <p style="color: #888;">Enter your website URL below to get an instant outbound health report.</p>
        
        <form id="auditForm">
            <input type="url" id="targetUrl" placeholder="https://yourwebsite.com" required>
            <button type="submit">SCAN SITE NOW</button>
        </form>

        <div id="results">
            <h3 style="color: #00ff00;">📊 Audit Complete Result:</h3>
            <p id="totalLinks">Total Links Checked: 0</p>
            <ul id="brokenList"></ul>
            <hr style="border-color: #222; margin-top: 20px;">
            <p style="text-align: center; font-weight: bold; color: #00ffff;">
                ⚠️ Want Mudassir Hussain to fix these dead links permanently? <br>
                <a href="mailto:xavierbacklinksexpert@gmail.com" style="color: #ff0055; text-decoration: none;">Click Here to Hire Me Instantly for $85</a>
            </p>
        </div>

        <script>
            document.getElementById('auditForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const url = document.getElementById('targetUrl').value;
                const resultsDiv = document.getElementById('results');
                resultsDiv.style.display = 'block';
                resultsDiv.innerHTML = '<p style="color: #00ffff;">🕵️‍♂️ Scanning backend servers... Please wait...</p>';

                const response = await fetch('/scan', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: url })
                });
                
                const data = await response.json();
                if(data.error) {
                    resultsDiv.innerHTML = `<p style="color: red;">❌ Error: ${data.error}</p>`;
                    return;
                }

                let brokenItems = '';
                data.broken_links.forEach(link => {
                    brokenItems += `<li class="broken-link">${link}</li>`;
                });

                resultsDiv.innerHTML = `
                    <h3 style="color: #00ff00;">📊 Audit Complete Result for ${url}</h3>
                    <p><b>Total Links Scanned:</b> ${data.total_checked}</p>
                    <p style="color: #ff0055;"><b>Dead / Broken Links Found:</b> ${data.broken_links.length}</p>
                    <ul>${brokenItems || '<li>Wow! No broken links found. Clear SEO health! 🎉</li>'}</ul>
                    <hr style="border-color: #222; margin-top: 20px;">
                    <p style="text-align: center; font-weight: bold; color: #00ffff; font-size: 16px;">
                        ⚠️ Want Mudassir Hussain to fix these dead links & optimize authority? <br>
                        <span style="color: #fff;">Let's secure your site traffic before it leaks.</span><br><br>
                       <a href="https://wa.me/923172931708?text=Hi%20Mudassir,%20I%20scanned%20my%20website%20using%20your%20tool%20and%20found%20broken%20links.%20I%20want%20to%20hire%20you%20to%20fix%20them." target="_blank" style="background: #ff0055; color: white; padding: 10px 20px;
                    </p>
                `;
            });
        </script>
    </body>
    </html>
    '''

# Main Background Scanning API Endpoint
@app.route('/scan', methods=['POST'])
def scan_endpoint():
    data = request.get_json()
    site_url = data.get('url')
    
    if not site_url:
        return jsonify({"error": "No URL provided"}), 400

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(site_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        
        external_links = []
        for link in links:
            full_url = urljoin(site_url, link)
            if full_url.startswith('http') and not full_url.startswith(site_url):
                external_links.append(full_url)
        
        # Test matching (Hum sirf top 15 links filter kar rahe hain taake fast test ho sake)
        target_links = list(set(external_links))[:15]
        broken_links = []
        
        for link in target_links:
            try:
                res = requests.head(link, headers=headers, timeout=5)
                if res.status_code >= 400:
                    broken_links.append(link)
            except:
                broken_links.append(link) # Timeout/Dead domain
                
        return jsonify({
            "total_checked": len(target_links),
            "broken_links": broken_links
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
