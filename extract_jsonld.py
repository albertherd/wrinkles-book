import urllib.request
import json
import re

urls = [
    'https://www.midseabooks.com/shop/art-photography/wrinkles/',
    'https://wrinklesbook.com/'
]

for url in urls:
    print(f"--- {url} ---")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        # Find all script tags with type application/ld+json
        pattern = re.compile(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.DOTALL | re.IGNORECASE)
        scripts = pattern.findall(html)
        
        for i, script in enumerate(scripts):
            print(f"Script {i+1}:")
            try:
                data = json.loads(script)
                print(json.dumps(data, indent=2))
            except Exception as e:
                print("Error parsing JSON:", e)
                print(script)
    except Exception as e:
        print("Error fetching:", e)
